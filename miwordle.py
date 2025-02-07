
import unicodedata
import os
from collections import Counter

# Cargar la clave de API de OpenAI desde una variable de entorno


def normalizar_palabra(palabra):
    """Normaliza una palabra eliminando las tildes."""
    return unicodedata.normalize('NFD', palabra).encode('ascii', 'ignore').decode('utf-8')

def cargar_palabras():
    """Carga y filtra palabras válidas desde el archivo palabras_validas.txt."""
    filepath = "palabras_validas.txt"
    palabras = set()
    if not os.path.exists(filepath):
        print(f"Error: No se encontró el archivo '{filepath}'.")
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                palabra = linea.strip().upper()
                palabra_normalizada = normalizar_palabra(palabra)
                if len(palabra_normalizada) == 5 and palabra_normalizada.isalpha():
                    palabras.add(palabra_normalizada)
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return []
    return list(palabras) if palabras else []

def filtrar_palabras(palabras_posibles, intento, resultado):
    """Filtra palabras basándose en el resultado del intento de Wordle."""
    nuevas_palabras = []

    for palabra in palabras_posibles:
        palabra_normalizada = normalizar_palabra(palabra)
        coincide = True
        
        # Conteos de letras en la palabra y en el intento
        conteo_intento = {letra: intento.count(letra) for letra in set(intento)}
        conteo_palabra = {letra: palabra_normalizada.count(letra) for letra in set(palabra_normalizada)}

        for i in range(5):
            letra_intento = intento[i]
            letra_palabra = palabra[i]

            if resultado[i] == 'b':  # 'b' -> Letra en la posición correcta
                if letra_palabra != letra_intento:
                    coincide = False
                    break

            elif resultado[i] == 'c':  # 'c' -> Letra está en otra posición
                if letra_intento not in palabra_normalizada or letra_palabra == letra_intento:
                    coincide = False
                    break

            elif resultado[i] == 'm':  # 'm' -> Letra NO está en la palabra en ninguna posición
                if conteo_intento[letra_intento] <= conteo_palabra.get(letra_intento, 0):
                    coincide = False
                    break

        if coincide:
            nuevas_palabras.append(palabra)

    if not nuevas_palabras:
        print("⚠️ ERROR: Se eliminaron todas las palabras. Verifica la lógica de filtrado.")

    return nuevas_palabras



def seleccionar_mejor_palabra(palabras_posibles):
    """Selecciona la mejor palabra basada en la frecuencia de letras."""
    if not palabras_posibles:
        return None
    frecuencia_letras = Counter("".join(palabras_posibles))
    
    def puntuacion_palabra(palabra):
        return sum(frecuencia_letras[letra] for letra in set(palabra))
    
    palabras_posibles.sort(key=puntuacion_palabra, reverse=True)
    return palabras_posibles[0]

def wordle_solver():
    print("\n¡Bienvenido al solucionador de Wordle en español!")
    palabras_validas = cargar_palabras()
    
    if not palabras_validas:
        print("Error: No se pudieron cargar palabras válidas.")
        return
    
    palabras_posibles = palabras_validas.copy()
    intentos = 0
    retroalimentacion_acumulada = ""
    intentos_previos = set()
    
    # Solicitar la primera palabra al usuario
    while True:
        primer_intento = input("Ingresa la primera palabra de 5 letras: ").strip().upper()
        primer_intento_normalizado = normalizar_palabra(primer_intento)
        if len(primer_intento_normalizado) == 5 and primer_intento_normalizado.isalpha():
            break
        print("⚠️ Entrada inválida. Ingresa una palabra de exactamente 5 letras.")
    
    intentos += 1
    intentos_previos.add(primer_intento)
    
    print(f"Intento {intentos}: {primer_intento}")
    
    while True:
        resultado = input("Ingresa el resultado usando 'm', 'c', y 'b' (ejemplo: 'mmcbc'): ").strip().lower()
        if len(resultado) == 5 and all(c in 'mcb' for c in resultado):
            break
        print("⚠️ Entrada inválida. Usa solo 'm', 'c' y 'b' con longitud exacta de 5.")
    
    retroalimentacion_acumulada += f"\nPalabra: {primer_intento}, Resultado: {resultado}"
    palabras_posibles = filtrar_palabras(palabras_posibles, primer_intento, resultado)
    
    if resultado == "bbbbb":
        print(f"¡El bot ha resuelto la palabra: {primer_intento} en {intentos} intentos! 🎉")
        return
    
    while intentos < 6 and palabras_posibles:
        intento = seleccionar_mejor_palabra(palabras_posibles)
        if not intento:
            print("No quedan palabras posibles para intentar.")
            return
        while intento in intentos_previos:
            intento = seleccionar_mejor_palabra(palabras_posibles)
        intentos_previos.add(intento)
        intentos += 1

        print(f"Intento {intentos}: {intento}")
        
        while True:
            resultado = input("Ingresa el resultado usando 'm', 'c', y 'b' (ejemplo: 'mmcbc'): ").strip().lower()
            if len(resultado) == 5 and all(c in 'mcb' for c in resultado):
                break
            print("⚠️ Entrada inválida. Usa solo 'm', 'c' y 'b' con longitud exacta de 5.")
        
        retroalimentacion_acumulada += f"\nPalabra: {intento}, Resultado: {resultado}"
        palabras_posibles = filtrar_palabras(palabras_posibles, intento, resultado)
        
        if resultado == "bbbbb":
            print(f"¡El bot ha resuelto la palabra: {intento} en {intentos} intentos! 🎉")
            return
        
        print(f"Palabras restantes: {len(palabras_posibles)}")
    
    if palabras_posibles:
        print("El bot aún tiene opciones viables pero no pudo encontrar la solución exacta dentro del límite de intentos.")
        print(f"Últimas palabras posibles: {', '.join(palabras_posibles[:10])} ...")
    else:
        print("No quedan palabras posibles según las indicaciones dadas.")

if __name__ == "__main__":
    wordle_solver()