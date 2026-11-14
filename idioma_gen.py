# idioma_gen.py
# Sub-paso 4A: A y B parten de cero, coordinan un encuentro inventando un codigo,
#              y B redacta la tabla final en un formato capturable.

import json 
from openai import OpenAI

cliente = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="lm-studio")

MODELO_A = "llama-3.2-3b-instruct"
MODELO_B = "google/gemma-3-4b"

# --- El "estado vivo" del idioma ---
# Hoy (generacion 0) arranca vacio. En generaciones futuras, esto se va a
# cargar desde codigo_acordado.json. Por ahora, string vacio = parten de cero.
tabla_actual = ""   # <- aca vivira el idioma acumulado, mas adelante

# --- La necesidad comunicativa (la "presion" que hace nacer los simbolos) ---
MISION = (
    "Deben coordinar un encuentro entre ustedes: acordar un LUGAR, una HORA "
    "y una CONFIRMACION final. No tienen un idioma comun todavia: tienen que "
    "INVENTAR simbolos o abreviaturas para esos conceptos y usarlos."
)

# --- Instruccion de rol para cada IA ---
# Nota: el bloque {tabla} queda listo para inyectar el idioma acumulado en el futuro.
def system_para(nombre, otra):
    base = (
        f"Sos la IA '{nombre}' y te comunicas con la IA '{otra}'.\n"
        f"{MISION}\n"
        "Responde SIEMPRE breve, usando los simbolos que vayan acordando.\n"
    )
    if tabla_actual.strip():
        base += f"\nCodigo ya acordado hasta ahora:\n{tabla_actual}\n"
    return base

SYSTEM_A = system_para("A", "B")
SYSTEM_B = system_para("B", "A")

# --- Dos historiales separados (cada una ve la charla desde su lado) ---
historial_A = [{"role": "system", "content": SYSTEM_A}]
historial_B = [{"role": "system", "content": SYSTEM_B}]

arranque = "Empecemos. Propongamos simbolos para coordinar el encuentro. Arranca vos."
historial_A.append({"role": "user", "content": arranque})

TURNOS = 4
for i in range(TURNOS):
    # Habla A
    r_A = cliente.chat.completions.create(model=MODELO_A, messages=historial_A)
    texto_A = r_A.choices[0].message.content
    print(f"\nA (Llama) [{i+1}]: {texto_A}")
    historial_A.append({"role": "assistant", "content": texto_A})
    historial_B.append({"role": "user",      "content": texto_A})

    # Habla B
    r_B = cliente.chat.completions.create(model=MODELO_B, messages=historial_B)
    texto_B = r_B.choices[0].message.content
    print(f"B (Gemma) [{i+1}]: {texto_B}")
    historial_B.append({"role": "assistant", "content": texto_B})
    historial_A.append({"role": "user",      "content": texto_B})

# --- CIERRE: B redacta la tabla final en formato capturable ---
# Le pedimos SOLO la tabla, con marcas fijas, para poder recortarla despues.
pedido_cierre = (
    "Ahora cerramos. Escribi la tabla final de simbolos que acordaron.\n"
    "REGLAS ESTRICTAS:\n"
    "- Cada linea debe ser: SIMBOLO = significado\n"
    "- El SIMBOLO va SIEMPRE al principio y NO puede estar vacio.\n"
    "- Usa un simbolo o abreviatura concreta (ej: una letra, ~, #, una sigla).\n"
    "- No escribas ningun texto fuera de las marcas.\n\n"
    "Ejemplo EXACTO del formato esperado:\n"
    "===TABLA_INICIO===\n"
    "LUG = lugar del encuentro\n"
    "HR = hora acordada\n"
    "OK = confirmacion final\n"
    "===TABLA_FIN===\n\n"
    "Ahora escribi TU tabla real con los simbolos que acordaron, en ese mismo formato:"
)
historial_B.append({"role": "user", "content": pedido_cierre})
r_cierre = cliente.chat.completions.create(model=MODELO_B, messages=historial_B)
tabla_final = r_cierre.choices[0].message.content

print("\n==================== TABLA FINAL (redactada por B) ====================")
print(tabla_final)

# ============================================================
# 4B: Capturar la tabla y guardarla en codigo_acordado.json
# ============================================================

# --- 1) RECORTAR: quedarnos solo con lo que esta entre las marcas ---
MARCA_INI = "===TABLA_INICIO==="
MARCA_FIN = "===TABLA_FIN==="

# Verificamos que las dos marcas existan antes de recortar.
if MARCA_INI in tabla_final and MARCA_FIN in tabla_final:
    # Tomamos el texto DESPUES de la marca de inicio...
    despues_del_inicio = tabla_final.split(MARCA_INI)[1]
    # ...y de eso, lo que esta ANTES de la marca de fin.
    cuerpo = despues_del_inicio.split(MARCA_FIN)[0]
else:
    # Si B no puso las marcas, avisamos y usamos todo el texto como respaldo.
    print("\n[AVISO] No encontre las marcas; intento parsear todo el texto.")
    cuerpo = tabla_final

# --- 2) PARSEAR: convertir cada linea 'simbolo = significado' en un diccionario ---
codigo = {}  # aca se va a armar el idioma como pares simbolo -> significado

for linea in cuerpo.splitlines():      # recorremos linea por linea
    if "=" in linea:                   # solo nos interesan las que tienen '='
        # split("=", 1) corta en el PRIMER '=' nomas (por si el significado tiene otro)
        partes = linea.split("=", 1)
        simbolo = partes[0].strip()    # .strip() saca espacios sobrantes
        significado = partes[1].strip()
        if simbolo:                    # evitamos lineas vacias o raras
            codigo[simbolo] = significado

# --- 3) GUARDAR: volcar el diccionario al archivo JSON ---
# ensure_ascii=False para que acentos y simbolos raros se guarden bien.
# indent=2 para que el archivo quede legible (sangria de 2 espacios).
with open("codigo_acordado.json", "w", encoding="utf-8") as f:
    json.dump(codigo, f, ensure_ascii=False, indent=2)


# --- 4) CONFIRMAR, con chequeo defensivo ---
if len(codigo) == 0:
    print("\n[!] ATENCION: se capturaron 0 simbolos.")
    print("    La tabla salio vacia o mal formada. Conviene volver a correr")
    print("    el script (los modelos chicos varian entre corridas).")
    print("    NO se piso el archivo anterior: se mantiene lo que ya habia.")
else:
    with open("codigo_acordado.json", "w", encoding="utf-8") as f:
        json.dump(codigo, f, ensure_ascii=False, indent=2)
    print(f"\n[OK] Capturados {len(codigo)} simbolos en codigo_acordado.json")