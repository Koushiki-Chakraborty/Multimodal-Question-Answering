import os
import json
import warnings
from dotenv import load_dotenv
from converter import pdf_to_json

# Load environment variables from .env file
load_dotenv()

# RAG Libraries
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import FAISS 
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_groq import ChatGroq
except ImportError as e:
    print(f"CRITICAL ERROR: Missing required dependencies. Error: {e}")
    print("Please run: pip install -r requirements.txt")
    exit(1)

# Suppress Pydantic V1 compatibility warnings typical in current LangChain versions
warnings.filterwarnings("ignore", category=UserWarning, module="langchain_core")
warnings.filterwarnings("ignore", category=DeprecationWarning)

def setup_rag(json_path):
    print("Loading data...")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Extract metadata for prompt
    metadata = {
        "title": data.get('title', 'Unknown Title'),
        "authors": ", ".join(data.get('authors', [])) or "Unknown Authors",
        "abstract": data.get('abstract', 'No Abstract Available')
    }

    # Prepare text chunks
    text_chunks = []
    
    # Add abstract as the first chunk
    if data.get('abstract'):
        text_chunks.append(f"ABSTRACT: {data['abstract']}")

    for section in data['sections']:
        # Format: "SECTION NAME: content..."
        content = f"SECTION {section['heading']}: {section['content']}"
        text_chunks.append(content)

    # Splitter for better granularity
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.create_documents(text_chunks)

    print("Embedding data (Running locally, this might take a moment)...")
    # Uses a free, high-performance local model
    embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Create Vector Store (FAISS)
    db = FAISS.from_documents(docs, embedding_function)
    
    return db, metadata

def query_rag(db, metadata, query, client):
    # 1. Retrieve
    # k=3 means get the top 3 most relevant chunks
    results = db.similarity_search(query, k=3)
    context_text = "\n\n---\n\n".join([doc.page_content for doc in results])

    # 2. Generate
    prompt_template = ChatPromptTemplate.from_template("""
    You are an expert research assistant analysing the following paper:
    
    Title: {title}
    Authors: {authors}
    
    Abstract: {abstract}
    
    Relevant Context from the paper:
    <context>
    {context}
    </context>
    
    Question: {question}
    
    Answer the question based strictly on the context provided above. 
    The output MUST NOT be in Markdown format(you can use numberings or points but not markdown formatting like **bold** or *italic*).
    

    """)

    prompt = prompt_template.format(
        title=metadata['title'],
        authors=metadata['authors'],
        abstract=metadata['abstract'],
        context=context_text, 
        question=query
    )
    
    response = client.invoke(prompt)
    return response.content, results

def main():
    print("=== Research Paper RAG CLI (FAISS Edition) ===")
    
    # Configuration
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        api_key = input("Enter your Groq API Key: ")
    
    # Source Directory Management
    source_dir = "source"
    data_dir = "data"
    
    if not os.path.exists(source_dir):
        os.makedirs(source_dir)
        print(f"\n[Created '{source_dir}' folder]")
        print(f"Please place your PDF files in the '{source_dir}' folder and run this script again.")
        return

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # List PDFs
    pdf_files = [f for f in os.listdir(source_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"\nNo PDF files found in '{source_dir}' folder.")
        print(f"Please add some PDF files and try again.")
        return

    print(f"\nFound {len(pdf_files)} PDF(s) in '{source_dir}':")
    for i, f in enumerate(pdf_files):
        print(f"{i+1}. {f}")
    
    selected_pdf = None
    while True:
        try:
            choice = input(f"\nSelect a file (1-{len(pdf_files)}) or 'q' to quit: ")
            if choice.lower() in ['q', 'quit', 'exit']:
                return
            
            idx = int(choice) - 1
            if 0 <= idx < len(pdf_files):
                selected_pdf = pdf_files[idx]
                break
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a number.")

    pdf_path = os.path.join(source_dir, selected_pdf)
    
    # Create unique JSON path in data/ folder
    base_name = os.path.splitext(selected_pdf)[0]
    json_path = os.path.join(data_dir, f"{base_name}_data.json")
    
    # Check if JSON already exists to save time
    if os.path.exists(json_path):
        print(f"\nFound existing extracted data for '{selected_pdf}'.")
        print("Using cached data...")
    else:
        try:
            print(f"\nConverting '{selected_pdf}' to JSON using GROBID...")
            pdf_to_json(pdf_path, json_path)
        except Exception as e:
            print(f"Error connecting to GROBID: {e}")
            print("Make sure Docker is running: docker-compose up -d")
            return

    # Setup RAG
    try:
        db, metadata = setup_rag(json_path)
    except Exception as e:
        print(f"Error setting up RAG index: {e}")
        return
        
    llm = ChatGroq(temperature=0, groq_api_key=api_key, model_name="openai/gpt-oss-120b")

    print(f"\nSystem Ready! Ask questions about '{selected_pdf}'. (Type 'exit' to quit)")
    
    while True:
        query = input("\nQuery: ")
        if query.lower() in ['exit', 'quit']:
            break
        
        try:
            answer, sources = query_rag(db, metadata, query, llm)
            print(f"\n>> ANSWER:\n{answer}")
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()