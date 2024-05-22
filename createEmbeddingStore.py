from google.cloud import discoveryengine, storage
from langchain_google_vertexai import (
    VectorSearchVectorStore,
    VectorSearchVectorStoreDatastore,
    VertexAIEmbeddings,
)
from langchain_community.document_loaders import SeleniumURLLoader
from google.api_core.client_options import ClientOptions
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from bs4 import BeautifulSoup as Soup

PROJECT_ID = "lumibakalaurs"
REGION = "europe-west3"
BUCKET = "lumivectorembeddingstorage"
BUCKET_URI = f"gs://{BUCKET}"
STORAGE = storage.Client()
DATASTORE = "lumi_1715330343731"
DOCUMENT_FOLDER=f"gs://{BUCKET}/documents/*.txt"

def createEmbeddingStore(_):

    exclude_dirs=["https://www.lu.lv/en/", "https://www.lu.lv/par-mums/lu-mediji/zinas/zina/t/", "https://www.lu.lv/muzejs/par-mums/zinas/zina/"]

    url = "https://www.lu.lv/studijas/studiju-programmas/"

    url_loader = RecursiveUrlLoader(
        url=url, 
        max_depth=15, 
        extractor=lambda x: Soup(x, "html.parser").text, 
        exclude_dirs=exclude_dirs
    )
    urls=[]
    for i in url_loader.lazy_load():
        urls += [i.metadata["source"]]

    url = "https://www.lu.lv"

    url_loader = RecursiveUrlLoader(
        url=url, 
        max_depth=5, 
        extractor=lambda x: Soup(x, "html.parser").text, 
        exclude_dirs=exclude_dirs
    )

    for i in url_loader.lazy_load():
        urls += [i.metadata["source"]]
        
    urls = list(dict.fromkeys(urls))
    
    urls = [x for x in urls if ".css" not in x]
    urls = [x for x in urls if "+371" not in x]

    loader = SeleniumURLLoader(urls=urls)
    documents = loader.load()

    deleteBlob()

    bucket = STORAGE.bucket(BUCKET)
    blob = bucket.blob("documents/")
    blob.upload_from_string("")

    index = 0

    for d in documents:

        title = d.metadata["title"].replace("/", " ")
        blob = bucket.blob(f"documents/{title}_{index}.txt")

        index = index + 1

        blob.upload_from_string(data=d.page_content + d.metadata["source"] + d.metadata["title"], content_type='text/plain; charset=utf-8')

    print("Documents stored!")

    importFilesToAgent()

    return "OK"

def deleteBlob():
    bucket_name = BUCKET
    bucket = STORAGE.get_bucket(bucket_name)
    blobs = bucket.list_blobs(prefix="documents/")
    for blob in blobs:
        blob.delete()
    print("Folder deleted.")

def importFilesToAgent():
    client_options = (
        ClientOptions(api_endpoint="global-discoveryengine.googleapis.com")
    )

    client = discoveryengine.DocumentServiceClient(client_options=client_options)

    parent = client.branch_path(
        project=PROJECT_ID,
        location="global",
        data_store=DATASTORE,
        branch="default_branch",
    )

    request = discoveryengine.ImportDocumentsRequest(
        parent=parent,
        gcs_source=discoveryengine.GcsSource(
            input_uris=[DOCUMENT_FOLDER], data_schema="content"
        ),
        reconciliation_mode=discoveryengine.ImportDocumentsRequest.ReconciliationMode.FULL,
    )

    operation = client.import_documents(request=request)

    print(f"Waiting for operation to complete: {operation.operation.name}")
    response = operation.result()

    metadata = discoveryengine.ImportDocumentsMetadata(operation.metadata)

    print(response)
    print(metadata)

    print("Documents imported!")