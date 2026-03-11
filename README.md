# SIMPLE VECTOR STORE

CLI para indexar documentos `.txt` en una base vectorial (ChromaDB) y consultarlos por similitud semántica.

## ¿Para qué sirve?

Esta app permite:

- **Sincronizar textos** desde la carpeta `documents/`.
- **Dividirlos en fragmentos** automáticamente.
- **Vectorizarlos** (embeddings) y guardarlos en una vectorstore.
- **Buscar en modo chat** los fragmentos más relacionados con el texto que escribas.

No es un chatbot conversacional todavía: actualmente el modo `chat` devuelve resultados de búsqueda semántica (top resultados más cercanos).

---

## Requisitos

- Python 3.10+
- Un proveedor/modelo de embeddings compatible con la API de OpenAI (OpenAI, LM Studio, Grok, etc.)

---

## Configuración del proyecto

### 1) Crear y activar entorno virtual

En Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

En Windows (PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2) Instalar dependencias

Como no hay `requirements.txt` todavía, instala las librerías usadas por la app:

```bash
pip install chromadb openai python-dotenv
```

### 3) Crear archivo `.env`

Copia el ejemplo y edítalo:

```bash
cp .env.example .env
```

Variables importantes:

- `SCAPE_KEYWORD`: palabra/comando para salir del modo `chat` (ejemplo: `/bye`).
- `VECTORSTORE_PATH`: nombre/ruta de la vectorstore y colección de Chroma.
  - Puedes cambiarlo para tener **distintas bases de datos vectoriales**.
- `MULTI_PROCESSING_LIMIT`: cantidad máxima de fragmentos que se embeben en paralelo.
  - Mayor valor = más concurrencia (si tu proveedor/PC lo soporta).
- `EMBEDDING_MODEL`, `EMBEDDING_API_KEY`, `EMBEDDING_BASE_URL`: configuración del modelo de embeddings.

En `.env.example` ya hay bloques para descomentar según proveedor (LM Studio, Grok, OpenAI).

> Nota: también aparecen variables `CHAT_MODEL`, `CHAT_API_KEY` y `CHAT_BASE_URL`, pero el flujo actual todavía no usa respuesta de chat como feature principal; por ahora el modo `chat` se centra en búsqueda semántica por vectores.

---

## Uso

### Ejecutar la app

```bash
python main.py
```

Verás un menú con opciones:

- `chat`
- `sync`
- `exit`

### Modo `sync`

1. Lista los archivos `.txt` disponibles dentro de `documents/`.
2. Eliges uno.
3. El texto se divide en múltiples fragmentos.
4. Cada fragmento se vectoriza (embeddings).
5. Se guardan/actualizan en la vectorstore.

Después de esto, esos fragmentos ya aparecen en las búsquedas del modo `chat`.

### Modo `chat`

1. Te pide que escribas un texto.
2. Genera embedding de tu consulta.
3. Busca en la vectorstore los fragmentos más relacionados por similitud vectorial.
4. Muestra los resultados más cercanos.

Para terminar el modo `chat`, escribe el valor de `SCAPE_KEYWORD` (por ejemplo, `/bye`).

---

## Estructura rápida

- `main.py`: menú principal y flujos `chat` / `sync`.
- `vectorstore.py`: división de texto, embeddings concurrentes y operaciones ChromaDB.
- `ai.py`: cliente OpenAI-compatible para embeddings.
- `config.py`: lectura de variables de entorno.
- `documents/`: textos fuente `.txt` para sincronizar.

---

## Próximos pasos sugeridos

- Agregar `requirements.txt` para instalación reproducible.
- Incorporar el uso completo de `CHAT_MODEL` en un flujo conversacional real (RAG + generación).
