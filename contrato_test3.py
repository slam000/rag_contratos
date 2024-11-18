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

# 3. Fragmentos relevantes del contrato
fragmentos_contrato = {
    "partes": """
    De una parte, D. Daniel Leganés Ferreras y Dña. Mercedes Paniagua Guijarro, con documento
    nacional de identidad 46840734S y 02648205P respectivamente, en nombre y representación de 
    DIVARIAN PROPIEDAD, S.A., con CIF A-81.036.501
    
    De otra parte, D. NABIL EL KHAYAT EL KHAYAT, con documentos nacional de identidad 54029866Z
    
    De otra parte, D. MOHAMED EL KHAYAT EL KHAYAT, con documento nacional de identidad 53322137H
    """,
    
    "inmueble": """
    Vivienda sita en Viladecans, con una superficie aproximada de 40 m2, inscrita en el Registro 
    de la Propiedad número 1 de Viladecans, al tomo 1309, libro 665, folio 197, finca número 6848.
    
    Dirección: Calle CATALUNYA, 58, 2 1, 08840 VILADECANS, BARCELONA
    FINCA REGISTRAL: 6848
    REFERENCIA CATASTRAL: 8544903DF1784D0009BS
    """,
    
    "condiciones_economicas": """
    5.1 Importe de la Renta: El Arrendatario abonará al Arrendador una renta mensual de
    Seiscientos Treinta Euros (630 €), cada una, a pagar en mensualidades anticipadas.
    
    10.2 Gastos Comunes: el importe anual de Gastos Comunes de la Finca para el ejercicio 2020 
    ascienden a 480 euros anuales, 40 euros mensuales.
    
    10.3 Impuestos: el importe anual por este concepto para el ejercicio 2020 asciende a 203,95 euros anuales.
    
    Bonificaciones según Adenda:
    - Primer año: 100% de los Costes Repercutibles
    - Segundo año: 66% de los Costes Repercutibles
    - Tercer año: 33% de los Costes Repercutibles
    """,
    
    "duracion": """
    4.1 Duración: La duración del presente Contrato será de siete (7) años a contar desde la fecha
    de firma del mismo, 30 de marzo de 2020.
    
    7.1 Fianza: El Arrendatario hace entrega en este acto al Arrendador, en concepto de fianza
    legal, la cantidad de Seiscientos Treinta Euros (630 €) equivalente a una (1) mensualidad de renta.
    """
}

def extract_contract_data():
    """Realiza la consulta a Claude y extrae la información"""
    try:
        message = anthropic.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": f"""
                Extrae la siguiente información del contrato y devuélvela en formato JSON con exactamente esta estructura:

                {{
                    "arrendador": {{
                        "nombre": "nombre de la empresa",
                        "cif": "número de CIF",
                        "representantes": ["nombre y DNI"]
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
                        "registro": "datos registro propiedad",
                        "finca": "número de finca"
                    }},
                    "condiciones_economicas": {{
                        "renta_mensual": "importe en euros",
                        "gastos_comunes": {{
                            "mensual": "importe en euros",
                            "anual": "importe en euros"
                        }},
                        "impuestos": "importe anual en euros",
                        "bonificaciones": {{
                            "primer_año": "porcentaje",
                            "segundo_año": "porcentaje",
                            "tercer_año": "porcentaje"
                        }}
                    }},
                    "duracion": {{
                        "plazo": "duración del contrato",
                        "fecha_inicio": "fecha",
                        "fianza": "importe"
                    }}
                }}

                Fragmentos del contrato:
                {json.dumps(fragmentos_contrato, indent=2)}
                
                Devuelve solo el JSON, sin ningún texto adicional.
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
        print(f"Error al consultar Claude: {e}")
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
                    elif isinstance(subvalue, list):
                        df_rows.append({
                            'Categoría': key,
                            'Subcategoría': subkey,
                            'Valor': ', '.join(subvalue)
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