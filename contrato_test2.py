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

# 3. Datos de prueba más realistas
fragmentos_contrato = {
    "partes": """
    REUNIDOS
    De una parte:
    D./Dña. ENRIQUE JIMENEZ MONTES con DNI 75140348S y domicilio a estos efectos en Plaza Manuel Gómez Moreno, nº 2, planta 16, Madrid, Madrid 28020 España.
    
    El/La primero/a, en nombre y representación, en su condición de Apoderado, de la compañía mercantil PROMONTORIA MACC 1X1 SOCIMI, S.A, con domicilio social en Plaza Manuel Gómez Moreno, nº 2, planta 16, Madrid, Madrid 28020 España, e inscrita en el Registro Mercantil de Madrid, al tomo 39908, folio 109, hoja nº M-708813, inscripción y titular de CIF A88534359 (en adelante, el "Futuro Arrendador").
    
    De otra parte:
    D./Dña. Glenda Isabel Sumalave Zambrano con DNI Y9028643F y domicilio a estos efectos en CL DE BADAJOZ, número 7, planta 1 y letra 1.
    D./Dña. Erika Lizeth Herrera Granada con DNI 09231449P y domicilio a estos efectos en CL DE BADAJOZ, número 7, planta 1 y letra 1.
    """,
    
    "inmueble": """
    I. Que el Arrendador es dueño en pleno dominio de:
    Vivienda: sita en CL DE BADAJOZ número 7, planta 1 y letra 1, con una superficie aproximada de 66,00 m2, inscrita en el Registro de la Propiedad número 01-ALCORCON, finca número 24602 y con referencia catastral 9567001VK2696N0004DR
    En adelante, la Vivienda, la "Finca".
    """,
    
    "condiciones_economicas": """
    5. RENTA
    5.1 Importe de la Renta:
    El Arrendatario abonará al Arrendador una renta mensual de 990,00 €, cada una, a pagar en mensualidades anticipadas (la "Renta").
    
    9.2 Gastos Comunes:
    De conformidad con lo previsto en el artículo 20.1 de la LAU, las Partes han acordado que la cuota de la Finca en los gastos comunes del inmueble del que forma parte sea satisfecha por el Arrendatario (los "Gastos Comunes").
    A fecha de firma de este Contrato, el importe anual de Gastos Comunes de la Finca para el ejercicio 17/06/2024 asciende a 840,00 € anuales.
    Los Gastos Comunes serán repercutidos mensualmente a razón de 70,00 € por el Arrendador al Arrendatario en el recibo de la Renta.
    
    9.3 Impuestos:
    A fecha de firma de este Contrato, el importe anual por este concepto para el ejercicio 17/06/2024 asciende a 412,20 € anuales.
    El IBI será prorrateado y repercutido mensualmente a razón de 34,35 € por el Arrendador al Arrendatario en el recibo de la Renta.
    """,
    
    "duracion": """
    4. DURACIÓN
    4.1 Duración: La duración del presente Contrato será de siete (7) años y entrará en vigor en la fecha de entrega de la posesión de la Finca, 17/06/2024, surtiendo efectos económicos a partir de ese mismo día (la "Duración").
    
    7. FIANZA
    7.1 FIANZA
    A. Fianza: El Arrendatario ha abonado al Arrendador, la cantidad equivalente a una (1) mensualidad de Renta en concepto de fianza (en adelante, la "Fianza").
    """
}

def extract_contract_data():
    try:
        message = anthropic.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": f"""
                Extrae la siguiente información específica del contrato y devuélvela en formato JSON exactamente con esta estructura:

                {{
                    "arrendador": {{
                        "nombre": "nombre de la empresa",
                        "cif": "número de CIF"
                    }},
                    "arrendatarios": [
                        {{
                            "nombre": "nombre completo",
                            "dni": "número de DNI"
                        }}
                    ],
                    "inmueble": {{
                        "direccion": "dirección completa",
                        "superficie": "metros cuadrados",
                        "ref_catastral": "referencia catastral",
                        "registro": "datos registro propiedad"
                    }},
                    "condiciones_economicas": {{
                        "renta_mensual": "importe en euros",
                        "gastos_comunes": {{
                            "mensual": "importe en euros",
                            "anual": "importe en euros"
                        }},
                        "ibi": {{
                            "mensual": "importe en euros",
                            "anual": "importe en euros"
                        }}
                    }},
                    "duracion": {{
                        "plazo": "duración del contrato",
                        "fecha_inicio": "fecha",
                        "fianza": "importe o descripción"
                    }}
                }}

                Fragmentos del contrato:
                {json.dumps(fragmentos_contrato, indent=2)}
                
                Devuelve solo el JSON con la estructura exacta especificada, sin texto adicional.
                """
            }]
        )
        
        response = message.content[0].text
        print("Respuesta de Claude:")
        print(response)
        
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
        print("\nDatos extraídos (JSON):")
        print(json.dumps(datos, indent=2, ensure_ascii=False))
        
        # Guardar en archivo JSON
        with open('datos_contrato.json', 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        
        # Crear DataFrame para visualización
        df_rows = []
        for key, value in datos.items():
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    if isinstance(subvalue, dict):
                        for subsubkey, subsubvalue in subvalue.items():
                            df_rows.append({
                                'Categoría': key,
                                'Subcategoría': f"{subkey} - {subsubkey}",
                                'Valor': subsubvalue
                            })
                    else:
                        df_rows.append({
                            'Categoría': key,
                            'Subcategoría': subkey,
                            'Valor': subvalue
                        })
            elif isinstance(value, list):
                for i, item in enumerate(value, 1):
                    for subkey, subvalue in item.items():
                        df_rows.append({
                            'Categoría': key,
                            'Subcategoría': f"Arrendatario {i} - {subkey}",
                            'Valor': subvalue
                        })
        
        df = pd.DataFrame(df_rows)
        print("\nDatos en formato tabla:")
        print(df.to_string(index=False))
        
        # Guardar en CSV
        df.to_csv('datos_contrato.csv', index=False, encoding='utf-8')
        
        print("\nArchivos generados: datos_contrato.json y datos_contrato.csv")
    else:
        print("No se pudieron extraer los datos")

if __name__ == "__main__":
    main()