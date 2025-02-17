from langchain.document_loaders import PyPDFLoader , DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings

#Extract Data from the PDF file
# Tabine: Edit| Test | Explain | Document | Ask
def load_pdf_file(data):
    loader= DirectoryLoader(data,
                            glob="*.pdf",
                            loader_cls=PyPDFLoader,)
    documents=loader.load()
    return documents

#split the data into text Chunks
# Tabine: Edit| Test | Explain | Document | Ask
def text_split(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=100)
    text_chunks = text_splitter.split_documents(extracted_data)
    return text_chunks

# download the  embeddings from hugging face
# Tabine: Edit| Test | Explain | Document | Ask
def download_hugging_face_embeddings():
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    return embeddings