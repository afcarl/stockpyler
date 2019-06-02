import test_stockpyler
import os

THIS_DIR = os.path.abspath(os.path.dirname(__file__))

import pyximport; pyximport.install(language_level=3,setup_args={'include_dirs':THIS_DIR})
import rff


print("Asdf")
test_stockpyler.test_stockpyler()