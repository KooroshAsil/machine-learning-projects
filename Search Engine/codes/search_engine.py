import os
import nltk
from nltk.tokenize import word_tokenize
import numpy as np
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk import pos_tag
from sklearn.metrics.pairwise import cosine_similarity


class SearchEngine:
    """
    A basic search engine that preprocesses documents and queries,
    builds a vocabulary, and allows searching based on text similarity.

    Attributes:
        documents (dict): Dictionary of document_name -> document_content.
        cleaned_documents (dict): Preprocessed documents with lemmatization and stopword removal.
        vocabulary (list): List of unique words in the corpus.
        preprocessed_query (str): Query string after preprocessing.
    """

    def __init__(self, documents):
        """
        Initialize the SearchEngine with documents.

        Args:
            documents (dict): A dictionary of document_name -> document_content.
        """
        self.documents = documents
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = stopwords.words("english")
        self.punctuations = list(string.punctuation)
        self.cleaned_documents = {}
        self.vocabulary = []
        self.preprocessed_query = ""
        self.vectorizer = None
        self.tfidf_matrix = None

    def get_wordnet_pos(self, treebank_tag):
        """
        Map POS tag from Treebank tag to WordNet tag for lemmatization.

        Args:
            treebank_tag (str): POS tag from pos_tag (e.g., 'NN', 'VB').

        Returns:
            str: One-letter WordNet POS tag ('a', 'v', 'n', 'r') or 'n' by default.
        """
        if treebank_tag.startswith('J'):
            return 'a'
        elif treebank_tag.startswith('V'):
            return 'v'
        elif treebank_tag.startswith('N'):
            return 'n'
        elif treebank_tag.startswith('R'):
            return 'r'
        else:
            return 'n'

    def preprocess_text(self, text):
        """
        Preprocess text by tokenizing, removing stopwords and punctuations,
        performing POS tagging and lemmatization (with some redundancy to keep original forms).

        Args:
            text (str): Raw text to preprocess.

        Returns:
            list: List of processed tokens with duplicates removed but order preserved.
        """
        tokens = word_tokenize(text.lower())
        tokens = [t for t in tokens if t not in self.stop_words + self.punctuations]
        pos_tags = pos_tag(tokens)

        out_tokens = []
        for word, treebank_pos in pos_tags:
            out_tokens.append(word)
            wn_pos = self.get_wordnet_pos(treebank_pos)
            lemma_pos = self.lemmatizer.lemmatize(word, wn_pos)
            if lemma_pos != word:
                out_tokens.append(lemma_pos)
            lemma_verb = self.lemmatizer.lemmatize(word, 'v')
            if lemma_verb not in (word, lemma_pos):
                out_tokens.append(lemma_verb)

        seen = set()
        final_tokens = []
        for token in out_tokens:
            if token not in seen:
                seen.add(token)
                final_tokens.append(token)

        return final_tokens

    def clean_documents(self):
        """
        Preprocess all documents stored in self.documents.
        Returns cleaned_documents dict.
        """
        if self.cleaned_documents:
            return self.cleaned_documents

        cleaned_docs = {}
        for doc_name, content in self.documents.items():
            cleaned_tokens = self.preprocess_text(content)
            cleaned_docs[doc_name] = " ".join(cleaned_tokens)

        self.cleaned_documents = cleaned_docs
        return cleaned_docs

    def get_all_words(self):
        """
        Extract all unique words from cleaned documents to build the vocabulary.
        Automatically cleans documents if not done yet.

        Returns:
            list: List of unique words in the corpus.
        """
        if not self.cleaned_documents:
            self.clean_documents()

        all_words = list(set(
            word
            for content in self.cleaned_documents.values()
            for word in content.split()
        ))
        self.vocabulary = all_words
        return all_words

    def build_tfidf_matrix(self):
        """
        Build a TF-IDF matrix from the cleaned documents.
        Automatically cleans documents if not done yet.
        """
        if not self.cleaned_documents:
            self.clean_documents()

        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform(list(self.cleaned_documents.values()))

    def search(self, query, top_n=3, threshold=0.0):
        """
        Search for the query in the documents and return top_n results ranked by cosine similarity.
        Automatically builds TF-IDF matrix if not done yet.
        Filters results with similarity scores > threshold.

        Args:
            query (str): The search query.
            top_n (int): Number of top results to return.
            threshold (float): Minimum cosine similarity score to include a result.

        Returns:
            list of tuples: [(doc_name, similarity_score), ...] sorted by score descending.
        """
        if self.tfidf_matrix is None or self.vectorizer is None:
            self.build_tfidf_matrix()

        cleaned_query_tokens = self.preprocess_text(query)
        cleaned_query = " ".join(cleaned_query_tokens)
        query_vec = self.vectorizer.transform([cleaned_query])
        cosine_scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        doc_scores = list(zip(self.cleaned_documents.keys(), cosine_scores))
        filtered_results = [item for item in doc_scores if item[1] > threshold]
        ranked_results = sorted(filtered_results, key=lambda x: x[1], reverse=True)

        return ranked_results[:top_n]
    
folder_path = "./documents"
documents = {}

for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        with open(os.path.join(folder_path, filename), "r", encoding="utf-8") as file:
            content = file.read()
            documents[filename] = content
            
search_engine = SearchEngine(documents)




