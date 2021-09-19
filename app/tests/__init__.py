import unittest
import logging
from app.main import app

logging.getLogger('sqlalchemy').setLevel(logging.ERROR)

def run():
    testsuite = unittest.TestLoader().discover('./app/tests/routers', pattern='*_test.py')
    unittest.TextTestRunner(verbosity=1).run(testsuite)