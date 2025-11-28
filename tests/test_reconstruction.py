"""
Unit tests for the reconstruction module
"""

import unittest
import sys
import os

# Add the dagsfm directory to the path so we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'dagsfm'))

from reconstruction import SubReconstructor


class TestSubReconstructor(unittest.TestCase):
    """Test cases for the SubReconstructor class"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.reconstructor = SubReconstructor()
    
    def test_init(self):
        """Test SubReconstructor initialization"""
        self.assertIsInstance(self.reconstructor, SubReconstructor)
        self.assertTrue(hasattr(self.reconstructor, 'use_pycolmap'))


if __name__ == '__main__':
    unittest.main()