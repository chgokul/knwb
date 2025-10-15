"""
Unit tests for the Knowledge Base Search Engine
"""

import unittest
import os
import json
import tempfile
from knowledge_base import KnowledgeBase


class TestKnowledgeBase(unittest.TestCase):
    
    def setUp(self):
        """Set up test knowledge base."""
        self.kb = KnowledgeBase()
        
    def test_add_document(self):
        """Test adding documents to the knowledge base."""
        self.kb.add_document(0, "Test Title", "Test content")
        self.assertEqual(len(self.kb.documents), 1)
        self.assertEqual(self.kb.documents[0]['title'], "Test Title")
        self.assertEqual(self.kb.documents[0]['content'], "Test content")
    
    def test_tokenization(self):
        """Test text tokenization."""
        tokens = self.kb._tokenize("Hello World! This is a test.")
        self.assertEqual(tokens, ['hello', 'world', 'this', 'is', 'a', 'test'])
    
    def test_search_empty(self):
        """Test search on empty knowledge base."""
        results = self.kb.search("test query")
        self.assertEqual(len(results), 0)
    
    def test_search_single_document(self):
        """Test search with a single document."""
        self.kb.add_document(0, "Python", "Python is a programming language")
        results = self.kb.search("python")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], 0)  # doc_id
        self.assertGreater(results[0][1], 0)  # score should be positive
    
    def test_search_multiple_documents(self):
        """Test search with multiple documents."""
        self.kb.add_document(0, "Python", "Python is a programming language")
        self.kb.add_document(1, "Java", "Java is another programming language")
        self.kb.add_document(2, "Cooking", "How to cook pasta")
        
        results = self.kb.search("programming")
        self.assertEqual(len(results), 2)
        # Both Python and Java should be returned
        doc_ids = [r[0] for r in results]
        self.assertIn(0, doc_ids)
        self.assertIn(1, doc_ids)
    
    def test_search_ranking(self):
        """Test that search results are properly ranked."""
        self.kb.add_document(0, "Python", "Python programming")
        self.kb.add_document(1, "Python Guide", "Complete Python programming guide with examples")
        
        results = self.kb.search("python programming")
        # Document with more occurrences should rank higher
        self.assertEqual(len(results), 2)
        # Both should be returned, ordered by relevance
        self.assertTrue(results[0][1] >= results[1][1])
    
    def test_save_and_load(self):
        """Test saving and loading knowledge base."""
        # Add some documents
        self.kb.add_document(0, "Title 1", "Content 1")
        self.kb.add_document(1, "Title 2", "Content 2")
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            self.kb.save(temp_file)
            
            # Load into new knowledge base
            new_kb = KnowledgeBase()
            new_kb.load(temp_file)
            
            # Verify contents
            self.assertEqual(len(new_kb.documents), 2)
            self.assertEqual(new_kb.documents[0]['title'], "Title 1")
            self.assertEqual(new_kb.documents[1]['title'], "Title 2")
            
            # Verify search works after loading
            results = new_kb.search("content")
            self.assertEqual(len(results), 2)
        finally:
            # Clean up
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_top_k_results(self):
        """Test that top_k parameter limits results."""
        for i in range(10):
            self.kb.add_document(i, f"Title {i}", "Test content")
        
        results = self.kb.search("test", top_k=3)
        self.assertEqual(len(results), 3)
        
        results = self.kb.search("test", top_k=5)
        self.assertEqual(len(results), 5)


if __name__ == '__main__':
    unittest.main()
