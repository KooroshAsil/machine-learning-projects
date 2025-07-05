import os
import tkinter as tk
from tkinter import ttk
from search_engine import SearchEngine

class AgoraGUI:
    """
    A Tkinter-based GUI for the Agora search engine.

    Attributes:
        master (tk.Tk): The root window of the application.
        search_engine (SearchEngine): An instance of the search engine to perform searches.
    """
    def __init__(self, master, search_engine):
        """
        Initialize the GUI with a search bar, logo, and results display area.

        Args:
            master (tk.Tk): The root Tkinter window.
            search_engine (SearchEngine): The search engine instance for querying documents.
        """
        self.master = master
        self.search_engine = search_engine
        master.title("Agora")
        master.geometry("820x740")
        master.configure(bg="#f5f5f5")

        header_frame = tk.Frame(master, bg="#ffffff")
        header_frame.pack(fill=tk.X, pady=(20, 0))

        logo_canvas = tk.Canvas(header_frame, width=400, height=80, bg="#ffffff", highlightthickness=0)
        logo_canvas.pack(pady=(10, 0))
        logo_canvas.create_text(204, 42, text="AGORA", font=("Times New Roman", 60, "bold"), fill="#bbbbbb")
        logo_canvas.create_text(200, 40, text="AGORA", font=("Times New Roman", 60, "bold"), fill="#4285F4")

        underline = tk.Frame(header_frame, bg="#4285F4", height=4)
        underline.pack(fill=tk.X, padx=200, pady=(0, 20))

        self.search_frame = tk.Frame(master, bg="#f5f5f5")
        self.search_frame.pack(pady=20)

        style = ttk.Style()
        style.theme_use('default')
        style.configure(
            "Custom.TEntry",
            padding=8,
            relief="flat",
            fieldbackground="#ffffff",
            background="#ffffff",
            bordercolor="#4285F4",
            lightcolor="#4285F4",
            darkcolor="#4285F4"
        )
        style.configure(
            "Custom.TButton",
            font=("Arial", 12),
            padding=6,
            relief="flat",
            background="#4285F4",
            foreground="#ffffff"
        )
        style.map(
            "Custom.TButton",
            background=[('active', '#3367D6')]
        )

        self.query_var = tk.StringVar()
        self.search_entry = ttk.Entry(
            self.search_frame,
            textvariable=self.query_var,
            width=60,
            style="Custom.TEntry"
        )
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.search_entry.bind('<Return>', self.on_search)

        self.search_button = ttk.Button(
            self.search_frame,
            text="🔍 Search",
            command=self.on_search,
            style="Custom.TButton"
        )
        self.search_button.pack(side=tk.LEFT)

        container = tk.Frame(master, bg="#f5f5f5")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        self.canvas = tk.Canvas(container, bg="#f5f5f5", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.results_container = tk.Frame(self.canvas, bg="#f5f5f5")

        self.results_container.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.results_container, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def extract_snippet(self, content, query_tokens, window=100):
        """
        Extract a snippet of text around the first occurrence of any query token.

        Args:
            content (str): The document text.
            query_tokens (list[str]): The list of preprocessed query tokens.
            window (int): Number of characters to include before and after the match.

        Returns:
            str: A text snippet with ellipses indicating trimmed context.
        """
        lower_content = content.lower()
        for token in query_tokens:
            idx = lower_content.find(token.lower())
            if idx != -1:
                start = max(0, idx - window)
                end = min(len(content), idx + len(token) + window)
                snippet = content[start:end].replace("\n", " ")
                if start > 0:
                    snippet = "..." + snippet
                if end < len(content):
                    snippet += "..."
                return snippet
        snippet = content[:window*2].replace("\n", " ")
        return snippet + ("..." if len(content) > window*2 else "")

    def clear_results(self):
        """
        Remove all widgets from the results container.
        """
        for widget in self.results_container.winfo_children():
            widget.destroy()

    def on_search(self, event=None):
        """
        Handle the search action: process query, perform search, and display results.

        Args:
            event: Optional Tkinter event (e.g., pressing Enter key).
        """
        query = self.query_var.get().strip()
        self.clear_results()
        if not query:
            tk.Label(self.results_container, text="Please enter a search query.", font=("Arial", 14), fg="#777777", bg="#f5f5f5").pack(pady=20)
            return

        query_tokens = self.search_engine.preprocess_text(query)
        try:
            results = self.search_engine.search(query, top_n=10, threshold=0.0)
        except Exception as e:
            tk.Label(self.results_container, text=f"Search error: {e}", font=("Arial", 14), fg="#D93025", bg="#f5f5f5").pack(pady=20)
            return

        if not results:
            tk.Label(self.results_container, text="No results found.", font=("Arial", 14), fg="#777777", bg="#f5f5f5").pack(pady=20)
            return

        base_bg = "#ffffff"
        alt_bg = "#fafafa"
        purple = "#8E24AA"
        for idx, (doc_name, score) in enumerate(results, start=1):
            frame_bg = base_bg if idx % 2 else alt_bg
            frame = tk.Frame(self.results_container, bg=frame_bg, bd=1, relief="solid")
            frame.pack(fill=tk.X, padx=10, pady=6)

            title = tk.Label(frame, text=f"{idx}. {doc_name}", font=("Times New Roman", 17, "bold"), fg="#1a0dab", bg=frame_bg, cursor="hand2")
            title.pack(anchor="w", padx=12, pady=(10,0))

            accent = tk.Frame(frame, bg=purple, height=3)
            accent.pack(fill=tk.X, padx=12, pady=(0,8))

            tk.Label(frame, text=f"Relevance: {score:.3f}", font=("Arial", 10, "italic"), fg=purple, bg=frame_bg).pack(anchor="w", padx=12)

            snippet = self.extract_snippet(self.search_engine.documents.get(doc_name, ""), query_tokens)
            tk.Label(frame, text=snippet, font=("Arial", 13), fg="#3c4043", bg=frame_bg, wraplength=760, justify="left").pack(anchor="w", padx=12, pady=(6,12))

if __name__ == "__main__":
    folder_path = os.path.join(os.path.dirname(__file__), "documents")
    documents = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), encoding="utf-8") as f:
                documents[filename] = f.read()

    search_engine = SearchEngine(documents)
    root = tk.Tk()
    app = AgoraGUI(root, search_engine)
    root.mainloop()
