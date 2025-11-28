"""
Unit tests for the partition module
"""

import unittest
import sys
import os

# Add the dagsfm directory to the path so we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'dagsfm'))

from partition import ViewGraphNode, ViewGraph, NcutPartitioner


class TestViewGraphNode(unittest.TestCase):
    """Test cases for the ViewGraphNode class"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.node = ViewGraphNode(image_id=1)
    
    def test_init(self):
        """Test ViewGraphNode initialization"""
        self.assertEqual(self.node.image_id, 1)
        self.assertIsNone(self.node.features)
        self.assertEqual(self.node.edges, {})
    
    def test_add_edge(self):
        """Test adding edges to a node"""
        self.node.add_edge(neighbor_id=2, weight=0.5)
        self.assertIn(2, self.node.edges)
        self.assertEqual(self.node.edges[2], 0.5)


class TestViewGraph(unittest.TestCase):
    """Test cases for the ViewGraph class"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.graph = ViewGraph()
    
    def test_init(self):
        """Test ViewGraph initialization"""
        self.assertEqual(self.graph.nodes, {})
    
    def test_add_node(self):
        """Test adding nodes to the graph"""
        self.graph.add_node(image_id=1)
        self.assertIn(1, self.graph.nodes)
        self.assertIsInstance(self.graph.nodes[1], ViewGraphNode)
    
    def test_add_edge(self):
        """Test adding edges between nodes"""
        # First add nodes
        self.graph.add_node(image_id=1)
        self.graph.add_node(image_id=2)
        
        # Then add edge
        self.graph.add_edge(image_id1=1, image_id2=2, weight=0.8)
        
        # Check that both nodes have the edge
        self.assertIn(2, self.graph.nodes[1].edges)
        self.assertIn(1, self.graph.nodes[2].edges)
        self.assertEqual(self.graph.nodes[1].edges[2], 0.8)
        self.assertEqual(self.graph.nodes[2].edges[1], 0.8)


class TestNcutPartitioner(unittest.TestCase):
    """Test cases for the NcutPartitioner class"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.partitioner = NcutPartitioner()
    
    def test_init(self):
        """Test NcutPartitioner initialization"""
        self.assertIsInstance(self.partitioner, NcutPartitioner)


if __name__ == '__main__':
    unittest.main()