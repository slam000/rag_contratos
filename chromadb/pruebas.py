import chromadb
import os

# Configurar ruta y cliente
CHROMA_DB_PATH = os.path.join(os.path.dirname(__file__), "chroma_db")
client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

# Crear o recuperar colección
try:
    collection = client.create_collection(name="contratos_alquiler")
except:
    collection = client.get_collection(name="contratos_alquiler")

# Leer y cargar el contrato si la colección está vacía
try:
    collection.peek() 
except:
    with open("contracts/contrato.txt", "r", encoding="utf-8") as f:
        contract_text = f.read()
        collection.add(
            documents=[contract_text],
            ids=["contrato_1"]
        )

# Consultas de prueba
pruebas = [
    "¿Quién es el arrendador?",
    "¿Cuál es la renta mensual?",
    "¿Cuál es la duración del contrato?",
    "¿Cuál es la dirección del inmueble?",
    "¿Cuál es el importe de la fianza?",
    "¿Cuáles son los gastos comunes mensuales?"
]

for pregunta in pruebas:
    resultados = collection.query(
        query_texts=[pregunta],
        n_results=1
    )
    print(f"\nPregunta: {pregunta}")
    print("Respuesta:", resultados['documents'][0][0][:500])