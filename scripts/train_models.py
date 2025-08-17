import pandas as pd
import joblib
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from xgboost import XGBClassifier


def preprocess_data(df):
    features = df[['Country', 'Region', 'City', 'Device Type', 'Is Attack IP']].copy()
    target = df['Is Account Takeover'].astype(int)

    categorical_cols = ['Country', 'Region', 'City', 'Device Type']
    label_encoders = {}

    for col in categorical_cols:
        le = LabelEncoder()
        features[col] = le.fit_transform(features[col].astype(str))
        label_encoders[col] = le

    return features, target, label_encoders


def train_isolation_forest(X_train, X_test, y_test):
    print("\nTraining Isolation Forest...")
    modelIF = IsolationForest(contamination=0.05, random_state=42, n_jobs=-1)
    modelIF.fit(X_train)

    y_pred = modelIF.predict(X_test)
    y_pred = [1 if x == -1 else 0 for x in y_pred]

    print("\nIsolation Forest Results:")
    print(classification_report(y_test, y_pred, target_names=['Normal', 'Anomaly']))
    print(f"Accuracy: {100 *accuracy_score(y_test, y_pred):.4f}")

    return modelIF


def train_random_forest(X_train, X_test, y_train, y_test):
    print("\nTraining Random Forest...")
    modelRFC = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1,
        class_weight='balanced'
    )
    modelRFC.fit(X_train, y_train)

    y_pred = modelRFC.predict(X_test)

    print("\nRandom Forest Results:")
    print(classification_report(y_test, y_pred, target_names=['Normal', 'Anomaly']))
    print(f"Accuracy: {100 * accuracy_score(y_test, y_pred):.4f}")

    return modelRFC


def train_xgboost(X_train, X_test, y_train, y_test):
    print("\nTraining XGBoost...")
    modelXGB = XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        n_jobs=-1,
        scale_pos_weight=sum(y_train == 0) / sum(y_train == 1)
    )
    modelXGB.fit(X_train, y_train)

    y_pred = modelXGB.predict(X_test)

    print("\nXGBoost Results:")
    print(classification_report(y_test, y_pred, target_names=['Normal', 'Anomaly']))
    print(f"Accuracy: {100 *accuracy_score(y_test, y_pred):.4f}")

    return modelXGB


def save_model(model, model_name, label_encoders):
    output_dir = Path(__file__).parent.parent / 'model'
    output_dir.mkdir(parents=True, exist_ok=True)

    model_path = output_dir / f'{model_name}.pkl'
    joblib.dump(model, model_path)

    if label_encoders:
        encoders_path = output_dir / f'{model_name}_label_encoders.pkl'
        joblib.dump(label_encoders, encoders_path)

    print(f"\nModel and encoders saved to {model_path}")


df = pd.read_csv(Path(__file__).parent.parent / 'data' / 'dataset.csv')
X, y, label_encoders = preprocess_data(df)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print(f"Training data shape: {X_train.shape}")
print(f"Test data shape: {X_test.shape}")
print(f"Class distribution in training set: {np.bincount(y_train)}")
print(f"Class distribution in test set: {np.bincount(y_test)}")

models = {
    'isolation_forest': train_isolation_forest(X_train, X_test, y_test),
    'random_forest': train_random_forest(X_train, X_test, y_train, y_test),
    'xgboost': train_xgboost(X_train, X_test, y_train, y_test),
}

for name, model in models.items():
    save_model(model, name, label_encoders if name != 'isolation_forest' else None)
