import os
import platform
from pathlib import Path


def main():
    base_dir = Path(__file__).parent.parent
    secrets_dir = base_dir / ".streamlit"
    secrets_file = secrets_dir / "secrets.toml"
    example_file = secrets_dir / "secrets.example.toml"

    secrets_dir.mkdir(exist_ok=True)

    if not example_file.exists():
        with open(example_file, 'w', encoding='utf-8') as f:
            f.write('DATASET_CHUNK_SIZE = "1000000"  \n')
            f.write('GEMINI_API_KEY = "<tu_api_key>"\n')
            f.write('GEMINI_MODEL = "gemini-2.5-flash"\n')
        print(f"✅ Se ha creado el archivo de ejemplo: {example_file}")

    if secrets_file.exists():
        print(f"⚠️  El archivo {secrets_file} ya existe.")
        overwrite = input("¿Deseas sobrescribirlo? (s/n): ").strip().lower()
        if overwrite != 's':
            print("Operación cancelada.")
            return

    try:
        with open(example_file, 'r', encoding='utf-8') as src, \
                open(secrets_file, 'w', encoding='utf-8') as dst:
            dst.write(src.read())

        print(f"✅ Se ha creado/actualizado el archivo: {secrets_file}")
        print("\nPor favor, edita el archivo y reemplaza las claves de ejemplo con tus propias credenciales.")

        if platform.system() == 'Windows':
            os.system(f'notepad "{secrets_file}"')
        elif platform.system() == 'Darwin':
            os.system(f'open -t "{secrets_file}"')
        else:
            os.system(f'xdg-open "{secrets_file}"')

    except Exception as e:
        print(f"❌ Error al crear el archivo: {e}")


if __name__ == "__main__":
    print("🔧 Configuración de variables de entorno")
    print("=" * 50)
    main()
