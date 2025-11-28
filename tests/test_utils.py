"""
Unit tests for the utils module
"""

import unittest
import sys
import os
import tempfile
import numpy as np

# Add the dagsfm directory to the path so we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'dagsfm'))

from utils import create_working_directory, load_images_from_directory, compute_image_similarity, create_database_file


class TestUtils(unittest.TestCase):
    """Test cases for utility functions"""
    
    def test_create_working_directory(self):
        """Test creating a working directory"""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_path = os.path.join(temp_dir, "test_directory")
            result_path = create_working_directory(test_path)
            self.assertEqual(result_path, test_path)
            self.assertTrue(os.path.exists(test_path))
            self.assertTrue(os.path.isdir(test_path))
    
    def test_create_database_file(self):
        """Test creating a database file"""
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = os.path.join(temp_dir, "test.db")
            result_path = create_database_file(db_path)
            self.assertEqual(result_path, db_path)
            self.assertTrue(os.path.exists(db_path))
            self.assertTrue(os.path.isfile(db_path))
    
    def test_create_database_file_with_subdir(self):
        """Test creating a database file in a subdirectory"""
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = os.path.join(temp_dir, "subdir", "test.db")
            result_path = create_database_file(db_path)
            self.assertEqual(result_path, db_path)
            self.assertTrue(os.path.exists(db_path))
            self.assertTrue(os.path.isfile(db_path))
    
    def test_load_images_from_directory(self):
        """Test loading images from a directory"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create some test files
            test_files = ["image1.jpg", "image2.png", "data.txt", "image3.jpeg"]
            for file_name in test_files:
                file_path = os.path.join(temp_dir, file_name)
                with open(file_path, 'w') as f:
                    f.write("test content")
            
            # Load image files
            image_paths = load_images_from_directory(temp_dir)
            
            # Check that only image files are returned
            self.assertEqual(len(image_paths), 3)
            
            # Check that the paths are sorted
            expected_paths = sorted([
                os.path.join(temp_dir, "image1.jpg"),
                os.path.join(temp_dir, "image2.png"),
                os.path.join(temp_dir, "image3.jpeg")
            ])
            self.assertEqual(image_paths, expected_paths)
    
    def test_compute_image_similarity(self):
        """Test computing image similarity"""
        # Test with dummy values since the actual implementation is not yet complete
        similarity = compute_image_similarity(None, None)
        self.assertEqual(similarity, 0.0)
        self.assertIsInstance(similarity, float)


if __name__ == '__main__':
    unittest.main()