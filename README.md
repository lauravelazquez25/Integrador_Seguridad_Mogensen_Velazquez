# Integrador de Seguridad — Comunicación entre IAs y análisis de vulnerabilidades

Trabajo Práctico Integrador — **Seguridad Informática (2026)**

Proyecto que instala **tres modelos de IA locales** para dos experimentos:
1. Que dos de ellas (A y B) desarrollen, conversando, un **código de comunicación propio y mutuamente entendible**.
2. **Encontrar y explotar una vulnerabilidad de comportamiento** en la tercera (C), mediante técnicas de *prompt injection*.

> **Entrega:** 16/11/2026
> **Entregables:** video explicativo en YouTube · código fuente (este repositorio) · presentación.

---

## Consigna (resumen)

- Instalar tres IAs locales.
- **Parte 1 — El idioma:** las IA **A** y **B** dialogan y acuerdan un código propio; luego se verifica que efectivamente se entienden entre ellas.
- **Parte 2 — El ataque:** a la IA **C** se le asigna un rol y un dato reservado, y se la ataca por su comportamiento para que rompa el rol o filtre información.
- Todo el proceso queda documentado y filmado. Si no se llega a una conclusión, también se documenta.

---

## Stack

- **LM Studio** — sirve los modelos mediante un servidor local compatible con la API de OpenAI (`http://127.0.0.1:1234/v1`).
- **Python 3** + librería **`openai`** (como cliente del servidor local).
- **Git / GitHub** para control de versiones.

## Roles de las IAs

| IA | Modelo | Función |
|----|--------|---------|
| **A** | Llama 3.2 3B Instruct | Dialoga con B (modelo directo) |
| **B** | Gemma 3 4B | Dialoga con A (modelo directo) |
| **C** | Qwen3-4B-2507-Instruct | Objetivo del análisis de seguridad |

---

## Puesta en marcha

### 1. Clonar el repositorio
```bash
git clone https://github.com/lauravelazquez25/Integrador_Seguridad_Mogensen_Velazquez.git
cd Integrador_Seguridad_Mogensen_Velazquez
```

### 2. Crear el entorno de Python e instalar dependencias
```bash
python3 -m venv mi_entorno_ia
source mi_entorno_ia/bin/activate
pip install openai
```
> El entorno virtual es propio de cada máquina y está excluido del repo (ver `.gitignore`). Cada integrante crea el suyo.

### 3. Levantar LM Studio
1. Descargar los modelos de la tabla de roles (cuantización **Q4_K_M**).
2. En la pestaña **Developer**, cargar los modelos y presionar **Start Server**.
3. Verificar el servidor y los identificadores exactos de los modelos:
```bash
curl http://127.0.0.1:1234/v1/models
```
> Los identificadores que arroja ese comando son los que van en el campo `model` de cada script.

---

## Estructura del repositorio

| Archivo | Descripción |
|---------|-------------|
| `hello.py` | Prueba de conexión: un mensaje a un modelo vía LM Studio. |
| `helloAB.py` | Primer diálogo de una ronda entre A y B. |
| `.gitignore` | Archivos excluidos del repo (entorno, cachés, logs). |
| _(próximamente)_ `dialogo_idioma.py` | Diálogo A↔B con memoria — construcción del código común. |

---

## Estado del proyecto

- [x] Conexión Python ↔ LM Studio
- [x] Diálogo A↔B de una ronda
- [x] Repositorio inicial y colaboración
- [ ] Diálogo A↔B con memoria (código común)
- [ ] Verificación de comprensión mutua del código
- [ ] Configuración de la IA C (rol + dato reservado)
- [ ] Script de ataque (prompt injection)
- [ ] Corridas con registro (logs)
- [ ] Video y presentación

---

## Integrantes

- **Laura Velazquez** — [@lauravelazquez25](https://github.com/lauravelazquez25)
- **Cristian Mogensen** — [@CristianMogensen](https://github.com/CristianMogensen)