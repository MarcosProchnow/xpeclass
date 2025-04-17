import os
from flask import Flask, jsonify, request, abort
import seaborn as sns
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from dotenv import load_dotenv

load_dotenv() # Carregar variáveis do arquivo .env

app = Flask(__name__)

# Carregar o dataset Iris
iris = sns.load_dataset('iris')

# Recuperar o token de autenticação da variável de ambiente
VALID_TOKEN = os.getenv("VALID_TOKEN")

# Função de treinamento
def train_model():
    # Dividir os dados em X (features) e y (label)
    X = iris.drop(columns='species')
    y = iris['species']

    # Divisão em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Modelo: Random Forest
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Predição
    y_pred = model.predict(X_test)

    # Avaliação do modelo
    report = classification_report(y_test, y_pred, output_dict=True)
    accuracy = accuracy_score(y_test, y_pred)

    return {"classification_report": report, "accuracy": accuracy}

# Endpoint único para treinamento
@app.route("/train", methods=["GET"])
def train():
    # Verificar o token no parâmetro "params"
    token = request.args.get("token")
    if not token or token != VALID_TOKEN:
        abort(401, description="Unauthorized: Invalid or missing token")

    # Processar o treinamento se o token for válido
    training_results = train_model()
    return jsonify(training_results)

if __name__ == "__main__":
    app.run(debug=True)
