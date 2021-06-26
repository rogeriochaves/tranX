import unittest

import server.app as server

test_server = server.app.test_client()

class AppTestCase(unittest.TestCase):
    def test_parses_code(self):
        res = test_server.get("/api/parse", query_string=dict(
            code="one plus one"
        ))
        self.assertEqual(res.data.decode(), "1 + 1")

    def test_parses_simple_function_calls(self):
        res = test_server.get("/api/parse", query_string=dict(
            code="print 'hello world'"
        ))
        self.assertEqual(res.data.decode(), "print('hello world')")

    def test_evaluates_code(self):
        res = test_server.post("/api/execute", json=dict(
            code="foo = 1 + 1\nprint(foo)"
        ))
        self.assertEqual(res.data.decode(), "2\n")

    def test_outputs_all_print_statements(self):
        res = test_server.post("/api/execute", json=dict(
            code="foo = 1 + 1\nprint(foo)\nprint('bar')"
        ))
        self.assertEqual(res.data.decode(), "2\nbar\n")

    def test_executes_loops(self):
        res = test_server.post("/api/execute", json=dict(
            code="counter = 0\nfor _ in range(20):\n    counter += 1\nprint(counter)"
        ))
        self.assertEqual(res.data.decode(), "20\n")