# coding=utf-8

from __future__ import print_function

import torch
import os
import re
import pickle
import ast
import astor
import nltk
import sys

import numpy as np

from asdl.lang.py3.py3_transition_system import python_ast_to_asdl_ast, asdl_ast_to_python_ast, Python3TransitionSystem, tokenize_code
from asdl.hypothesis import *

from components.action_info import get_action_infos

p_elif = re.compile(r'^elif\s?')
p_else = re.compile(r'^else\s?')
p_try = re.compile(r'^try\s?')
p_except = re.compile(r'^except\s?')
p_finally = re.compile(r'^finally\s?')
p_decorator = re.compile(r'^@.*')

QUOTED_STRING_RE = re.compile(
    r"(?P<quote>['\"])(?P<string>.*?)(?<!\\)(?P=quote)")


# From: https://stackoverflow.com/questions/14820429/how-do-i-decodestring-escape-in-python3
def string_escape(s, encoding='utf-8'):
    return (s.encode('utf-8')          # To bytes, required by 'unicode-escape'
             .decode('unicode-escape') # Perform the actual octal-escaping decode
             .encode('utf-8')          # 1:1 mapping back to bytes
             .decode(encoding))        # Decode original encoding


def replace_string_ast_nodes(py_ast, str_map):
    for node in ast.walk(py_ast):
        if isinstance(node, ast.Str):
            str_val = node.s

            if str_val in str_map:
                node.s = str_map[str_val]
            else:
                # handle cases like `\n\t` in string literals
                for key, val in str_map.items():
                    str_literal_decoded = string_escape(key)
                    if str_literal_decoded == str_val:
                        node.s = val


