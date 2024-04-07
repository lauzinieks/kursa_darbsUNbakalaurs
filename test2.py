from llama_index.core import VectorStoreIndex
from llama_index.readers.web import TrafilaturaWebReader
import chromadb
from llama_index.llms.ollama import Ollama
from llama_index.core import Settings

def createEmbeddingStore(name):
    chroma_client = chromadb.Client()
    return chroma_client.create_collection(name)

def queryPages(collection, urls, questions):
    Settings.llm = Ollama(model="mystral", request_timeout=120.0)
    docs = TrafilaturaWebReader().load_data(urls)
    index = VectorStoreIndex.from_documents(docs, chroma_collection=collection)
    queryEngine = index.as_query_engine()
    for question in questions:
        print(f"Jautājums: {question}")
        print(f"Atbilde: {queryEngine.query(question)} \n")

if __name__ == "__main__":
    urlList1 = ["https://www.lu.lv/studijas/studiju-celvedis/akademiskais-kalendars/2023/2024-akademiska-gada-kalendars/", 
                "https://www.lu.lv/studijas/studiju-programmas/bakalaura-limena-studijas/datorzinatnes/",
                "https://www.lu.lv/studijas/studiju-programmas/bakalaura-limena-studijas/farmacija/"]
    questions1 = [
        "Kad ir lieldienu brīvdienas?",
        "Kas ir datorzinātņu programmas direktors un kas ir farmācijas programmas direktors?",
        "Kādi ir uzņemšanas nosacījumi farmaceitiem?"
    ]
    urlList2 = ["https://www.lu.lv/en/studies/study-process/academic-calendar/2023/2024-academic-year-calendar/", 
                "https://www.lu.lv/en/studies/study-programmes-1/bachelors-study-programmes/computer-science/",
                "https://www.lu.lv/en/studies/study-programmes-1/bachelors-study-programmes/pharmacy/"]
    questions2 = [
        "When are the easter holidays?",
        "Who is computer science study programms director and who is farmacy study programms director?",
        "What are entry conditions for farmacy studie programm?"
    ]

    collection = createEmbeddingStore("LUMIs")

    queryPages(
        collection,
        urlList1,
        questions1
    )