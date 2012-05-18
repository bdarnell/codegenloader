import unittest
from google.protobuf.message import Message


class ProtobufTest(unittest.TestCase):
    def test_simple_import(self):
        from codegenloader.test.proto.simple_pb2 import Simple
        self.assertTrue(issubclass(Simple, Message))
