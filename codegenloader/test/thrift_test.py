import unittest


class ThriftTest(unittest.TestCase):
    def test_simple_import(self):
        from codegenloader.test.thriftgen.simple.ttypes import Simple
        self.assertTrue(isinstance(Simple, type))
