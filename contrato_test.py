import os
from anthropic import Anthropic
import json
import pandas as pd
from dotenv import load_dotenv

# 1. Cargar variables de entorno
load_dotenv()
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

# 2. Inicializar cliente de Anthropic
anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)

# 3. Datos de prueba
fragmentos_contrato = {
    "partes": """
    De una parte: D./Dña. ENRIQUE JIMENEZ MONTES con DNI 75140348S, en representación de PROMONTORIA MACC 1X1 SOCIMI, S.A, con CIF A88534359
    De otra parte: 
    D./Dña. Glenda Isabel Sumalave Zambrano con DNI Y9028643F
    D./Dña. Erika Lizeth Herrera Granada con DNI 09231449P
    """,
    
    "inmueble": """
    Vivienda: sita en CL DE BADAJOZ número 7, planta 1 y letra 1, con una superficie aproximada de 66,00 m2, 
    inscrita en el Registro de la Propiedad número 01-ALCORCON, finca número 24602 
    y con referencia catastral 9567001VK2696N0004DR
    """,
    
    "condiciones_economicas": """
    El Arrendatario abonará al Arrendador una renta mensual de 990,00 €
    Gastos comunes: 70,00€/mes (840,00€/año)
    IBI: 34,35€/mes (412,20€/año)
    Suministro agua: 20,00€/mes (240,00€/año)
    """
}

def extract_contract_data():
    try:
        # Crear el mensaje para Claude
        message = anthropic.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": f"""
                Extrae la siguiente información del contrato y devuélvela en JSON:
                {json.dumps(fragmentos_contrato, indent=2)}
                
                Necesito los siguientes datos específicos:
                - Arrendador (nombre y CIF)
                - Arrendatarios (nombres y DNIs)
                - Dirección completa
                - Superficie
                - Referencia Catastral
                - Registro de la Propiedad
                - Renta mensual
                - Gastos mensuales desglosados
                
                Devuelve solo el JSON, sin explicaciones adicionales.
                """
            }]
        )
        
        # Obtener la respuesta
        response = message.content[0].text
        print("Respuesta de Claude:")
        print(response)
        
        # Intentar parsear el JSON
        try:
            datos = json.loads(response)
            print("\nDatos parseados correctamente")
            return datos
        except json.JSONDecodeError as e:
            print(f"Error al parsear JSON: {e}")
            return None
            
    except Exception as e:
        print(f"Error al consultar a Claude: {e}")
        return None

def main():
    print("Iniciando extracción de datos...")
    print(f"API Key configurada: {'Sí' if ANTHROPIC_API_KEY else 'No'}")
    
    datos = extract_contract_data()
    
    if datos:
        print("\nDatos extraídos:")
        print(json.dumps(datos, indent=2, ensure_ascii=False))
        
        # Crear DataFrame
        df = pd.DataFrame([
            {"Campo": k, "Valor": v} 
            for k, v in datos.items()
        ])
        
        print("\nTabla de datos:")
        print(df)
    else:
        print("No se pudieron extraer los datos")

if __name__ == "__main__":
    main()