class Python3(object):
    @staticmethod
    def canonicalize_code(code):
        if p_elif.match(code):
            code = 'if True: pass\n' + code

        if p_else.match(code):
            code = 'if True: pass\n' + code

        if p_try.match(code):
            code = code + 'pass\nexcept: pass'
        elif p_except.match(code):
            code = 'try: pass\n' + code
        elif p_finally.match(code):
            code = 'try: pass\n' + code

        if p_decorator.match(code):
            code = code + '\ndef dummy(): pass'

        if code[-1] == ':':
            code = code + 'pass'

        code = code.replace("\\n", "\n")
        code = code.replace("\\t", "\t")

        return code

    @staticmethod
    def canonicalize_str_nodes(py_ast, str_map):
        for node in ast.walk(py_ast):
            if isinstance(node, ast.Str):
                str_val = node.s

                if str_val in str_map:
                    node.s = str_map[str_val]
                else:
                    # handle cases like `\n\t` in string literals
                    for str_literal, slot_id in str_map.items():
                        str_literal_decoded = string_escape(str_literal)
                        if str_literal_decoded == str_val:
                            node.s = slot_id

    @staticmethod
    def canonicalize_query(query):
        """
        canonicalize the query, replace strings to a special place holder
        """
        str_count = 0
        str_map = dict()

        matches = QUOTED_STRING_RE.findall(query)
        # de-duplicate
        cur_replaced_strs = set()
        for match in matches:
            # If one or more groups are present in the pattern,
            # it returns a list of groups
            quote = match[0]
            str_literal = match[1]
            quoted_str_literal = quote + str_literal + quote

            if str_literal in cur_replaced_strs:
                # replace the string with new quote with slot id
                query = query.replace(quoted_str_literal, str_map[str_literal])
                continue

            # FIXME: substitute the ' % s ' with
            if str_literal in ['%s']:
                continue

            str_repr = '_STR:%d_' % str_count
            str_map[str_literal] = str_repr

            query = query.replace(quoted_str_literal, str_repr)

            str_count += 1
            cur_replaced_strs.add(str_literal)

        # tokenize
        query_tokens = nltk.word_tokenize(query)

        new_query_tokens = []
        # break up function calls like foo.bar.func
        for token in query_tokens:
            new_query_tokens.append(token)
            i = token.find('.')
            if 0 < i < len(token) - 1:
                new_tokens = [
                    '['] + token.replace('.', ' . ').split(' ') + [']']
                new_query_tokens.extend(new_tokens)

        query = ' '.join(new_query_tokens)
        query = query.replace('\' % s \'', '%s').replace('\" %s \"', '%s')

        return query, str_map

    @staticmethod
    def canonicalize_example(query, code):

        canonical_query, str_map = Python3.canonicalize_query(query)
        query_tokens = canonical_query.split(' ')

        canonical_code = Python3.canonicalize_code(code)
        try:
            ast_tree = ast.parse(canonical_code)
        except Exception as e:
            print("canonical_code:\n" + canonical_code)
            raise e


        Python3.canonicalize_str_nodes(ast_tree, str_map)
        canonical_code = astor.to_source(ast_tree)

        # sanity check
        # decanonical_code = Python3.decanonicalize_code(canonical_code, str_map)
        # decanonical_code_tokens = tokenize_code(decanonical_code)
        # raw_code_tokens = tokenize_code(code)
        # if decanonical_code_tokens != raw_code_tokens:
        #     pass

        # try:
        #     ast_tree = ast.parse(canonical_code).body[0]
        # except:
        #     print('error!')
        #     canonical_code = Python3.canonicalize_code(code)
        #     gold_ast_tree = ast.parse(canonical_code).body[0]
        #     str_map = {}

        # parse_tree = python_ast_to_asdl_ast(gold_ast_tree, grammar)
        # gold_source = astor.to_source(gold_ast_tree)
        # ast_tree = asdl_ast_to_python_ast(parse_tree, grammar)
        # source = astor.to_source(ast_tree)

        # assert gold_source == source, 'sanity check fails: gold=[%s], actual=[%s]' % (gold_source, source)
        #
        # # action check
        # parser = Python3TransitionSystem(grammar)
        # actions = parser.get_actions(parse_tree)
        #
        # hyp = Hypothesis()
        # for action in actions:
        #     assert action.__class__ in parser.get_valid_continuation_types(hyp)
        #     if isinstance(action, ApplyRuleAction):
        #         assert action in parser.get_valid_continuations(hyp)
        #     hyp.apply_action(action)
        #
        # src_from_hyp = astor.to_source(asdl_ast_to_python_ast(hyp.tree, grammar))
        # assert src_from_hyp == gold_source

        return query_tokens, canonical_code, str_map

    @staticmethod
    def parse_python3_dataset(dataset_path, asdl_file_path, max_query_len=70, vocab_freq_cutoff=10):
        asdl_text = open(asdl_file_path).read()
        print('building grammar')
        grammar = ASDLGrammar.from_text(asdl_text)
        transition_system = Python3TransitionSystem(grammar)

        loaded_examples = []

        with open(os.path.join(dataset_path, "inputs.txt"), 'r') as file:
            annotations = file.read().split('\n')
        with open(os.path.join(dataset_path, "outputs.txt"), 'r') as file:
            codes = file.read().split('\n')

        annotation_codes = list(zip(annotations, codes))
        np.random.seed(42)
        np.random.shuffle(annotation_codes)

        from components.vocab import Vocab, VocabEntry
        from components.dataset import Example

        print('processing examples')
        for idx, (src_query, tgt_code) in enumerate(annotation_codes):
            if not src_query or not tgt_code:
                continue

            if (idx % 100 == 0 or idx + 1 == len(annotation_codes)):
                sys.stdout.write("\r%s / %s" % (idx, len(annotation_codes)))
                sys.stdout.flush()

            src_query = src_query.strip()
            tgt_code = tgt_code.strip()

            src_query_tokens, tgt_canonical_code, str_map = Python3.canonicalize_example(
                src_query, tgt_code)
            python_ast = ast.parse(tgt_canonical_code)#.body[0]
            gold_source = astor.to_source(python_ast).strip()
            tgt_ast = python_ast_to_asdl_ast(python_ast, transition_system.grammar)
            tgt_actions = transition_system.get_actions(tgt_ast)
            # print('+' * 60)
            # print('Example: %d' % idx)
            # print('Source: %s' % ' '.join(src_query_tokens))
            # if str_map:
            #     print('Original String Map:')
            #     for str_literal, str_repr in str_map.items():
            #         print('\t%s: %s' % (str_literal, str_repr))
            # print('Code:\n%s' % gold_source)
            # print('Actions:')

            # sanity check
            hyp = Hypothesis()
            for t, action in enumerate(tgt_actions):
                assert action.__class__ in transition_system.get_valid_continuation_types(hyp)
                if isinstance(action, ApplyRuleAction):
                    assert action.production in transition_system.get_valid_continuating_productions(hyp)
                # assert action.__class__ in transition_system.get_valid_continuation_types(
                # hyp)

                p_t = -1
                f_t = None
                if hyp.frontier_node:
                    p_t = hyp.frontier_node.created_time
                    f_t = hyp.frontier_field.field.__repr__(plain=True)

                # print('\t[%d] %s, frontier field: %s, parent: %d' %
                #     (t, action, f_t, p_t))
                hyp = hyp.clone_and_apply_action(action)

            # assert hyp.frontier_node is None and hyp.frontier_field is None

            src_from_hyp = astor.to_source(
                asdl_ast_to_python_ast(hyp.tree, grammar)).strip()
            if "b'" not in str(gold_source) and 'b"' not in str(gold_source):
                assert src_from_hyp == gold_source

            # print('+' * 60)

            loaded_examples.append({'src_query_tokens': src_query_tokens,
                                    'tgt_canonical_code': gold_source,
                                    'tgt_ast': tgt_ast,
                                    'tgt_actions': tgt_actions,
                                    'raw_code': tgt_code, 'str_map': str_map})

            # print('first pass, processed %d' % idx, file=sys.stderr)

        train_examples = []
        dev_examples = []
        test_examples = []

        action_len = []

        print("\nsplitting train/dev/test")
        for idx, e in enumerate(loaded_examples):
            src_query_tokens = e['src_query_tokens'][:max_query_len]
            tgt_actions = e['tgt_actions']
            tgt_action_infos = get_action_infos(src_query_tokens, tgt_actions)

            example = Example(idx=idx,
                              src_sent=src_query_tokens,
                              tgt_actions=tgt_action_infos,
                              tgt_code=e['tgt_canonical_code'],
                              tgt_ast=e['tgt_ast'],
                              meta={'raw_code': e['raw_code'], 'str_map': e['str_map']})

            # print('second pass, processed %d' % idx, file=sys.stderr)

            action_len.append(len(tgt_action_infos))

            # train, valid, test split
            total_examples = len(loaded_examples)
            split_size = np.ceil(total_examples * 0.05)
            (dev_split, test_split) = (total_examples - split_size * 2, total_examples - split_size)
            if 0 <= idx < dev_split:
                train_examples.append(example)
            elif dev_split <= idx < test_split:
                dev_examples.append(example)
            else:
                test_examples.append(example)

        print('Max action len: %d' % max(action_len), file=sys.stderr)
        print('Avg action len: %d' % np.average(action_len), file=sys.stderr)
        print('Actions larger than 100: %d' %
              len(list(filter(lambda x: x > 100, action_len))), file=sys.stderr)

        src_vocab = VocabEntry.from_corpus(
            [e.src_sent for e in train_examples], size=5000, freq_cutoff=vocab_freq_cutoff)

        primitive_tokens = [map(lambda a: a.action.token,
                            filter(lambda a: isinstance(a.action, GenTokenAction), e.tgt_actions))
                            for e in train_examples]

        primitive_vocab = VocabEntry.from_corpus(
            primitive_tokens, size=5000, freq_cutoff=vocab_freq_cutoff)
        # assert '_STR:0_' in primitive_vocab

        # generate vocabulary for the code tokens!
        code_tokens = [tokenize_code(e.tgt_code, mode='decoder')
                       for e in train_examples]
        code_vocab = VocabEntry.from_corpus(
            code_tokens, size=5000, freq_cutoff=vocab_freq_cutoff)

        vocab = Vocab(source=src_vocab,
                      primitive=primitive_vocab, code=code_vocab)
        print('generated vocabulary %s' % repr(vocab), file=sys.stderr)

        return (train_examples, dev_examples, test_examples), vocab

    @staticmethod
    def process_python3_dataset(dataset_path):
        vocab_freq_cutoff = 15  # TODO: found the best cutoff threshold

        (train, dev, test), vocab = Python3.parse_python3_dataset(dataset_path, 'asdl/lang/py3/py3_asdl.simplified.txt',
                                                                  vocab_freq_cutoff=vocab_freq_cutoff)

        pickle.dump(train, open(f'{dataset_path}/train.bin', 'wb'))
        pickle.dump(dev, open(f'{dataset_path}/dev.bin', 'wb'))
        pickle.dump(test, open(f'{dataset_path}/test.bin', 'wb'))
        pickle.dump(vocab, open(f'{dataset_path}/vocab.freq%d.bin' %
                    vocab_freq_cutoff, 'wb'))

    @staticmethod
    def run():
        asdl_text = open('asdl/lang/py3/py3_asdl.simplified.txt').read()
        grammar = ASDLGrammar.from_text(asdl_text)

        annot_file = 'data/python3/all.anno'
        code_file = 'data/python3/all.code'

        transition_system = Python3TransitionSystem(grammar)

        for idx, (src_query, tgt_code) in enumerate(zip(open(annot_file), open(code_file))):
            src_query = src_query.strip()
            tgt_code = tgt_code.strip()

            query_tokens, tgt_canonical_code, str_map = Python3.canonicalize_example(
                src_query, tgt_code)
            python_ast = ast.parse(tgt_canonical_code)#.body[0]
            gold_source = astor.to_source(python_ast)
            tgt_ast = python_ast_to_asdl_ast(python_ast, grammar)
            tgt_actions = transition_system.get_actions(tgt_ast)

            # sanity check
            hyp = Hypothesis()
            hyp2 = Hypothesis()
            for action in tgt_actions:
                assert action.__class__ in transition_system.get_valid_continuation_types(
                    hyp)
                if isinstance(action, ApplyRuleAction):
                    assert action.production in transition_system.get_valid_continuating_productions(
                        hyp)
                hyp = hyp.clone_and_apply_action(action)
                hyp2.apply_action(action)

            src_from_hyp = astor.to_source(
                asdl_ast_to_python_ast(hyp.tree, grammar))
            assert src_from_hyp == gold_source
            assert hyp.tree == hyp2.tree and hyp.tree is not hyp2.tree

            print(idx)

    @staticmethod
    def canonicalize_raw_python3_oneliner(code):
        # use the astor-style code
        code = Python3.canonicalize_code(code)
        py_ast = ast.parse(code)#.body[0]
        code = astor.to_source(py_ast).strip()

        return code


def generate_vocab_for_paraphrase_model(vocab_path, save_path):
    from components.vocab import VocabEntry, Vocab

    vocab = pickle.load(open(vocab_path))
    para_vocab = VocabEntry()
    for i in range(0, 10):
        para_vocab.add('<unk_%d>' % i)
    for word in vocab.source.word2id:
        para_vocab.add(word)
    for word in vocab.code.word2id:
        para_vocab.add(word)

    pickle.dump(para_vocab, open(save_path, 'w'))


if __name__ == '__main__':
    # Python3.run()
    # f1 = Field('hahah', ASDLPrimitiveType('123'), 'single')
    # rf1 = RealizedField(f1, value=123)
    #
    # # print(f1 == rf1)
    # a = {f1: 1}
    # print(a[rf1])
    Python3.process_python3_dataset()
    # generate_vocab_for_paraphrase_model('data/python3/vocab.freq10.bin', 'data/python3/vocab.para.freq10.bin')

    # py_ast = ast.parse("""sorted(asf, reverse='k' 'k', k='re' % sdf)""")
    # canonicalize_py_ast(py_ast)
    # for node in ast.walk(py_ast):
    #     if isinstance(node, ast.Str):
    #         print(node.s)
    # print(astor.to_source(py_ast))
