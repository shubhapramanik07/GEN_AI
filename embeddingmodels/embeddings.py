from langchain_mistralai import MistralAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embeddings = MistralAIEmbeddings(model="mistral-embed")

texts = ["Hello, how are you?", "what is your name?"]

vector = embeddings.embed_documents(texts)

print(vector)

# here what we are doing is we are creating an instance of the MistralAIEmbeddings class and then we are calling the embed_documents method to get the embeddings for the given texts. The output will be a list of vectors corresponding to each input text. which can be used for various applications like semantic search, clustering, etc. in real-life example: 