import unittest

from api.logger import init_logger
loader = unittest.TestLoader()
tests = loader.discover('.', '*_test.py')
testRunner = unittest.runner.TextTestRunner()
init_logger()
testRunner.run(tests)
