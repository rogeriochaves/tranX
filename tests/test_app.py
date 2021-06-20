import unittest

import server.app as server

test_server = server.app.test_client()

class AppTestCase(unittest.TestCase):
    def test_parses_and_evaluates_code_sent_to_run(self):
        res = test_server.get("/api/parse", query_string=dict(
            code="one plus one"
        ))
        self.assertEqual(res.data.decode(), "1 + 1")

    def test_evaluates_simple_function_calls(self):
        res = test_server.get("/api/parse", query_string=dict(
            code="print 'hello world'"
        ))
        self.assertEqual(res.data.decode(), "print('hello world')")
