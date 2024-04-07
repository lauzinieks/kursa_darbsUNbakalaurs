from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import Html2TextTransformer
from langchain.chains import create_extraction_chain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import pprint
from langchain.text_splitter import RecursiveCharacterTextSplitter

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
vectorstore = Chroma(
    embedding_function=OpenAIEmbeddings(), persist_directory="./chroma_db_oai"
)

schema = {
    "properties": {
        "news_article_text": {"type": "string"},
    },
    "required": ["news_article_text"],
}


def extract(content: str, schema: dict):
    return create_extraction_chain(schema=schema, llm=llm).invoke(content)

def scrape_with_playwright(urls, schema):
    loader = AsyncChromiumLoader(urls)
    docs = loader.load()
    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(
        docs, tags_to_extract=["p"]
    )

    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000, chunk_overlap=0
    )
    splits = splitter.split_documents(docs_transformed)

    extracted_content = extract(schema=schema, content=splits[0].page_content)
    pprint.pprint(extracted_content)
    return extracted_content


urls = ["https://www.lu.lv/studijas/fakultates/datorikas-fakultate/bakalaura-limena-studijas/datorzinatnes/"]
extracted_content = scrape_with_playwright(urls, schema=schema)