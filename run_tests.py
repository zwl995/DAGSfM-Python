#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to run all tests for the DAGSfM-Python project
"""

import unittest
import sys
import os


def run_all_tests():
    """Discover and run all tests in the tests directory"""
    # Add the project root and dagsfm directory to the path
    project_root = os.path.dirname(os.path.abspath(__file__))
    dagsfm_path = os.path.join(project_root, 'dagsfm')
    tests_path = os.path.join(project_root, 'tests')
    
    sys.path.insert(0, project_root)
    sys.path.insert(0, dagsfm_path)
    sys.path.insert(0, tests_path)
    
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = tests_path
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code based on test results
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    exit_code = run_all_tests()
    sys.exit(exit_code)