import pandas as pd
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.ensemble import IsolationForest
import json


def save_feature_columns(cols):
    output_dir = Path(__file__).parent.parent / 'models'
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / 'feature_columns.json', 'w', encoding='utf-8') as f:
        json.dump(cols, f, ensure_ascii=False, indent=2)
    print(f"Columnas de features guardadas en {output_dir / 'feature_columns.json'}")


def preprocess_data(df: pd.DataFrame):
    cols_to_drop = ['Is Attack IP']
    cols_to_drop = [c for c in cols_to_drop if c in df.columns]

    features = df.drop(columns=cols_to_drop, axis=1)
    target = df['Is Attack IP']

    X_train, X_test, y_train, y_test = train_test_split(
        features, target, test_size=0.2, random_state=42, stratify=target
    )

    print("\n")
    print(f"Total datos: {df.shape[0]}")
    print(f"Datos de entrenamiento: {X_train.shape[0]}")
    print(f"Datos de prueba: {X_test.shape[0]}")

    feature_cols = features.columns.tolist()
    return X_train, X_test, y_train, y_test, feature_cols


def train_isolation_forest(X_train, y_train, X_test, y_test):
    print("\nEntrenando Isolation Forest...")

    X_fit = X_train[y_train == 0]

    model = IsolationForest(contamination=0.05, random_state=42, n_jobs=-1)
    model.fit(X_fit)  # <- sin y

    y_pred = model.predict(X_test)
    y_pred = [1 if x == -1 else 0 for x in y_pred]

    print("\nResultados de Isolation Forest:")
    print(classification_report(y_test, y_pred, target_names=['Normal', 'Anomalía'], zero_division=0))
    print(f"Precisión: {100 * accuracy_score(y_test, y_pred):.4f}%")

    return model


def save_model(model, model_name):
    # Crear directorio de salida si no existe
    output_dir = Path(__file__).parent.parent / 'models'
    output_dir.mkdir(parents=True, exist_ok=True)

    # Guardar el modelo
    model_path = output_dir / f'{model_name}.pkl'
    joblib.dump(model, model_path)

    print("\n")
    print(f"Modelo guardado en {model_path}")


try:
    # 1. Cargar los datos
    data_path = Path(__file__).parent.parent / 'data' / 'dataset.csv'
    print(f"Cargando datos desde: {data_path}")
    df = pd.read_csv(data_path)

    # 2. Pre-procesar los datos
    X_train, X_test, y_train, y_test, feature_cols = preprocess_data(df)

    # 3. Entrenar los modelos
    print("\n")
    print("Iniciando entrenamiento de modelos...")
    models = {
        'isolation_forest': train_isolation_forest(X_train, y_train, X_test, y_test),
    }

    # 4. Guardar solo los modelos que se entrenaron correctamente
    for name, model in models.items():
        save_model(model, name)

    # 5. Guardar las columnas de features
    save_feature_columns(feature_cols)


except Exception as e:
    print("\n")
    print(f"Ocurrió un error: {str(e)}")
    raise
