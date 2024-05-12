from google.cloud import aiplatform
from langchain_google_vertexai import (
    VectorSearchVectorStore,
    VectorSearchVectorStoreDatastore,
    VertexAIEmbeddings,
)
from langchain_community.document_loaders import SeleniumURLLoader
from google.cloud import storage

PROJECT_ID = "lumibakalaurs"
REGION = "europe-west3"
BUCKET = "lumivectorembeddingstorage"
BUCKET_URI = f"gs://{BUCKET}"

def deleteBlob(_):
    bucket_name = "lumivectorembeddingstorage"

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blobs = bucket.list_blobs(prefix='documents/')
    for blob in blobs:
        blob.delete()

    print("Folder deleted.")
    
    createEmbeddingStore()

    return 'OK'

def createEmbeddingStore():

    aiplatform.init(project=PROJECT_ID, location=REGION, staging_bucket=BUCKET_URI)
    embedding_model = VertexAIEmbeddings(model_name="textembedding-gecko@latest")
    
    my_index = aiplatform.MatchingEngineIndex("4563061216200622080", location=REGION)
    my_index_endpoint = aiplatform.MatchingEngineIndexEndpoint("4008133299615563776", location=REGION)

    urls = ["https://www.lu.lv/studijas/studiju-celvedis/akademiskais-kalendars/2023/2024-akademiska-gada-kalendars/",
            "https://www.lu.lv/studijas/studiju-programmas/bakalaura-limena-studijas/datorzinatnes/",
            "https://www.lu.lv/studijas/studiju-programmas/bakalaura-limena-studijas/farmacija/"]

    loader = SeleniumURLLoader(urls=urls)
    documents = loader.load()
    docs = []
    for d in documents:
        docs += [d.page_content]

    # Create a Vector Store
    vector_store = VectorSearchVectorStore.from_components(
        project_id=PROJECT_ID,
        region=REGION,
        gcs_bucket_name=BUCKET,
        index_id=my_index.name,
        endpoint_id=my_index_endpoint.name,
        embedding=embedding_model,
        stream_update=True,
    )

    # Add vectors and mapped text chunks to your vectore store
    vector_store.add_texts(texts=docs)