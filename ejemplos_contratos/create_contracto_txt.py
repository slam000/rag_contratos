import PyPDF2
import os

def pdf_to_txt(pdf_path, txt_path):
   # Abrir el PDF
   with open(pdf_path, 'rb') as file:
       # Crear objeto PDF
       pdf_reader = PyPDF2.PdfReader(file)
       
       # Extraer texto de cada página
       text = ''
       for page in pdf_reader.pages:
           text += page.extract_text()
           
       # Guardar en archivo txt
       with open(txt_path, 'w', encoding='utf-8') as txt_file:
           txt_file.write(text)

# Rutas
pdf_path = 'ejemplos_contratos\Contract.pdf' 
txt_path = 'ejemplos_contratos\Contract.txt'

# Crear directorio si no existe
os.makedirs(os.path.dirname(txt_path), exist_ok=True)

# Convertir PDF a TXT
pdf_to_txt(pdf_path, txt_path)