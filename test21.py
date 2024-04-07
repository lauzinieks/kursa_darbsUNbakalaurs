from llama_index import VectorStoreIndex, download_loader
import chromadb

from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
import torch

model = "tiiuae/falcon-7b"

tokenizer = AutoTokenizer.from_pretrained(model)
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
    device_map="auto",
)

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
    url_list = ["https://www.lu.lv/studijas/studiju-celvedis/akademiskais-kalendars/2023/2024-akademiska-gada-kalendars/", 
                "https://www.lu.lv/studijas/fakultates/datorikas-fakultate/bakalaura-limena-studijas/datorzinatnes/",
                "https://www.lu.lv/studijas/fakultates/medicinas-fakultate/bakalaura-limena-studijas/farmacija/"]
    questions = [
        "Kad ir lieldienu brīvdienas?",
        "Kas ir datorzinātņu programmas direktors?",
        "Kādi ir uzņemšanas nosacījumi farmaceitiem un kā tie atšķiras no datorzinātņu fakultātes?"
    ]

    collection = create_embedding_store("lumis")

    query_pages(
        collection,
        url_list,
        questions
    )