import pandas as pd
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.ensemble import IsolationForest


def preprocess_data(df: pd.DataFrame):
    features = df.drop(['Is Attack IP', 'Is Account Takeover'], axis=1)
    target = df['Is Account Takeover']

    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42,
                                                        stratify=target)

    print("\n")
    print(f"Total datos: {df.shape[0]}")
    print(f"Datos de entrenamiento: {X_train.shape[0]}")
    print(f"Datos de prueba: {X_test.shape[0]}")

    return X_train, X_test, y_train, y_test


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
    output_dir = Path(__file__).parent.parent / 'model'
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
    X_train, X_test, y_train, y_test = preprocess_data(df)

    # 3. Entrenar los modelos
    print("\n")
    print("Iniciando entrenamiento de modelos...")
    models = {
        'isolation_forest': train_isolation_forest(X_train, y_train, X_test, y_test),
    }

    # 4. Guardar solo los modelos que se entrenaron correctamente
    for name, model in models.items():
        save_model(model, name)


except Exception as e:
    print("\n")
    print(f"Ocurrió un error: {str(e)}")
    raise
