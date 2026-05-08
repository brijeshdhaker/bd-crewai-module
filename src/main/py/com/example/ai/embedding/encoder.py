from sentence_transformers import SentenceTransformer
from com.example.ai.loader.pdf_loader import extract_text_from_pdf

# Load the pre-trained sentence transformer model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Load your text data (e.g., from a file or database)
documents = load_text_data()

# Generate vector embeddings for the documents
document_embeddings = model.encode(documents)