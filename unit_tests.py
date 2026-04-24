"""
This module is designed to contain the written unit tests for our code
"""
import unittest
from ai import AiAgent

class AiUnitTests (unittest.TestCase):
    """A class to hold unit tests for the ai"""
    def setUp(self):
        self.ai = AiAgent({'move': 1, 'search': 2, 'talk': 2})
