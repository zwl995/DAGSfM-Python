"""
Utility functions for DAGSfM-Python
"""

import os
import numpy as np


def create_working_directory(directory_path):
    """
    Create a working directory if it doesn't exist
    
    Args:
        directory_path (str): Path to the directory to create
        
    Returns:
        str: Path to the created directory
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    return directory_path


def create_database_file(database_path):
    """
    Create an empty database file for COLMAP
    
    Args:
        database_path (str): Path where the database file should be created
        
    Returns:
        str: Path to the created database file
    """
    # Create directory if it doesn't exist
    db_dir = os.path.dirname(database_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    # Create empty database file
    # In a real implementation, this would initialize a SQLite database
    # with the proper COLMAP schema
    with open(database_path, 'w') as f:
        pass
    
    return database_path


def load_images_from_directory(image_directory):
    """
    Load all images from a directory
    
    Args:
        image_directory (str): Path to directory containing images
        
    Returns:
        list: List of image file paths
    """
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    image_paths = []
    
    for file in os.listdir(image_directory):
        if any(file.lower().endswith(ext) for ext in image_extensions):
            image_paths.append(os.path.join(image_directory, file))
            
    return sorted(image_paths)


def compute_image_similarity(image1_features, image2_features):
    """
    Compute similarity between two images based on their features
    
    Args:
        image1_features: Features from first image
        image2_features: Features from second image
        
    Returns:
        float: Similarity score between the images
    """
    # TODO: Implement actual similarity computation
    # This could be based on feature matching count, geometric consistency, etc.
    return 0.0


def visualize_point_cloud(points, colors=None):
    """
    Visualize 3D point cloud
    
    Args:
        points: 3D coordinates of points (Nx3 array)
        colors: Colors for points (Nx3 array, optional)
    """
    # TODO: Implement point cloud visualization
    # Could use matplotlib, open3d, or other visualization library
    pass


def save_reconstruction(reconstruction, output_path):
    """
    Save reconstruction to disk
    
    Args:
        reconstruction: The reconstruction to save
        output_path (str): Path to save the reconstruction
    """
    # TODO: Implement reconstruction saving
    # Could save as PLY, OBJ, or other 3D formats
    pass