# --- Your Test Queries ---
queries = [
    # 1. High Relevance - Direct keywords from Doc 1
    "future renewable energy solar wind",
    # 2. High Relevance - Direct keywords from Doc 2
    "mindful living present moment meditation",
    # 3. High Relevance - Direct keywords from Doc 3
    "black holes spacetime general relativity",
    # 4. High Relevance - Direct keywords from Doc 4
    "digital art NFT virtual reality",
    # 5. High Relevance - Direct keywords from Doc 5
    "artificial intelligence societal impact ethics",

    # 6. Lemmatization Test - 'runs' vs 'run', 'changing' vs 'change' related to 'transformation'
    "AI transforming society", # Test 'transforming' -> 'transform' / 'transformation' for Doc 5
    # 7. Stopword/Punctuation Test - Query with many stopwords/punctuation
    "What is the actual impact of the new AI on our society?", # Should still find Doc 5
    # 8. Broad Term - Expect multiple results, possibly ranked
    "technology", # Appears in Doc 1, 4, 5
    # 9. Low Relevance / Shared Terms - Common words that might not be discriminative
    "study history", # Unlikely to be highly relevant to any specific doc, but 'study' might appear.
    # 10. Query with a mix of relevant and irrelevant terms
    "sustainable clean energy with ancient pyramids", # Strong keywords for Doc 1, but irrelevant 'ancient pyramids'
    # 11. Empty query - Should return no results or very low scores
    "",
    # 12. Query with only stopwords
    "to be or not to be", # Should return no results as stopwords are removed
    # 13. Query with non-existent words
    "supercalifragilisticexpialidocious quantum entanglement", # Should yield no results, good for threshold test
    # 14. Test with higher top_n
    "development", # Appears in multiple documents (e.g., 'digital art', 'AI')
    # 15. Test with a high threshold (should filter out most results)
    "meditation", # Should only return Doc 2, possibly others if very close
    # 16. Test with a very specific, unique phrase that exists
    "Event Horizon Telescope M87", # From Doc 3
    # 17. Test capitalization (should be handled by lowercasing)
    "Mindful LiVinG PracticE", # Should match Doc 2
    # 18. Pluralization test (e.g., 'solutions' vs 'solution')
    "energy storage solution", # From Doc 1
    # 19. Verb form test (e.g., 'formed' vs 'form')
    "stars forming black holes", # From Doc 3
    # 20. Query with only punctuations or numbers (should be removed)
    "123!@#$%",
]

if __name__ == "__main__":
    #  Test Queries ---
    queries = [
        # 1. High Relevance - Direct keywords from Doc 1
        "future renewable energy solar wind",
        # 2. High Relevance - Direct keywords from Doc 2
        "mindful living present moment meditation",
        # 3. High Relevance - Direct keywords from Doc 3
        "black holes spacetime general relativity",
        # 4. High Relevance - Direct keywords from Doc 4
        "digital art NFT virtual reality",
        # 5. High Relevance - Direct keywords from Doc 5
        "artificial intelligence societal impact ethics",

        # 6. Lemmatization Test - 'runs' vs 'run', 'changing' vs 'change' related to 'transformation'
        "AI transforming society", # Test 'transforming' -> 'transform' / 'transformation' for Doc 5
        # 7. Stopword/Punctuation Test - Query with many stopwords/punctuation
        "What is the actual impact of the new AI on our society?", # Should still find Doc 5
        # 8. Broad Term - Expect multiple results, possibly ranked
        "technology", # Appears in Doc 1, 4, 5
        # 9. Low Relevance / Shared Terms - Common words that might not be discriminative
        "study history", # Unlikely to be highly relevant to any specific doc, but 'study' might appear.
        # 10. Query with a mix of relevant and irrelevant terms
        "sustainable clean energy with ancient pyramids", # Strong keywords for Doc 1, but irrelevant 'ancient pyramids'
        # 11. Empty query - Should return no results or very low scores
        "",
        # 12. Query with only stopwords
        "to be or not to be", # Should return no results as stopwords are removed
        # 13. Query with non-existent words
        "supercalifragilisticexpialidocious quantum entanglement", # Should yield no results, good for threshold test
        # 14. Test with higher top_n
        "development", # Appears in multiple documents (e.g., 'digital art', 'AI')
        # 15. Test with a high threshold (should filter out most results)
        "meditation", # Should only return Doc 2, possibly others if very close
        # 16. Test with a very specific, unique phrase that exists
        "Event Horizon Telescope M87", # From Doc 3
        # 17. Test capitalization (should be handled by lowercasing)
        "Mindful LiVinG PracticE", # Should match Doc 2
        # 18. Pluralization test (e.g., 'solutions' vs 'solution')
        "energy storage solution", # From Doc 1
        # 19. Verb form test (e.g., 'formed' vs 'form')
        "stars forming black holes", # From Doc 3
        # 20. Query with only punctuations or numbers (should be removed)
        "123!@#$%",
    ]

    # --- Run the queries ---
    print("\n--- Running Test Queries ---")
    for i, query in enumerate(queries):
        print(f"\n--- Query {i+1}: '{query}' ---")
        
        # Default parameters for search. You can modify these for specific tests.
        top_n_param = 3
        threshold_param = 0.0

        # Adjust parameters for specific test cases if needed (e.g., for empty/irrelevant queries)
        if query in ["", " ", "to be or not to be", "supercalifragilisticexpialidocious quantum entanglement", "123!@#$%"]:
            top_n_param = 5 # Show more to confirm low scores
            threshold_param = 0.1 # A small threshold to likely filter them out

        # For the specific threshold test
        if query == "meditation":
            top_n_param = 5
            threshold_param = 0.2

        try:
            results = search_engine.search(query, top_n=top_n_param, threshold=threshold_param)
            if results:
                for doc_name, score in results:
                    print(f"  - Document: {doc_name}, Score: {score:.4f}")
            else:
                print("  No results found above the specified threshold.")
        except Exception as e:
            print(f"  An error occurred: {e}")

    print("\n--- All Test Queries Completed ---")