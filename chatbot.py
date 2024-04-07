from llama_index import VectorStoreIndex, download_loader
import chromadb

TrafilaturaWebReader = download_loader("TrafilaturaWebReader")
loader = TrafilaturaWebReader()

def create_embedding_store(name):
    chroma_client = chromadb.Client()
    return chroma_client.create_collection(name)

def query_pages(collection, urls, questions):
    docs = loader.load_data(urls)
    index = VectorStoreIndex.from_documents(docs, chroma_collection=collection)
    query_engine = index.as_query_engine()
    for question in questions:
        print(f"Jautājums: {question} \n")
        print(f"Atbilde: {query_engine.query(question)}")

if __name__ == "__main__":
    url_list = ["https://en.wikipedia.org/wiki/Large_language_model", 
                "https://www.techtarget.com/whatis/definition/large-language-model-LLM"]
    questions = [
        "What is LLM and how can I use it? And can you answer in latvian?"
    ]

    collection = create_embedding_store("lumis")

    query_pages(
        collection,
        url_list,
        questions
    )