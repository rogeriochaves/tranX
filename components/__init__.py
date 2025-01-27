import six

from datasets.django.evaluator import DjangoEvaluator
from datasets.python3.evaluator import Python3Evaluator

if six.PY3:
    from datasets.conala.evaluator import ConalaEvaluator
    from datasets.wikisql.evaluator import WikiSQLEvaluator
