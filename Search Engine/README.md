<!-- README for Agora Search Engine -->

<div align="center">
  <h1 style="font-family: 'Helvetica Neue', sans-serif; font-size: 3em; color: #1a73e8;">🔍 <strong>Agora</strong> Search Engine 🚀</h1>
  <p style="font-size: 1.2em; color: #555;">A lightweight, modular document search application built in Python</p>
</div>

---

## 📖 Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Architecture](#architecture)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Code Walkthrough](#code-walkthrough)
7. [Configuration](#configuration)
8. [Contributing](#contributing)
9. [License](#license)

---

## 🏁 Introduction

**Agora** is a desktop-based search engine designed to index and search plain-text documents with ease. Developed in Python and packaged with a graphical user interface (GUI) using Tkinter, Agora enables users to run fast, local searches over large collections of `.txt` files. Whether you are managing research notes, technical documentation, or personal knowledge bases, Agora offers relevance scoring, snippet generation, and a customizable interface to streamline your workflow.

**Objectives:**

* Provide a simple installation and setup process
* Deliver rapid, accurate search results
* Support extensibility for custom scoring or indexing strategies
* Offer a clean, user-friendly GUI for all major operating systems

---

## 🌟 Features

* **Document Indexing**: Automatically loads and indexes `.txt` files from a `documents/` folder.
* **Relevance Scoring**: Uses TF–IDF vectorization and cosine similarity to rank results.
* **Snippet Highlighting**: Displays query terms in context within each result.
* **Modular Design**: Separate modules for indexing/search (`search_engine.py`) and GUI (`main.py`, `gui.py`).
* **Cross-Platform GUI**: Built with Tkinter; runs on Windows, macOS, and Linux.
* **Customizable Parameters**: Tweak threshold and top-N results via simple function parameters.

---

## 🏗️ Architecture

![sample](https://github.com/user-attachments/assets/bffc9018-552a-4df2-ae79-ddef5c54f867)

### 1. Document Loader

* Scans the `documents/` directory
* Reads each `.txt` file into memory as a string
* Stores file paths and text in a dictionary

### 2. Search Engine Module (`search_engine.py`)

Responsible for indexing and querying:

* **Initialization**:

  * Builds a document-term matrix using TF–IDF
  * Computes IDF values for all terms
* **Search Method** (`search(query, threshold, top_n)`):

  1. Tokenizes and vectorizes the query
  2. Computes cosine similarity scores against all document vectors
  3. Filters out scores below `threshold`
  4. Sorts and returns the top `top_n` results with snippets

### 3. GUI Module (`main.py` & `gui.py`)

Presents the application window and handles events:

* **Main Script** (`main.py`):

  * Loads documents, instantiates `SearchEngine`
  * Initializes Tkinter root and launches `AgoraGUI`

* **GUI Class** (`AgoraGUI` in `gui.py`):

  * Sets window title, size, and styling
  * Creates search bar (`Entry` + `Button`) and result container (`Canvas` + `Scrollbar`)
  * Defines event handlers for user input and result rendering

---

## ⚙️ Installation

To get started with Agora:

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/agora-search-engine.git

# 2. Navigate into project directory
cd agora-search-engine

# 3. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Add your text documents
mkdir documents
# Copy your .txt files into the 'documents/' folder
```

---

## 💻 Usage

Once installed:

1. **Start the application**:

   ```bash
   python main.py
   ```
2. **Perform a search**:

   * Enter your keywords in the search bar
   * Press <kbd>Enter</kbd> or click the 🔍 **Search** button
3. **Review results**:

   * **Filename**: Name of the matching document
   * **Score**: Relevance value (0–1 scale)
   * **Snippet**: Contextual preview with highlighted terms

<details>
<summary>🔧 Advanced Options</summary>

* **Threshold**: Default is `0.1`; raise to filter weak matches.
* **Top-N**: Default is `10`; modify to show more or fewer results.
* **Styling**: Edit font, color, and layout settings in `gui.py`.

</details>

---

## 📂 Code Walkthrough

Below is a high-level view of the key files and their responsibilities.

### `search_engine.py`

```python
from typing import Dict, List, Tuple

class SearchEngine:
    def __init__(self, documents: Dict[str, str]):
        """Prepare TF–IDF matrix and document vectors."""
        # 1. Tokenize texts and compute term frequencies
        # 2. Calculate IDF for each term
        # 3. Build TF–IDF matrix

    def search(
        self,
        query: str,
        threshold: float = 0.1,
        top_n: int = 10
    ) -> List[Tuple[str, float, str]]:
        """
        Returns a list of (filename, score, snippet) for matching documents.
        """
        # 1. Vectorize query
        # 2. Compute cosine similarities
        # 3. Filter and sort
        # 4. Generate snippets
```

---

### `main.py`

```python
import os, glob
import tkinter as tk
from search_engine import SearchEngine
from gui import AgoraGUI

if __name__ == "__main__":
    # Load documents
    files = glob.glob(os.path.join("documents", "*.txt"))
    documents = {os.path.basename(f): open(f).read() for f in files}

    # Initialize engine and GUI
    engine = SearchEngine(documents)
    root = tk.Tk()
    app = AgoraGUI(root, engine)
    root.mainloop()
```

---

### `gui.py`

```python
import tkinter as tk
from tkinter import ttk

class AgoraGUI:
    def __init__(self, master, search_engine):
        self.master = master
        self.engine = search_engine
        self._setup_window()
        self._build_widgets()

    def _setup_window(self):
        master.title("Agora Search Engine")
        master.geometry("800x600")
        # Additional styling...

    def _build_widgets(self):
        # Search bar frame
        # Results canvas and scrollbar
        # Event bindings

    def _on_search(self):
        query = self.search_var.get()
        results = self.engine.search(query)
        self._display_results(results)

    def _display_results(self, results):
        # Clear old results
        # For each (filename, score, snippet): render a frame
```

---

## ⚙️ Configuration

Adjust parameters and styles to suit your needs:

| Setting       | Location           | Description                             |
| ------------- | ------------------ | --------------------------------------- |
| `threshold`   | `search_engine.py` | Minimum similarity score (0–1)          |
| `top_n`       | `main.py`          | Number of results to display            |
| `font_family` | `gui.py`           | Text font for labels and buttons        |
| `color_theme` | `gui.py`           | HEX codes for background and highlights |

Example: To change `threshold` to `0.2`, update:

```python
results = engine.search(query, threshold=0.2, top_n=10)
```

---

## 🤝 Contributing

We welcome contributions of all sizes! Please:

1. **Fork** the repository
2. **Branch**: `git checkout -b feature/YourFeature`
3. **Commit**: `git commit -m "Add feature"`
4. **Push**: `git push origin feature/YourFeature`
5. **Create** a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on coding style, testing, and more.

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for full terms.

---

<p align="center">Made with ❤️ by <strong>Your Name</strong></p>
