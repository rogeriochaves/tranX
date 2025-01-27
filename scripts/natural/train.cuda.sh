#!/bin/bash
set -e

seed=${1:-0}
dataset_path="natural/dataset"
vocab="$dataset_path/vocab.freq15.bin"
train_file="$dataset_path/train.bin"
dev_file="$dataset_path/dev.bin"
test_file="$dataset_path/test.bin"
dropout=0.3
hidden_size=256
embed_size=128
action_embed_size=128
field_embed_size=64
type_embed_size=64
ptrnet_hidden_dim=32
lr=0.001
lr_decay=0.5
beam_size=15
lstm='lstm'  # lstm
model_name=model.sup.natural.${lstm}.hidden${hidden_size}.embed${embed_size}.action${action_embed_size}.field${field_embed_size}.type${type_embed_size}.dropout${dropout}.lr${lr}.lr_decay${lr_decay}.beam_size${beam_size}.$(basename ${vocab}).$(basename ${train_file}).glorot.par_state_w_field_embe.seed${seed}

echo "**** Writing results to natural/logs/${model_name}.log ****"
mkdir -p natural/logs
echo commit hash: `git rev-parse HEAD` > natural/logs/${model_name}.log

# --cuda
python3 exp.py \
    --cuda \
    --seed ${seed} \
    --mode train \
    --batch_size 10 \
    --asdl_file asdl/lang/py3/py3_asdl.simplified.txt \
    --transition_system python3 \
    --evaluator python3_evaluator \
    --train_file ${train_file} \
    --dataset_path ${dataset_path} \
    --dev_file ${dev_file} \
    --test_file ${test_file} \
    --vocab ${vocab} \
    --lstm ${lstm} \
    --no_parent_field_type_embed \
    --no_parent_production_embed \
    --hidden_size ${hidden_size} \
    --embed_size ${embed_size} \
    --action_embed_size ${action_embed_size} \
    --field_embed_size ${field_embed_size} \
    --type_embed_size ${type_embed_size} \
    --dropout ${dropout} \
    --patience 5 \
    --max_num_trial 5 \
    --glorot_init \
    --lr ${lr} \
    --lr_decay ${lr_decay} \
    --beam_size ${beam_size} \
    --log_every 50 \
    --save_to natural/saved_models/${model_name} # 2>&1 | tee -a natural/logs/${model_name}.log

. scripts/natural/test.sh natural/saved_models/${model_name}.bin 2>&1 | tee -a natural/logs/${model_name}.log
