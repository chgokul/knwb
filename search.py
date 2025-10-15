#!/usr/bin/env python3
"""
Command-line interface for the Knowledge Base Search Engine.
"""

import argparse
import json
import os
from knowledge_base import KnowledgeBase


def load_sample_data(kb: KnowledgeBase):
    """Load sample knowledge base data."""
    sample_docs = [
        {
            "title": "Python Programming",
            "content": "Python is a high-level, interpreted programming language known for its simplicity and readability. It supports multiple programming paradigms including procedural, object-oriented, and functional programming."
        },
        {
            "title": "Machine Learning Basics",
            "content": "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. It focuses on developing computer programs that can access data and use it to learn for themselves."
        },
        {
            "title": "Web Development",
            "content": "Web development involves creating websites and web applications. It includes front-end development (HTML, CSS, JavaScript) and back-end development (server-side programming, databases)."
        },
        {
            "title": "Data Science",
            "content": "Data science combines statistics, data analysis, and machine learning to extract insights from data. Python is one of the most popular languages for data science due to its extensive libraries like NumPy, Pandas, and Scikit-learn."
        },
        {
            "title": "Artificial Intelligence",
            "content": "Artificial Intelligence (AI) is the simulation of human intelligence processes by machines, especially computer systems. These processes include learning, reasoning, and self-correction."
        }
    ]
    
    for idx, doc in enumerate(sample_docs):
        kb.add_document(idx, doc['title'], doc['content'])


def interactive_search(kb: KnowledgeBase):
    """Interactive search mode."""
    print("\n=== Knowledge Base Search Engine ===")
    print("Type 'quit' or 'exit' to stop\n")
    
    while True:
        query = input("Search: ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if not query:
            continue
        
        results = kb.search(query)
        
        if not results:
            print(f"No results found for '{query}'\n")
        else:
            print(f"\nFound {len(results)} result(s) for '{query}':\n")
            for rank, (doc_id, score, doc) in enumerate(results, 1):
                print(f"{rank}. {doc['title']} (Score: {score:.4f})")
                print(f"   {doc['content'][:150]}...")
                print()


def main():
    parser = argparse.ArgumentParser(description='Knowledge Base Search Engine')
    parser.add_argument('--load', type=str, help='Load knowledge base from JSON file')
    parser.add_argument('--save', type=str, help='Save knowledge base to JSON file')
    parser.add_argument('--add-data', type=str, help='Add documents from JSON file')
    parser.add_argument('--query', type=str, help='Single query search')
    parser.add_argument('--interactive', action='store_true', help='Interactive search mode')
    parser.add_argument('--sample-data', action='store_true', help='Load sample data')
    
    args = parser.parse_args()
    
    kb = KnowledgeBase()
    
    # Load existing knowledge base
    if args.load and os.path.exists(args.load):
        print(f"Loading knowledge base from {args.load}...")
        kb.load(args.load)
        print(f"Loaded {len(kb.documents)} documents")
    
    # Add sample data
    if args.sample_data:
        print("Loading sample data...")
        load_sample_data(kb)
        print(f"Loaded {len(kb.documents)} sample documents")
    
    # Add custom data
    if args.add_data and os.path.exists(args.add_data):
        print(f"Adding data from {args.add_data}...")
        with open(args.add_data, 'r') as f:
            docs = json.load(f)
        for idx, doc in enumerate(docs):
            kb.add_document(len(kb.documents), doc['title'], doc['content'])
        print(f"Added {len(docs)} documents")
    
    # Save knowledge base
    if args.save:
        print(f"Saving knowledge base to {args.save}...")
        kb.save(args.save)
        print("Saved successfully")
    
    # Perform single query
    if args.query:
        results = kb.search(args.query)
        if not results:
            print(f"No results found for '{args.query}'")
        else:
            print(f"\nResults for '{args.query}':\n")
            for rank, (doc_id, score, doc) in enumerate(results, 1):
                print(f"{rank}. {doc['title']} (Score: {score:.4f})")
                print(f"   {doc['content'][:150]}...")
                print()
    
    # Interactive mode
    if args.interactive or (not args.query and not args.save):
        if len(kb.documents) == 0:
            print("No documents in knowledge base. Loading sample data...")
            load_sample_data(kb)
        interactive_search(kb)


if __name__ == '__main__':
    main()
