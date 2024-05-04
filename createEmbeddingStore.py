from vertexai.language_models import TextEmbeddingModel
from langchain_community.document_loaders import SeleniumURLLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_google_alloydb_pg import AlloyDBEngine
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_google_alloydb_pg import AlloyDBVectorStore
import uuid
from google.cloud.alloydb.connector import Connector
import sqlalchemy
from flask import Flask, jsonify, request, make_response
import asyncio

PROJECT_ID = "lumibakalaurs"
REGION = "europe-north1"
CLUSTER = "lumicluster"
INSTANCE = "lumibachelortest3"
DATABASE = "postgres"
TABLE_NAME = "vectorembeddings"

app = Flask(__name__)
loop = asyncio.get_event_loop()

async def start(request):
    try:
        result = await createEmbeddingStore()
        return make_response(jsonify({'message': result}), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

@app.route('/route', methods=['GET'])
def route(_):
    return asyncio.run_coroutine_threadsafe(start(request), loop).result()

if __name__ == "__main__":
    app.run()

async def createEmbeddingStore():
    connector = Connector()

    pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
    )

    urls = ["https://www.lu.lv/studijas/studiju-celvedis/akademiskais-kalendars/2023/2024-akademiska-gada-kalendars/",
            "https://www.lu.lv/studijas/studiju-programmas/bakalaura-limena-studijas/datorzinatnes/",
            "https://www.lu.lv/studijas/studiju-programmas/bakalaura-limena-studijas/farmacija/"]

    loader = SeleniumURLLoader(urls=urls)
    documents = loader.load()
    docs = []
    for d in documents:
        docs += [d.page_content]

    engine = AlloyDBEngine.from_instance(
        project_id=PROJECT_ID,
        region=REGION,
        cluster=CLUSTER,
        instance=INSTANCE,
        database=DATABASE,
        user="username",
        password="password",
    )

    await engine.drop_table(TABLE_NAME)

    engine.init_vectorstore_table(
        table_name=TABLE_NAME,
        vector_size=768,
    )

    embedding = VertexAIEmbeddings(
        model_name="textembedding-gecko@latest", project=PROJECT_ID
    )

    store = await AlloyDBVectorStore.create(
        engine=engine,
        table_name=TABLE_NAME,
        embedding_service=embedding,
    )

    metadatas = [{"len": len(t)} for t in docs]
    ids = [str(uuid.uuid4()) for _ in docs]

    await store.aadd_texts(docs, metadatas=metadatas, ids=ids)

    return 'OK'

def getconn():
    conn = connector.connect(
        "projects/" + PROJECT_ID + "/locations/" + REGION + "/clusters/" + CLUSTER + "/instances/" + INSTANCE,
        "pg8000",
        user="username",
        password="password",
        db="postgres"
    )
    return conn
