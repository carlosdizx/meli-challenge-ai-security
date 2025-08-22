# Reto técnico MeLi: Proposta Desafio - Desenvolvedor - IA

Esta guía te ayudará a configurar y ejecutar el proyecto de manera rápida y eficiente. 
Sigue estos pasos para poner en marcha un entorno de desarrollo robusto, listo para la acción.

## 🛠️ Requisitos

- Windows, macOS o Linux
- Python 3.11 (recomendado) o compatible
- Verifica tu versión:
    - Windows: `py --version` o `python --version`
    - macOS/Linux: `python3 --version` o `python --version`

Para verificar la versión de Python instalada, abre tu terminal y ejecuta
uno de los siguientes comandos:
- Windows: py --version o python --version 
- macOS/Linux: python3 --version o python --version

## 1) 📦 Crear el entorno virtual

Un entorno virtual aísla las dependencias de tu proyecto, evitando conflictos con otras instalaciones 
de Python. Es una práctica esencial para un desarrollo limpio.

En la raíz del proyecto, ejecuta:

```bash
# Comando general (todas las plataformas)
python -m venv .venv
```

## 2) ▶️ Activar el entorno virtual

Activar el entorno te permitirá usar las librerías específicas del proyecto.
El comando varía según tu sistema operativo y el shell que uses:

- Windows (PowerShell):
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
- Windows (CMD):
  ```cmd
  .venv\Scripts\activate.bat
  ```
- macOS/Linux (Bash/Zsh):
  ```bash
  source .venv/bin/activate
  ```
- macOS/Linux (Fish):
  ```fish
  source .venv/bin/activate.fish
  ```

## 3) 🐍 Verificar la versión de Python del entorno

Una vez activado el entorno, confirma que estás utilizando el intérprete correcto:

```bash
# Windows
.\.venv\Scripts\python.exe --version
```

```bash
# macOS/Linux
.venv/bin/python --version
```

## 4) ⚙️ Actualizar pip

```bash
python -m pip install --upgrade pip
```

## 5) ✨ Instalar dependencias

Con tu entorno activo y pip actualizado, instala todas las librerías necesarias para que el proyecto funcione correctamente.
Estas se encuentran listadas en el archivo requirements.txt.

```bash
pip install -r requirements.txt
```

## 6) 🔑 Configurar variables de entorno

Para que la aplicación se conecte con las herramientas y servicios necesarios,
necesitas configurar tus claves y variables. Crea el archivo `.streamlit/secrets.toml`
con la siguiente información, sustituyendo `<tu_api_key>` con tu clave de API de Gemini.

Copia el nombre del siguiente archivo y créalo:
```bash
python -m scripts.setup_secrets
```

Copia el siguiente contenido en el archivo creado y reemplaza `<tu_api_key>` con tu clave de API de Gemini y los valores
que desees.

```toml
DATASET_CHUNK_SIZE = "1000000"     # Tamaño del chunk para el dataset
GEMINI_API_KEY = "<tu_api_key>"
GEMINI_MODEL = "gemini-2.5-flash"  # ejemplo
```

## 7) 🦾 Ejecutar scripts para descargar y preprocesar los datos

Ejecuta estos scripts para preparar el proyecto. El proceso descarga y limpia el conjunto de datos,
y luego entrena los modelos de IA, dejándolos listos para ser utilizados por la API.


```bash
python -m scripts.load_dataset
python -m scripts.train_models
```

## 8) 🌐 Ejecutar la API

Con el entorno virtual activo, puedes lanzar el servidor de la API.
Esta es la parte central del proyecto, que manejará la lógica de la aplicación.

```bash
uvicorn app.api:app --reload --port 4200
```

## 9) 🖥️ Ejecutar la aplicación cliente

Abre una nueva ventana de tu terminal, asegúrate de que el entorno virtual esté activo y ejecuta el cliente de Streamlit.
Aquí es donde verás la interfaz de usuario.

```bash
streamlit run app/client.py
```
Nota: Es crucial que utilices el entorno virtual para este comando.

## 10) (Opcional) 🧠 Ejecutar langgraph para analizarlo el flujo de agentes

Si quieres explorar el flujo de agentes de la IA, ejecuta este comando. Te permitirá visualizar cómo está construido el
grafo, qué datos se necesitan y cómo se comunican los agentes entre sí.

```bash
langgraph dev
```

## 11) (Opcional) 🐳 Dockerización

Para ejecutar las aplicaciones dentro de contenedores Docker, hay dos maneras de hacerlo:

### 11.1) Dockerfile para Streamlit + FastAPI (Parecido a ejecutar todo en una sola máquina)

Esto ejecuta el archivo `Dockerfile` con la configuración de `supervisord.conf`
para iniciar tanto FastAPI como Streamlit **_en un solo contenedor y una sola máquina_**.

```bash
docker build -t rba-anomaly-dashboard .
```

Luego ejecuta

```bash
docker run -p 8501:8501 -p 4200:4200 rba-anomaly-dashboard
```

### 11.2) Docker compose para Streamlit + FastAPI (Parecido a ejecutar cada app en una máquina)

Esto ejecuta el archivo `docker-compose.yml` para iniciar un contenedor con FastAPI y Streamlit
**_en un solo contenedor y dos máquinas_**.

```bash
docker-compose build
```

Luego ejecuta

```bash
docker-compose up -d
```
