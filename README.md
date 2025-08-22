# meli-thecnical-test-security-and-ai

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

Si tienes un archivo `requirements.txt` en la raíz del proyecto:

```bash
pip install -r requirements.txt
```
