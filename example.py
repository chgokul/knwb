#!/usr/bin/env python3
"""
Example usage of the Knowledge Base Search Engine API.
This demonstrates how to use the search engine programmatically.
"""

from knowledge_base import KnowledgeBase


def main():
    # Create a new knowledge base
    kb = KnowledgeBase()
    
    # Add some documents
    print("Adding documents to knowledge base...")
    kb.add_document(0, "Python Programming", 
                    "Python is a high-level, interpreted programming language known for its simplicity.")
    kb.add_document(1, "Machine Learning", 
                    "Machine learning is a subset of artificial intelligence that enables systems to learn.")
    kb.add_document(2, "Data Science", 
                    "Data science combines statistics, data analysis, and machine learning.")
    kb.add_document(3, "Web Development",
                    "Web development involves creating websites using HTML, CSS, and JavaScript.")
    
    print(f"Added {len(kb.documents)} documents\n")
    
    # Perform searches
    queries = [
        "python programming",
        "machine learning",
        "web development",
        "data analysis"
    ]
    
    for query in queries:
        print(f"Search: '{query}'")
        results = kb.search(query, top_k=3)
        
        if results:
            for rank, (doc_id, score, doc) in enumerate(results, 1):
                print(f"  {rank}. {doc['title']} (Score: {score:.4f})")
        else:
            print("  No results found")
        print()
    
    # Save the knowledge base
    print("Saving knowledge base to 'example_kb.json'...")
    kb.save('example_kb.json')
    
    # Load the knowledge base
    print("Loading knowledge base from 'example_kb.json'...")
    new_kb = KnowledgeBase()
    new_kb.load('example_kb.json')
    
    # Verify it works
    results = new_kb.search("python", top_k=1)
    if results:
        print(f"Verification search for 'python': {results[0][2]['title']}")
    
    print("\nExample completed successfully!")


if __name__ == '__main__':
    main()
