# Imports the Google Cloud client library
from vertexai.language_models import TextEmbeddingModel
from langchain_community.document_loaders import SeleniumURLLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_google_alloydb_pg import AlloyDBEngine
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_google_alloydb_pg import AlloyDBVectorStore
import uuid

PROJECT_ID = "lumibakalaurs"  # @param {type:"string"}
REGION = "europe-north1"  # @param {type: "string"}
CLUSTER = "lumicluster"  # @param {type: "string"}
INSTANCE = "lumibachelortest3"  # @param {type: "string"}
DATABASE = "postgres"  # @param {type: "string"}
TABLE_NAME = "vectorembeddings"  # @param {type: "string"}

def createEmbeddingStore(_):

    urls = ["https://www.lu.lv/studijas/studiju-celvedis/akademiskais-kalendars/2023/2024-akademiska-gada-kalendars/", 
                "https://www.lu.lv/studijas/studiju-programmas/bakalaura-limena-studijas/datorzinatnes/",
                "https://www.lu.lv/studijas/studiju-programmas/bakalaura-limena-studijas/farmacija/"]
    
    loader = SeleniumURLLoader(urls=urls)
    documents = loader.load()
    docs = []
    for d in documents:
        docs += [d.page_content]

    # text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    # docs = text_splitter.split_documents(docs1)

    engine = AlloyDBEngine.from_instance(
        project_id=PROJECT_ID,
        region=REGION,
        cluster=CLUSTER,
        instance=INSTANCE,
        database=DATABASE,
    )

    engine.init_vectorstore_table(
        table_name=TABLE_NAME,
        vector_size=768,  # Vector size for VertexAI model(textembedding-gecko@latest)
    )

    embedding = VertexAIEmbeddings(
        model_name="textembedding-gecko@latest", project=PROJECT_ID
    )

    store = AlloyDBVectorStore.create(
        engine=engine,
        table_name=TABLE_NAME,
        embedding_service=embedding,
    )

    metadatas = [{"len": len(t)} for t in docs]
    ids = [str(uuid.uuid4()) for _ in docs]

    store.add_texts(docs, metadatas=metadatas, ids=ids)