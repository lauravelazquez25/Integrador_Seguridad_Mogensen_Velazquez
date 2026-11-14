# Integrador de Seguridad — Comunicación entre IAs y análisis de vulnerabilidades

Trabajo Práctico Integrador — **Seguridad Informática (2026)**

Proyecto que instala **tres modelos de IA locales** para dos experimentos:
1. Que dos de ellas (A y B) desarrollen, conversando, un **código de comunicación propio, mutuamente entendible y que evoluciona con el uso**.
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

## Parte 1 — El idioma entre A y B

El código no se impone: **emerge** de la conversación entre A y B, se **persiste** en disco y **evoluciona** cuando enfrenta necesidades nuevas.

### Cómo funciona
1. **Generación del código:** A y B conversan con una necesidad comunicativa concreta (ej.: coordinar un encuentro) e inventan símbolos para cubrirla.
2. **Captura:** una de ellas redacta la tabla final en un formato con marcas (`===TABLA_INICIO===` / `===TABLA_FIN===`); el programa la recorta y la guarda como diccionario en `codigo_acordado.json`.
3. **Evolución:** se relee el código existente, se lo inyecta a ambas IAs, se les da una **necesidad nueva** (ej.: avisar emergencias / cancelar) y suman símbolos. Cada generación se respalda en `codigo_genN.json`.

### Resultados observados
- El código **emerge** por presión comunicativa (los símbolos nacen de lo que necesitan decir).
- El idioma es **acumulativo**: al evolucionar, conserva el vocabulario previo y suma el nuevo (verificado: 3 → 6 símbolos entre la gen 0 y la gen 1).
- El comportamiento es **no determinista**: distintas corridas producen códigos distintos (siglas, símbolos visuales, etc.), y a veces la tabla declarada no coincide del todo con el uso real (inestabilidad típica de modelos chicos).

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

### 4. Correr los experimentos
```bash
python hello.py              # prueba de conexión
python helloAB.py            # primer diálogo A-B (una ronda)
python dialogo_idioma.py     # diálogo A-B con memoria
python idioma_gen.py         # genera un código desde cero y lo guarda
python idioma_evolucion.py   # evoluciona el código existente (suma símbolos)
```

---

## Estructura del repositorio

| Archivo | Descripción |
|---------|-------------|
| `hello.py` | Prueba de conexión: un mensaje a un modelo vía LM Studio. |
| `helloAB.py` | Primer diálogo de una ronda entre A y B. |
| `dialogo_idioma.py` | Diálogo A↔B con memoria (dos historiales separados). |
| `idioma_gen.py` | Genera un código desde cero, lo captura y lo guarda en JSON. |
| `idioma_evolucion.py` | Lee el código previo, lo hace evolucionar y versiona cada generación. |
| `codigo_acordado.json` | Estado vivo del idioma (última versión acordada). |
| `codigo_genN.json` | Respaldo de cada generación (para comparar la evolución). |
| `corridas.md` | Bitácora de corridas y observaciones. |
| `.gitignore` | Archivos excluidos del repo (entorno, cachés, logs). |

---

## Estado del proyecto

### Parte 1 — El idioma
- [x] Conexión Python ↔ LM Studio
- [x] Diálogo A↔B de una ronda
- [x] Diálogo A↔B con memoria
- [x] Generación del código con captura a archivo
- [x] Persistencia del idioma en JSON
- [x] Evolución del idioma con versionado por generación
- [ ] Test formal de comprensión mutua (métrica)

### Parte 2 — El ataque
- [ ] Configuración de la IA C (rol + dato reservado)
- [ ] Script de ataque (prompt injection)
- [ ] Corridas con registro de intentos

### Cierre
- [ ] Video y presentación

---

## Integrantes

- **Laura Velazquez** — [@lauravelazquez25](https://github.com/lauravelazquez25)
- **Cristian Mogensen** — [@CristianMogensen](https://github.com/CristianMogensen)

---
