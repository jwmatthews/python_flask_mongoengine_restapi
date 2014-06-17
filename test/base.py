import os
import sys
# Adding sampleapp source code to python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)) + "/../")

if sys.version_info < (2,7):
    # python 2.6
    import unittest2 as unittest
else:
    # python 2.7 and greater
    import unittest

import sampleapp
from sampleapp.models import Item

CONFIG_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), "config/unittests.cfg")

class SampleAppTestCase(unittest.TestCase):

    def drop_collections(self):
        Item.drop_collection()

    def setUp(self):
        sampleapp.app.config['TESTING'] = True
        sampleapp.initialize(CONFIG_FILE)
        self.app = sampleapp.app.test_client()
        self.drop_collections()

    def tearDown(self):
        pass