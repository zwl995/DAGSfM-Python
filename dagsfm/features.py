"""
Feature extraction and matching module for DAGSfM-Python
"""

import subprocess
import os

class FeatureExtractor:
    """
    Class for extracting features from images using various algorithms like SIFT, SURF, etc.
    """
    
    def __init__(self, colmap_path="colmap"):
        """
        Initialize feature extractor
        
        Args:
            colmap_path (str): Path to the COLMAP executable, defaults to "colmap"
        """
        self.colmap_path = "colmap"
        self.feature_cfg = {    
                    "ImageReader.camera_model": "OPENCV",
                    # "ImageReader.single_camera_per_folder": "1",
                    # cx, cy, fx, fy, k1, k2, p1, p2
                    # "ImageReader.camera_params": "3707.93,3698.64,2693.69,1825.26,-0.270231,0.109206,0.000298561,3.15755e-05",
                    "SiftExtraction.max_image_size": "3200",
                    "SiftExtraction.max_num_features": "8192",
                    "SiftExtraction.num_threads": "16",
                    "SiftExtraction.use_gpu": "1",
                    "SiftExtraction.gpu_index": "0,1,2,3",
        }  # Configuration dictionary for COLMAP parameters
    
    def extract_features(self, image_path, database_path):
        """
        Extract features from an image and store in database
        
        Args:
            image_path (str): Path to the image file
            database_path (str): Path to the database file
            
        Returns:
            str: Path to the database file with extracted features
        """
        # Build COLMAP feature extractor command
        cmd = (
            f"{self.colmap_path} feature_extractor "
            f"--database_path={database_path} "
            f"--image_path={image_path}"
        )
        
        # Add any additional COLMAP configuration parameters
        for k, v in self.feature_cfg.items():
            cmd += f" --{k}={v}"
        
        # Execute the command
        try:
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"COLMAP feature extraction failed: {e}")
        
        return database_path


class FeatureMatcher:
    """
    Class for matching features between images
    """
    
    def __init__(self, colmap_path="colmap"):
        """
        Initialize feature matcher
        
        Args:
            colmap_path (str): Path to the COLMAP executable, defaults to "colmap"
        """
        self.colmap_path = colmap_path
        self.matcher_cfg = {}  # Configuration dictionary for COLMAP matching parameters
    
    def exhaustive_matcher(self, database_path):
        """
        Perform exhaustive matching on all images in the database
        
        Args:
            database_path (str): Path to the database file
            
        Returns:
            str: Path to the database file with computed matches
        """
        # Build COLMAP exhaustive_matcher command
        cmd = (
            f"{self.colmap_path} exhaustive_matcher "
            f"--database_path={database_path}"
        )
        
        # Add any additional COLMAP configuration parameters
        for k, v in self.matcher_cfg.items():
            cmd += f" --{k}={v}"
        
        # Execute the command
        try:
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"COLMAP exhaustive matching failed: {e}")
        
        return database_path
    
    def build_matching_graph(self, features_list):
        """
        Build a graph representing matching relationships between images
        
        Args:
            features_list: List of features from all images
            
        Returns:
            matching_graph: Graph of image matching relationships
        """
        # TODO: Construct image matching graph
        pass