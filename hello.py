# hola_mundo.py
# Objetivo: confirmar que Python puede hablarle a LM Studio.

# 1) Traemos el cliente de la librería openai (la que instalaste con pip).
from openai import OpenAI

# 2) Creamos el cliente, pero apuntándolo a TU LM Studio, no a internet:
#    - base_url: la dirección de tu servidor local (ojo el /v1 al final)
#    - api_key: el servidor local la ignora, así que va cualquier texto
cliente = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio",
)

# 3) Enviamos un mensaje y guardamos lo que devuelve.
#    - model: el identificador EXACTO que viste en LM Studio
#    - messages: la conversación; por ahora, un solo mensaje nuestro ("user")
respuesta = cliente.chat.completions.create(
    model="llama-3.2-3b-instruct",
    messages=[
        {"role": "user", "content": "¿Cuál es la capital de Francia?"},
    ],
)

# 4) La respuesta trae mucha info metida en una estructura.
#    El texto del modelo está en este "camino": choices[0].message.content
texto = respuesta.choices[0].message.content

# 5) Lo mostramos en pantalla.
print(texto)