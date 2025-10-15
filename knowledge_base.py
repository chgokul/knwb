"""
Knowledge Base Search Engine
A simple yet effective knowledge-based search engine with TF-IDF ranking.
"""

import json
import math
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple


class KnowledgeBase:
    """
    A knowledge-based search engine that indexes documents and performs searches
    using TF-IDF (Term Frequency-Inverse Document Frequency) scoring.
    """
    
    def __init__(self):
        self.documents = []
        self.index = defaultdict(list)  # term -> [(doc_id, positions)]
        self.doc_freq = Counter()  # term -> number of documents containing term
        self.doc_lengths = []  # document lengths for normalization
        
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into lowercase words."""
        return re.findall(r'\w+', text.lower())
    
    def add_document(self, doc_id: int, title: str, content: str):
        """Add a document to the knowledge base."""
        full_text = f"{title} {content}"
        tokens = self._tokenize(full_text)
        
        # Store document
        self.documents.append({
            'id': doc_id,
            'title': title,
            'content': content
        })
        
        # Build index
        term_positions = defaultdict(list)
        for pos, token in enumerate(tokens):
            term_positions[token].append(pos)
        
        for term, positions in term_positions.items():
            self.index[term].append((doc_id, positions))
            self.doc_freq[term] += 1
        
        self.doc_lengths.append(len(tokens))
    
    def _calculate_tf_idf(self, term: str, doc_id: int, term_freq: int) -> float:
        """Calculate TF-IDF score for a term in a document."""
        # Term Frequency (normalized by document length)
        tf = term_freq / max(self.doc_lengths[doc_id], 1)
        
        # Inverse Document Frequency with smoothing
        # Adding 1 to numerator gives non-zero scores even for single documents
        idf = math.log(1 + len(self.documents) / (self.doc_freq[term] + 1))
        
        return tf * idf
    
    def search(self, query: str, top_k: int = 5) -> List[Tuple[int, float, Dict]]:
        """
        Search for documents matching the query.
        Returns a list of (doc_id, score, document) tuples.
        """
        query_tokens = self._tokenize(query)
        scores = defaultdict(float)
        
        for term in query_tokens:
            if term in self.index:
                for doc_id, positions in self.index[term]:
                    term_freq = len(positions)
                    tf_idf = self._calculate_tf_idf(term, doc_id, term_freq)
                    scores[doc_id] += tf_idf
        
        # Sort by score and return top-k results
        ranked_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        
        results = []
        for doc_id, score in ranked_results:
            results.append((doc_id, score, self.documents[doc_id]))
        
        return results
    
    def save(self, filepath: str):
        """Save the knowledge base to a JSON file."""
        data = {
            'documents': self.documents,
            'index': {term: postings for term, postings in self.index.items()},
            'doc_freq': dict(self.doc_freq),
            'doc_lengths': self.doc_lengths
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load(self, filepath: str):
        """Load the knowledge base from a JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.documents = data['documents']
        self.index = defaultdict(list, {term: postings for term, postings in data['index'].items()})
        self.doc_freq = Counter(data['doc_freq'])
        self.doc_lengths = data['doc_lengths']
