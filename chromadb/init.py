import chromadb
from chromadb.utils import embedding_functions

# Inicializar cliente
client = chromadb.Client()

# Crear colección
collection = client.create_collection(name="contratos_alquiler")