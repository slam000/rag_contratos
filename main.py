import os
import subprocess

def mostrar_menu():
    print("Seleccione el ejemplo que desea ejecutar:")
    print("1. Modelo de contrato 1")
    print("2. Modelo de contrato 2")
    print("0. Salir")

def confirmar_seleccion(opcion):
    if opcion == '1':
        print("\nHa seleccionado el modelo de contrato 1")
    elif opcion == '2':
        print("\nHa seleccionado el modelo de contrato 2")
    else:
        print("\nSelección inválida")
        return False
    
    confirmacion = input("¿Desea continuar? (s/n): ")
    print(f"Confirmación recibida: {confirmacion}")  # Depuración
    return confirmacion.lower() == 's'

def ejecutar_ejemplo(opcion):
    print(f"Ejecutando ejemplo para opción: {opcion}")  # Depuración
    if opcion == '1':
        script_path =  './test/contrato_test2.py'
    elif opcion == '2':
        script_path = './test/contrato_test3.py'
    else:
        print("Opción no válida.")  # Depuración
        
    try:
        resultado = subprocess.run(['python', script_path], check=True)
        print(f"Resultado: {resultado}")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar script: {e}")
        

def main():
    while True:
        mostrar_menu()
        opcion = input("Ingrese su opción: ")
        print(f"Opción ingresada: {opcion}")  # Depuración
        
        if opcion == '0':
            print("Saliendo...")
            break
        
        if confirmar_seleccion(opcion):
            ejecutar_ejemplo(opcion)
        else:
            print("Volviendo al menú principal...")
            
if __name__ == '__main__':
    main()