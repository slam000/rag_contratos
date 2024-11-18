import chromadb
import os
import shutil

def clean_and_create_db():
   current_dir = os.path.dirname(os.path.abspath(__file__))
   chroma_dir = os.path.join(current_dir, "chroma_db")
   if os.path.exists(chroma_dir):
       shutil.rmtree(chroma_dir)
   os.makedirs(chroma_dir, exist_ok=True)
   return chroma_dir


def extract_sections(text):
    sections = {
        "arrendador": text[text.find("El/La primero/a, en nombre y representación"):text.find("Y el segundo,")],
        "arrendatario": text[text.find("De otra parte, D. NABIL"):text.find("INTERVIENEN")],
        "renta": text[text.find("5.1 Importe de la Renta"):text.find("Bonificación total")],
        "duracion": text[text.find("4.1 Duración"):text.find("4.2 Prórroga")],
        "fianza": text[text.find("7.1 Fianza"):text.find("7.2 Finalidad")],
        "gastos_comunes": text[text.find("10.2 Gastos Comunes"):text.find("10.3 Impuestos")]
    }
    
    return sections, {
        "arrendador": {"seccion": "identificacion"},
        "arrendatario": {"seccion": "identificacion"},
        "renta": {"seccion": "economico"},
        "duracion": {"seccion": "plazo"},
        "fianza": {"seccion": "economico"},
        "gastos_comunes": {"seccion": "economico"}
    }

def query_contract_db(collection, question, codigo_contrato="106591"):
    where_filter = {"$and": [{"codigo_contrato": codigo_contrato}]}
    
    if "renta" in question.lower():
        where_filter["$and"].append({"seccion": "economico"})
    elif "fianza" in question.lower():
        where_filter["$and"].append({"seccion": "economico"})
    elif "duración" in question.lower():
        where_filter["$and"].append({"seccion": "plazo"})
    elif "gastos" in question.lower():
        where_filter["$and"].append({"seccion": "economico"})
    
    results = collection.query(
        query_texts=[question],
        where=where_filter,
        n_results=1
    )
    
    if not results['documents'][0]:
        return ["No se encontró información"]
    return results['documents'][0]

def query_contract_db(collection, question, codigo_contrato="106591"):
    where_filter = {"codigo_contrato": codigo_contrato}
    
    # Determinar el tipo de búsqueda basado en la pregunta
    if "renta" in question.lower():
        where_filter = {"$and": [{"subtipo": "renta"}, {"codigo_contrato": codigo_contrato}]}
    elif "fianza" in question.lower():
        where_filter = {"$and": [{"subtipo": "garantia"}, {"codigo_contrato": codigo_contrato}]}
    elif "duración" in question.lower() or "plazo" in question.lower():
        where_filter = {"$and": [{"subtipo": "plazo"}, {"codigo_contrato": codigo_contrato}]}
    elif "arrendador" in question.lower():
        where_filter = {"$and": [{"subtipo": "arrendador"}, {"codigo_contrato": codigo_contrato}]}
    elif "arrendatario" in question.lower():
        where_filter = {"$and": [{"subtipo": "arrendatario"}, {"codigo_contrato": codigo_contrato}]}
    elif "gastos" in question.lower():
        where_filter = {"$and": [{"subtipo": "gastos"}, {"codigo_contrato": codigo_contrato}]}
    
    results = collection.query(
        query_texts=[question],
        where=where_filter,
        n_results=1
    )
    return results['documents'][0] if results['documents'] else ["No se encontró información"]

if __name__ == "__main__":
   chroma_dir = clean_and_create_db()
   collection = create_contract_db(chroma_dir)
   
   preguntas = [
       "¿Quién es el arrendador?",
       "¿Quiénes son los arrendatarios?",
       "¿Cuál es la renta mensual?",
       "¿Cuál es la duración del contrato?",
       "¿Cuál es el importe de la fianza?",
       "¿Cuáles son los gastos comunes mensuales?"
   ]
   
   for pregunta in preguntas:
       respuesta = query_contract_db(collection, pregunta)
       print(f"\nPregunta: {pregunta}")
       print(f"Respuesta:")
       print(f"{respuesta[0][:500]}\n")