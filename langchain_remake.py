from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.vectorstores import Chroma
import trafilatura
from langchain_community.document_loaders import SeleniumURLLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAI, OpenAIEmbeddings
import shutil
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFaceEndpoint
from vertexai.language_models import TextEmbeddingModel

def createEmbeddingStore():
    try:
        folder_path = './chroma_db'
        shutil.rmtree(folder_path)
        print('Folder and its content removed')
    except:
        print('Folder not deleted')
        
    urls = ["https://www.lu.lv/studijas/studiju-celvedis/akademiskais-kalendars/2023/2024-akademiska-gada-kalendars/", 
                "https://www.lu.lv/studijas/studiju-programmas/bakalaura-limena-studijas/datorzinatnes/",
                "https://www.lu.lv/studijas/studiju-programmas/bakalaura-limena-studijas/farmacija/"]
    
    loader = SeleniumURLLoader(urls=urls)
    documents = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    # embedding_function = OpenAIEmbeddings(model="text-embedding-3-large")
    embedding_function = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
    
    # load it into Chroma
    Chroma.from_documents(docs, embedding_function, persist_directory="./chroma_db")

def askQuestion(questions):
    embedding_function = OpenAIEmbeddings(model="text-embedding-3-large")
    db = Chroma(persist_directory="./chroma_db", embedding_function=embedding_function)
    retriever = db.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(
        llm=OpenAI(), chain_type="stuff", retriever=retriever, return_source_documents=True
    )
    for question in questions:
        print(f"Jautājums: {question}")
        chain_response = qa_chain(question)
        result = chain_response["result"]
        print(f"Atbilde: {result} \n")

""" 
url = "https://www.lu.lv/"
loader = RecursiveUrlLoader(url=url)
docs = loader.load()
print(len(docs))

for d in docs:
    print(d.metadata["source"])
 """

createEmbeddingStore()

""" jautajumi = [
        "Kad ir lieldienu brīvdienas?",
        "Kas ir datorzinātņu programmas direktors un kas ir farmācijas programmas direktors?",
        "Kādi ir uzņemšanas nosacījumi farmaceitiem?"
    ]
askQuestion(jautajumi) """