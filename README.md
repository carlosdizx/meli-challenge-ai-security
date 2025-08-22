# Reto técnico MeLi - Proposta Desafio - Desenvolvedor - IA - ES

Guía para crear y usar un entorno virtual (.venv) y configurar el intérprete.

## Requisitos

- Windows, macOS o Linux
- Python 3.12 (recomendado) o compatible
- Verifica tu versión:
    - Windows: `py --version` o `python --version`
    - macOS/Linux: `python3 --version` o `python --version`

## 1) Crear el entorno virtual

En la raíz del proyecto, ejecuta:

```bash
# Comando general (todas las plataformas)
python -m venv .venv
```

## 2) Activar el entorno virtual

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

## 3) Verificar la versión de Python del entorno

```bash
# Windows
.\.venv\Scripts\python.exe --version
```

```bash
# macOS/Linux
.venv/bin/python --version
```

## 4) Actualizar pip

```bash
python -m pip install --upgrade pip
```

## 5) Instalar dependencias

Instala todas las librerías necesarias para ejecutar scripts, entrenar modelos y ejecutar las aplicaciones.

```bash
pip install -r requirements.txt
```

## 6) Ejecutar scripts para descargar y preprocesar los datos

```bash
python -m scripts.load_dataset
python -m scripts.train_models
```
Esto descarga, limpia los datos y entrena los modelos, dejándolos listos para usar en la API.

## 7) Configurar variables de entorno

Crea el archivo `.streamlit/secrets.toml` con los valores necesarios:

```toml
DATASET_CHUNK_SIZE = "1000000"     # Tamaño del chunk para el dataset
GEMINI_API_KEY = "<tu_api_key>"
GEMINI_MODEL = "gemini-2.5-flash"  # ejemplo
```

## 8) Ejecutar la API

Con el entorno virtual activo, inicia el servidor de FastAPI:

```bash
uvicorn app.api:app --reload --port 4200
```

## 9) Ejecutar la aplicación cliente

En otra ventana de tu terminal, ejecuta:

```bash
streamlit run app/client.py
```
Nota: Recuerda usar el entorno virtual para ejecutar la app de streamlit.

## 10) (Opcional) Ejecutar langgraph para analizarlo el flujo de agentes
Aquí podrás ver como está construido el grafo de agentes, qué datos necesitan para funcionar y como se comunican entre ellos.

```bash
langgraph dev
```

