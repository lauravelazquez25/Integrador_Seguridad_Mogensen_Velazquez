# dialogo_idioma.py
# Paso 3: A y B conversan de ida y vuelta, recordando lo dicho,
#         con la consigna de ir inventando un codigo compartido.

from openai import OpenAI

cliente = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="lm-studio")

MODELO_A = "llama-3.2-3b-instruct"
MODELO_B = "google/gemma-3-4b"   # usa el identificador EXACTO de tu LM Studio

# --- Instruccion de rol (system) para cada IA ---
SYSTEM_A = (
    "Sos la IA 'A' y conversas con otra IA llamada 'B'. "
    "El objetivo comun es inventar entre las dos un codigo propio y compacto "
    "para comunicarse, que ambas entiendan. Propone simbolos o abreviaturas "
    "y usa las que ya acordaron. Responde breve."
)
SYSTEM_B = SYSTEM_A.replace("IA 'A'", "IA 'B'").replace("llamada 'B'", "llamada 'A'")

# --- Dos historiales separados: cada IA ve la charla desde SU lugar ---
# "assistant" = lo que dijo ESA ia | "user" = lo que le llega de la otra
historial_A = [{"role": "system", "content": SYSTEM_A}]
historial_B = [{"role": "system", "content": SYSTEM_B}]

# Empujon inicial: a A le llega un primer mensaje (como "user") al que responder.
arranque = "Hola. Propongamos un codigo para entendernos de forma compacta. Empeza vos."
historial_A.append({"role": "user", "content": arranque})

TURNOS = 4  # cuantas idas y vueltas

for i in range(TURNOS):
    # --- Habla A ---
    r_A = cliente.chat.completions.create(model=MODELO_A, messages=historial_A)
    texto_A = r_A.choices[0].message.content
    print(f"\nA (Llama) [{i+1}]: {texto_A}")
    historial_A.append({"role": "assistant", "content": texto_A})  # para A, es ELLA
    historial_B.append({"role": "user",      "content": texto_A})  # para B, le llega

    # --- Habla B ---
    r_B = cliente.chat.completions.create(model=MODELO_B, messages=historial_B)
    texto_B = r_B.choices[0].message.content
    print(f"B (Gemma) [{i+1}]: {texto_B}")
    historial_B.append({"role": "assistant", "content": texto_B})  # para B, es ELLA
    historial_A.append({"role": "user",      "content": texto_B})  # para A, le llega

print("\n--- Fin de la conversacion ---")