# knwb - Knowledge Base Search Engine

A simple yet powerful knowledge-based search engine implemented in Python using TF-IDF (Term Frequency-Inverse Document Frequency) ranking.

## Features

- **TF-IDF based search**: Ranks documents based on relevance using industry-standard TF-IDF algorithm
- **Interactive mode**: Search interactively with a command-line interface
- **Persistent storage**: Save and load knowledge bases from JSON files
- **Custom data**: Add your own documents to the knowledge base
- **Sample data**: Includes sample documents for quick testing

## Installation

No external dependencies required! The search engine uses only Python standard library.

```bash
git clone https://github.com/chgokul/knwb.git
cd knwb
```

## Usage

### Interactive Search (Default)

```bash
python search.py
```

This will load sample data and start an interactive search session:

```
=== Knowledge Base Search Engine ===
Type 'quit' or 'exit' to stop

Search: machine learning
```

### Single Query Search

```bash
python search.py --sample-data --query "machine learning"
```

### Using Sample Data

```bash
python search.py --sample-data --interactive
```

### Adding Custom Data

Create a JSON file with your documents:

```json
[
  {
    "title": "Your Document Title",
    "content": "Your document content here..."
  }
]
```

Then load it:

```bash
python search.py --add-data your_data.json --interactive
```

### Saving and Loading Knowledge Base

Save the current knowledge base:

```bash
python search.py --sample-data --save kb.json
```

Load a saved knowledge base:

```bash
python search.py --load kb.json --interactive
```

## How It Works

The search engine uses TF-IDF (Term Frequency-Inverse Document Frequency) to rank documents:

1. **Indexing**: When documents are added, they are tokenized and indexed
2. **TF-IDF Scoring**: 
   - Term Frequency (TF): How often a term appears in a document
   - Inverse Document Frequency (IDF): How rare a term is across all documents
3. **Ranking**: Documents are ranked by their TF-IDF scores for query terms

## API Usage

You can also use the search engine programmatically:

```python
from knowledge_base import KnowledgeBase

# Create a new knowledge base
kb = KnowledgeBase()

# Add documents
kb.add_document(0, "Python Programming", "Python is a high-level language...")
kb.add_document(1, "Machine Learning", "ML is a subset of AI...")

# Search
results = kb.search("python programming", top_k=5)

# Display results
for doc_id, score, doc in results:
    print(f"{doc['title']}: {score:.4f}")

# Save knowledge base
kb.save("my_kb.json")

# Load knowledge base
kb.load("my_kb.json")
```

## Command-Line Options

- `--load <file>`: Load knowledge base from JSON file
- `--save <file>`: Save knowledge base to JSON file
- `--add-data <file>`: Add documents from JSON file
- `--query <text>`: Perform a single search query
- `--interactive`: Start interactive search mode
- `--sample-data`: Load sample data

## Examples

Search for documents about Python:
```bash
python search.py --sample-data --query "python programming"
```

Load custom data and save it:
```bash
python search.py --add-data custom_docs.json --save my_kb.json
```

Load saved knowledge base and search interactively:
```bash
python search.py --load my_kb.json --interactive
```

## License

MIT License