# Imports the Google Cloud client library
from google.cloud import storage
from vertexai.language_models import TextEmbeddingModel
from langchain_community.document_loaders import SeleniumURLLoader
from langchain_text_splitters import CharacterTextSplitter


def createEmbeddingStore():
    
    # Instantiates a client
    storage_client = storage.Client()

    urls = ["https://www.lu.lv/studijas/studiju-celvedis/akademiskais-kalendars/2023/2024-akademiska-gada-kalendars/", 
                "https://www.lu.lv/studijas/studiju-programmas/bakalaura-limena-studijas/datorzinatnes/",
                "https://www.lu.lv/studijas/studiju-programmas/bakalaura-limena-studijas/farmacija/"]
    
    loader = SeleniumURLLoader(urls=urls)
    documents = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    bucket = storage_client.bucket('lumiembeddingstorage')
    blob = bucket.blob('embeddings.json')

    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
    embeddings = model.get_embeddings([docs])
    
    with open(embeddings, 'rb') as f:
        blob.upload_from_file(f)