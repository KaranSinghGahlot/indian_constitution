# -*- coding: utf-8 -*-
"""indian_constitution.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1BWSJ4JcXrJXJX2nmzuY4f0YbPc1uwjt3
"""

import os
from pinecone import Pinecone
from llama_index.llms.gemini import Gemini
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import StorageContext, VectorStoreIndex, download_loader
from llama_index.core import Settings

GOOGLE_API_KEY = "AIzaSyAdyuatpPFW6w0WhDEX7Sl0Crm8yfENpFs"
PINECONE_API_KEY = "pcsk_4YrbsX_JJ6obocyaGscLnwd6q6DNmHf5X1dptn3E76Dpmn8rCncKN3j9n4tf2jm7PcqYif"

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

llm = Gemini()
embed_model=GeminiEmbedding(model_name="models/embedding-001")
Settings.llm=llm
Settings.embed_model=embed_model
Settings.chunk_size=1024

pinecone_client = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

for index in pinecone_client.list_indexes():
  print( index['name'])

index_description= pinecone_client.describe_index("indianconstitutionai")
print(index_description)

from llama_index.core import SimpleDirectoryReader

documents = SimpleDirectoryReader("/content/data").load_data()

pinecone_index=pinecone_client.Index("indianconstitutionai")
# Create a PineconeVectorStore using the specified pinecone_index
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)

# Create a StorageContext using the created PineconeVectorStore
storage_context = StorageContext.from_defaults(
    vector_store=vector_store
)

# Use the chunks of documents and the storage_context to create the index
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context
)

chat_engine = index.as_chat_engine()
while True:
    text_input = input("User: ")
    if text_input.lower() == "exit":
        break
    try:
        response = chat_engine.chat(text_input)

        print(f"Agent: {response.response}")


    except Exception as e:
        print(f"Error during query: {str(e)}")