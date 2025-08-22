# Reto técnico MeLi: Proposta Desafio - Desenvolvedor - IA

## Stack

| Technology | Url Logo                                                                                                                                              |
|------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| Langgraph  | [![Langgraph](https://uploads-ssl.webflow.com/65ff950538088944d66126b3/662ef3209b872e92e41212f6_cookieicon.png)](https://www.langchain.com/langgraph) |
| Langgraph  | [![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg)](https://scikit-learn.org/)                                                |
| Python     | [![Python](https://img.shields.io/badge/Python-14354C?style=flat&logo=python&logoColor=white)](https://www.python.org/)                               |
| Streamlit  | [![Streamlit](https://docs.streamlit.io/logo.svg)](https://docs.streamlit.io/)                                                                        |
| FastAPI    | [![FastApi](https://fastapi.tiangolo.com/img/icon-white.svg)](https://fastapi.tiangolo.com/)                                                          |
| FastAPI    | [![Jupyter](https://img.shields.io/badge/jupyter-%23FA0F00.svg)](https://jupyter.org/)                                                                |
| Docker     | [![Docker](https://img.shields.io/badge/docker-%230db7ed.svg)](https://www.docker.com/)                                                               |

Esta guía te ayudará a configurar y ejecutar el proyecto de manera rápida y eficiente. Sigue estos pasos para poner
en marcha un entorno de desarrollo robusto, listo para la acción.

## 🛠️ Requisitos

- Windows, macOS o Linux
- Python 3.11 (recomendado) o compatible
- Verifica tu versión:
    - Windows: `py --version` o `python --version`
    - macOS/Linux: `python3 --version` o `python --version`
- Docker (opcional) si prefieres ejecutar todo el sistema de forma integrada y aislada.

### Nota: Recuerda ejecutar los comandos en la terminal y en la raiz del proyecto.

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

Con tu entorno activo y pip actualizado, instala todas las librerías necesarias para que el proyecto funcione
correctamente.
Estas se encuentran listadas en el archivo requirements.txt.

```bash
pip install -r requirements.txt
```

## 6) 🔑 Configurar variables de entorno

Para que la aplicación se conecte con las herramientas y servicios necesarios,
necesitas configurar tus claves y variables. Crea el archivo `.streamlit/secrets.toml`
con la siguiente información, sustituyendo `<tu_api_key>` con tu clave de API de Gemini.

Ejecuta el siguiente script para crear el archivo:

```bash
python -m scripts.setup_secrets
```

Reemplaza `<tu_api_key>` con tu clave de API de Gemini.

## 7) 🦾 Ejecutar scripts para descargar y preprocesar los datos

Ejecuta estos scripts para preparar el proyecto. El proceso descarga y limpia el conjunto de datos,
y luego entrena los modelos de IA, dejándolos listos para ser utilizados por la API.

```bash
python -m scripts.load_dataset
python -m scripts.train_models
```

---

# Probar aplicaciones

Aquí ya puedes probar tus aplicaciones. Tienes varias opciones para ejecutar los distintos componentes
del proyecto, según tu preferencia:

- Ejecutar de forma individual el API, el cliente y los agentes. Puedes levantar cada aplicación de forma separada,
  para pruebas más controladas y ajustes que desees aplicar.

- Ejecutar todo el sistema de forma dockerizada, ya sea:

    - Todo en un único contenedor y una instancia, si prefieres una ejecución integrada.
    - Por contenedor separando cada app en una instancia.

Esto te permite flexibilidad para realizar pruebas según el entorno o flujo que necesites validar.

## 🐳 Opción 1: Dockerización (recomendada para pruebas y producción)

Para ejecutar las aplicaciones dentro de contenedores Docker, hay dos maneras de hacerlo:

### 1) Dockerfile para Streamlit + FastAPI (Parecido a ejecutar todo en una sola máquina)

Esto ejecuta el archivo `Dockerfile` con la configuración de `supervisord.conf`
para iniciar tanto FastAPI como Streamlit **_en un solo contenedor y una sola máquina_**.

```bash
docker build -t rba-anomaly-dashboard .
```

Luego ejecuta

```bash
docker run -p 8501:8501 -p 4200:4200 rba-anomaly-dashboard
```

### 2) Docker compose para Streamlit + FastAPI (Parecido a ejecutar cada app en instancias)

Esto ejecuta el archivo `docker-compose.yml` para iniciar un contenedor con FastAPI y Streamlit
**_en un solo contenedor y dos instancias_**.

```bash
docker-compose build
```

Luego ejecuta

```bash
docker-compose up -d
```

## Opción 2: Ejecutar de manera individual (recomendada para pruebas y desarrollo)

### 1) 🌐 Ejecutar la API (individual)

Con el entorno virtual activo, puedes lanzar el servidor de la API.
Esta es la parte central del proyecto, que manejará la lógica de la aplicación.

```bash
uvicorn app.api:app --reload --port 4200
```

### 2) 🖥️ Ejecutar la aplicación cliente (individual)

Abre una nueva ventana de tu terminal, asegúrate de que el entorno virtual esté activo y ejecuta el cliente de
Streamlit.
Aquí es donde verás la interfaz de usuario.

```bash
streamlit run app/client.py
```

Nota: Es crucial que utilices el entorno virtual para este comando.

### 3) (Opcional) 🧠 Ejecutar langgraph para analizarlo el flujo de agentes (individual)

Si quieres explorar el flujo de agentes de la IA, ejecuta este comando. Te permitirá visualizar cómo está construido el
grafo, qué datos se necesitan y cómo se comunican los agentes entre sí.

```bash
langgraph dev
```
