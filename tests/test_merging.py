"""
Unit tests for the merging module
"""

import unittest
import sys
import os

# Add the dagsfm directory to the path so we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'dagsfm'))

from merging import SubReconstructionMerger


class TestSubReconstructionMerger(unittest.TestCase):
    """Test cases for the SubReconstructionMerger class"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.merger = SubReconstructionMerger()
    
    def test_init(self):
        """Test SubReconstructionMerger initialization"""
        self.assertIsInstance(self.merger, SubReconstructionMerger)
    
    # TODO: Add tests for alignment, merging and bundle adjustment methods
    # after implementing the actual functionality


if __name__ == '__main__':
    unittest.main()