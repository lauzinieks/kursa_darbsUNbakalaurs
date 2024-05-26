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

PROJECT_ID = "lumibakalaurs" # katram projektam atšķirīgs, projekta ID
BUCKET = "lumi_text_document_bucket" # katram projektam atšķirīgs, glabātuves nosaukums
STORAGE = storage.Client()
DATASTORE = "lumi_1715330343731" # katram projektam atšķirīgs, atrodams pie produkta "Agent Builder", kā izveidotā aģenta ID
DOCUMENT_FOLDER=f"gs://{BUCKET}/documents/*.txt"

def deleteBlob():
    bucket_name = BUCKET
    bucket = STORAGE.get_bucket(bucket_name) # iegūst glabātuvi
    blobs = bucket.list_blobs(prefix="documents/") # iegūst glabātuves mapi, kurā atrodas dokumenti
    for blob in blobs:
        blob.delete() # no mapes izdzēš visus tajā esošos dokumentus
    print("Folder deleted!")

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
    ) # iegūst aģentu

    request = discoveryengine.ImportDocumentsRequest(
        parent=parent,
        gcs_source=discoveryengine.GcsSource(
            input_uris=[DOCUMENT_FOLDER], data_schema="content"
        ),
        reconciliation_mode=discoveryengine.ImportDocumentsRequest.ReconciliationMode.FULL,
    ) # dokumentus no glabātuvs importē aģentam

    operation = client.import_documents(request=request)

    print(f"Waiting for operation to complete: {operation.operation.name}")
    response = operation.result()

    metadata = discoveryengine.ImportDocumentsMetadata(operation.metadata)

    print(response)
    print(metadata)

    print("Documents imported!")

def createEmbeddingStore(_):

    exclude_dirs=["https://www.lu.lv/en/", "https://www.lu.lv/par-mums/lu-mediji/zinas/zina/t/", "https://www.lu.lv/muzejs/par-mums/zinas/zina/"] # norāda, kuras lapas, ja tās sākas ar šau URL, neiekļaut sarakstā

    url = "https://www.lu.lv/studijas/studiju-programmas/" # sākuma lapa

    url_loader = RecursiveUrlLoader(
        url=url, 
        max_depth=15,
        extractor=lambda x: Soup(x, "html.parser").text, 
        exclude_dirs=exclude_dirs
    )  # max_depth - norāda cik "dziļi" rāpulis meklēs saistītās lapas no sākuma lapas
    urls=[]
    for i in url_loader.lazy_load(): # lazy_load nodrošina, ka ciklā, no saraksta, pārādīsies lapu URL, kas samazina apstrādes laiku
        urls += [i.metadata["source"]] # pievieno sarakstam URL no kurām jāiegūst tekstu

    url = "https://www.lu.lv" # sākuma lapa

    url_loader = RecursiveUrlLoader(
        url=url, 
        max_depth=5,
        extractor=lambda x: Soup(x, "html.parser").text, 
        exclude_dirs=exclude_dirs
    )  # max_depth - norāda cik "dziļi" rāpulis meklēs saistītās lapas no sākuma lapas

    for i in url_loader.lazy_load(): # lazy_load nodrošina, ka ciklā, no saraksta, pārādīsies lapu URL, kas samazina apstrādes laiku
        urls += [i.metadata["source"]] # pievieno sarakstam URL no kurām jāiegūst tekstu
        
    urls = list(dict.fromkeys(urls)) # izdzēš no URL saraksta duplikātus
    
    urls = [x for x in urls if ".css" not in x] # izdzēš no URL saraksta css lapas
    urls = [x for x in urls if "+371" not in x] # izdzēš no URL saraksta lapas, kuras satur telefona numurus
    urls = [x for x in urls if "-en" not in x] # izdzēš no URL saraksta lapas, kuras satur angļu valodas programmas

    loader = SeleniumURLLoader(urls=urls) # iegūst tekstu no lapām
    documents = loader.load()

    deleteBlob()

    bucket = STORAGE.bucket(BUCKET) # iegūst glabātuvi
    blob = bucket.blob("documents/") # iegūst glabātuves mapi kurā saglabāt dokumentus
    blob.upload_from_string("")

    index = 0 # izmantos, lai lapas ar vienādiem nosaukumiem nepārrakstītu pāri

    for d in documents:

        title = d.metadata["title"].replace("/", " ") # no izgūtās lapas informācijas iegūtās lapas nosaukuma "/" aizvieto ar " ", lai mapē "documents" neizveidotu vēl mapes
        blob = bucket.blob(f"documents/{title}_{index}.txt")

        index = index + 1

        blob.upload_from_string(data=d.page_content + d.metadata["source"] + d.metadata["title"], content_type='text/plain; charset=utf-8') # saglabā jaunu dokumentu glabātuvē

    print("Documents stored!")

    importFilesToAgent()

    return "OK"