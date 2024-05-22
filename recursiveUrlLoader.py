from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from bs4 import BeautifulSoup as Soup

def exclude_css(html):
    soup = Soup(html, "html.parser")
    for link in soup.find_all("link", href=True):
        if link["href"].endswith(".css"):
            link.decompose()
    return soup.prettify()

url = "https://www.lu.lv"

loader = RecursiveUrlLoader(
    url=url, 
    max_depth=15, 
    extractor=exclude_css, 
    exclude_dirs=["https://www.lu.lv/en/", "https://www.lu.lv/par-mums/lu-mediji/zinas/zina/t/", "https://www.lu.lv/muzejs/par-mums/zinas/zina/"]
)
urls=[]
for i in loader.lazy_load():
    urls += [i.metadata["source"]]
urls = list(dict.fromkeys(urls))

urls = [x for x in urls if ".css" not in x]

print(urls)