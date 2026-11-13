# dialogo_simple.py
# Objetivo: que un modelo (A=Llama) le hable a otro (B=Gemma), una sola ronda.


from openai import OpenAI

# El cliente es el mismo para los dos modelos: el servidor de LM Studio es uno solo.
cliente = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio",
)

# Guardamos los identificadores en variables, así el código queda más claro
# y si cambian, los tocás en un solo lugar.
MODELO_A = "llama-3.2-3b-instruct"   # IA A
MODELO_B = "google/gemma-3-4b"           # IA B  <-- CONFIRMÁ que sea EXACTO al de LM Studio

# --- Turno de A (Llama) ---
# Le pedimos a A que diga una frase para arrancar la conversación.
respuesta_A = cliente.chat.completions.create(
    model=MODELO_A,
    messages=[
        {"role": "user", "content": "Presentate en una sola frase a otra inteligencia artificial."},
    ],
)
# Sacamos el texto de A, igual que en el hola mundo.
mensaje_de_A = respuesta_A.choices[0].message.content

# --- Turno de B (Gemma) ---
# EL ENGANCHE: lo que dijo A entra como el mensaje del "user" para B.
respuesta_B = cliente.chat.completions.create(
    model=MODELO_B,
    messages=[
        {"role": "user", "content": mensaje_de_A},
    ],
)
mensaje_de_B = respuesta_B.choices[0].message.content

# --- Mostramos las dos cosas, con etiqueta para distinguirlas ---
print("A (Llama):", mensaje_de_A)
print()                      # una línea en blanco para que se lea mejor
print("B (Gemma):", mensaje_de_B)