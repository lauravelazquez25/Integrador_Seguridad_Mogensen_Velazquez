# idioma_evolucion.py
# 4C: El idioma EVOLUCIONA. Parte del codigo ya acordado (codigo_acordado.json),
#     enfrenta una necesidad NUEVA (emergencia/cancelacion) y suma simbolos.

from openai import OpenAI
import json
import os

cliente = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="lm-studio")

MODELO_A = "llama-3.2-3b-instruct"
MODELO_B = "google/gemma-3-4b"

ARCHIVO = "codigo_acordado.json"

# ============================================================
# 1) LEER el idioma que YA existe (el inverso de lo que guardamos)
# ============================================================
if os.path.exists(ARCHIVO):
    with open(ARCHIVO, "r", encoding="utf-8") as f:
        codigo_previo = json.load(f)   # lee el JSON y lo vuelve diccionario
else:
    codigo_previo = {}   # si no existe, arrancamos vacio (no deberia pasar ahora)

print(f"[INFO] Idioma previo: {len(codigo_previo)} simbolos -> {codigo_previo}")

# Convertimos el diccionario a texto legible para inyectarlo en el prompt.
# Queda tipo:  LUG = triángulo\nHR = circulo con 10\n...
codigo_previo_texto = "\n".join(f"{s} = {sig}" for s, sig in codigo_previo.items())

# ============================================================
# 2) La MISION nueva: algo que el codigo actual NO cubre
# ============================================================
MISION = (
    "Ya tienen un codigo acordado para coordinar encuentros (lugar, hora, "
    "confirmacion). AHORA surge una necesidad NUEVA que ese codigo no cubre: "
    "deben poder avisar una EMERGENCIA y CANCELAR el encuentro. "
    "Necesitan inventar simbolos nuevos para: PELIGRO, CANCELAR y TODO_BIEN. "
    "Usen su codigo viejo cuando aplique e INVENTEN los simbolos que falten."
)

def system_para(nombre, otra):
    base = (
        f"Sos la IA '{nombre}' y te comunicas con la IA '{otra}'.\n"
        f"{MISION}\n"
        "Responde SIEMPRE breve.\n"
    )
    # Inyectamos el idioma que YA tienen, para que lo reusen.
    if codigo_previo_texto.strip():
        base += f"\nCodigo que YA acordaron (usenlo):\n{codigo_previo_texto}\n"
    return base

SYSTEM_A = system_para("A", "B")
SYSTEM_B = system_para("B", "A")

historial_A = [{"role": "system", "content": SYSTEM_A}]
historial_B = [{"role": "system", "content": SYSTEM_B}]

arranque = "Tenemos una necesidad nueva: avisar emergencias y cancelar. Propone simbolos para eso. Arranca vos."
historial_A.append({"role": "user", "content": arranque})

# ============================================================
# 3) El dialogo (igual que antes)
# ============================================================
TURNOS = 4
for i in range(TURNOS):
    r_A = cliente.chat.completions.create(model=MODELO_A, messages=historial_A)
    texto_A = r_A.choices[0].message.content
    print(f"\nA (Llama) [{i+1}]: {texto_A}")
    historial_A.append({"role": "assistant", "content": texto_A})
    historial_B.append({"role": "user",      "content": texto_A})

    r_B = cliente.chat.completions.create(model=MODELO_B, messages=historial_B)
    texto_B = r_B.choices[0].message.content
    print(f"B (Gemma) [{i+1}]: {texto_B}")
    historial_B.append({"role": "assistant", "content": texto_B})
    historial_A.append({"role": "user",      "content": texto_B})

# ============================================================
# 4) CIERRE: B redacta la tabla COMPLETA (vieja + nueva)
# ============================================================
pedido_cierre = (
    "Ahora cerramos. Escribi la tabla final COMPLETA de simbolos: los que ya "
    "tenian MAS los nuevos que acordaron.\n"
    "REGLAS ESTRICTAS:\n"
    "- Cada linea debe ser: SIMBOLO = significado\n"
    "- El SIMBOLO va SIEMPRE al principio y NO puede estar vacio.\n"
    "- No escribas nada fuera de las marcas.\n\n"
    "Ejemplo EXACTO del formato:\n"
    "===TABLA_INICIO===\n"
    "LUG = lugar del encuentro\n"
    "PEL = peligro\n"
    "===TABLA_FIN===\n\n"
    "Ahora escribi TU tabla real completa, en ese mismo formato:"
)
historial_B.append({"role": "user", "content": pedido_cierre})
r_cierre = cliente.chat.completions.create(model=MODELO_B, messages=historial_B)
tabla_final = r_cierre.choices[0].message.content

print("\n==================== TABLA FINAL (redactada por B) ====================")
print(tabla_final)

# ============================================================
# 5) CAPTURAR y GUARDAR (con versionado)
# ============================================================
MARCA_INI = "===TABLA_INICIO==="
MARCA_FIN = "===TABLA_FIN==="

if MARCA_INI in tabla_final and MARCA_FIN in tabla_final:
    cuerpo = tabla_final.split(MARCA_INI)[1].split(MARCA_FIN)[0]
else:
    print("\n[AVISO] No encontre las marcas; intento parsear todo el texto.")
    cuerpo = tabla_final

codigo_nuevo = {}
for linea in cuerpo.splitlines():
    if "=" in linea:
        partes = linea.split("=", 1)
        simbolo = partes[0].strip()
        significado = partes[1].strip()
        if simbolo:
            codigo_nuevo[simbolo] = significado

if len(codigo_nuevo) == 0:
    print("\n[!] ATENCION: 0 simbolos capturados. No piso nada. Volve a correr.")
else:
    # a) Pisamos el archivo "oficial" (estado vivo = ultimo)
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(codigo_nuevo, f, ensure_ascii=False, indent=2)

    # b) Guardamos una copia versionada como respaldo historico.
    #    Buscamos el proximo numero de generacion libre (gen1, gen2...).
    n = 1
    while os.path.exists(f"codigo_gen{n}.json"):
        n += 1
    with open(f"codigo_gen{n}.json", "w", encoding="utf-8") as f:
        json.dump(codigo_nuevo, f, ensure_ascii=False, indent=2)

    # Reporte de evolucion: cuanto crecio
    antes = len(codigo_previo)
    ahora = len(codigo_nuevo)
    print(f"\n[OK] Idioma actualizado: {antes} -> {ahora} simbolos.")
    print(f"     Guardado en {ARCHIVO} y respaldo en codigo_gen{n}.json")