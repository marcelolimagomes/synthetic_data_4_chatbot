import ollama
import sys
import chromadb
from utilities import getconfig

embedmodel = getconfig()["embedmodel"]
mainmodel = getconfig()["mainmodel"]
chroma = chromadb.HttpClient(host="localhost", port=8000)
collection = chroma.get_or_create_collection("buildragwithpython")

query = " ".join(sys.argv[1:])
queryembed = ollama.embeddings(model=embedmodel, prompt=query)['embedding']


relevantdocs = collection.query(query_embeddings=[queryembed], n_results=5)["documents"][0]
print(relevantdocs)
docs = "\n\n".join(relevantdocs)
print(docs)
modelquery = f"{query} - Responda a essa pergunta usando o seguinte texto como recurso: {docs}"
print(modelquery)

stream = ollama.generate(model=mainmodel, prompt=modelquery, stream=True)

for chunk in stream:
  if chunk["response"]:
    print(chunk['response'], end='', flush=True)
