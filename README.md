# Proyecto RAG de Extracción de Datos de Contratos de Alquiler

Este proyecto es una prueba de concepto (PoC) para la extracción de datos de contratos de alquiler utilizando una base de datos vectorial ChromaDB y la API de Claude.

## Descripción

El objetivo de este proyecto es demostrar cómo se pueden extraer datos relevantes de contratos de alquiler utilizando técnicas de Recuperación de Información y Generación de Respuestas (RAG). La base de datos ChromaDB se utiliza para almacenar y gestionar los datos, mientras que la API de Claude se emplea para procesar y extraer la información.

## Requisitos

- Python 3.8 o superior
- Entorno virtual (recomendado)
- Dependencias listadas en `requirements.txt`

## Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/tu-usuario/tu-repositorio.git
cd tu-repositorio
```

2. Crea y activa un entorno virtual de Python
```python
python -m venv venv
source venv/bin/activate
```

**Nota**: en windows 
```cmd
venv\scripts\activate
```

3. Instala las dependencias
```bash    
pip install -r requirements.txt
```

## Uso

1. Crea un archivo .env en el raiz del proyecto
```bash
touch .env
```

2. Configura las variables de entorno necesarias en un archivo .env
```.env
CLAUDE_API_KEY=tu_clave_api
CHROMADB_URI=tu_uri_chromadb
```

3. Ejecuta el script

En esta prueba se han realizado 2 pruebas diferentes para la extracción de datos de 2 modelos de contratos distintos.

Prueba 1:
```bash
python contrato_test2.py
```

Prueba 2:
```bash
python contrato_test3.py
```

## Licencia
Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.

