#!/usr/bin/env python

import unittest

TEST_MODULES = [
    'codegenloader.test.thrift_test',
    'codegenloader.test.protobuf_test',
    ]


def all():
    return unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)

if __name__ == '__main__':
    unittest.main(defaultTest='all')
