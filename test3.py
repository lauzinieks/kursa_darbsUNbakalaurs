from llama_index.core import Settings
from llama_index.core import VectorStoreIndex
from llama_index.readers.web import TrafilaturaWebReader
from llama_index.llms.ollama import Ollama
import chromadb

def createEmbeddingStore(name):
    chroma_client = chromadb.Client()
    return chroma_client.create_collection(name)

def queryPages(collection, urls, questions):
    docs = TrafilaturaWebReader().load_data(urls)
    index = VectorStoreIndex.from_documents(docs, chroma_collection=collection)
    queryEngine = index.as_query_engine()
    for question in questions:
        print(f"Jautājums: {question}")
        print(f"Atbilde: {queryEngine.query(question)} \n")

if __name__ == "__main__":
    Settings.llm = Ollama(model="llama2", request_timeout=30.0)
    
    urlList = ["https://www.lu.lv/studijas/studiju-celvedis/akademiskais-kalendars/2023/2024-akademiska-gada-kalendars/", 
                "https://www.lu.lv/studijas/fakultates/datorikas-fakultate/bakalaura-limena-studijas/datorzinatnes/",
                "https://www.lu.lv/studijas/fakultates/medicinas-fakultate/bakalaura-limena-studijas/farmacija/"]
    questions = [
        "Kad ir lieldienu brīvdienas?",
        "Kas ir datorzinātņu programmas direktors un kas ir farmācijas programmas direktors?",
        "Kādi ir uzņemšanas nosacījumi farmaceitiem?"
    ]

    collection = createEmbeddingStore("LUMIs")

    queryPages(
        collection,
        urlList,
        questions
    )