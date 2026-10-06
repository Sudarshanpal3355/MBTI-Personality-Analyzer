import json
import os

models = {
    "LSTM": "lstm_metrics.json",
    "BiLSTM": "bilstm_metrics.json",
    "CNN": "cnn_metrics.json",
    "Transformer": "transformer_metrics.json",
    "CNN-BiLSTM": "cnn_bilstm_metrics.json"
}

print("\n" + "=" * 75)
print("             MBTI MODEL PERFORMANCE COMPARISON")
print("=" * 75)

print(f"{'Model':<15}{'Accuracy':>15}{'Precision':>15}{'Recall':>15}{'F1-Score':>15}")
print("-" * 75)

results = {}

for model_name, filename in models.items():

    path = os.path.join("models", filename)

    with open(path, "r") as file:
        data = json.load(file)

    macro = data["macro"]

    accuracy = macro["accuracy"] * 100
    precision = macro["precision"] * 100
    recall = macro["recall"] * 100
    f1 = macro["f1"] * 100

    results[model_name] = {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1
    }

    print(
        f"{model_name:<15}"
        f"{accuracy:>14.2f}%"
        f"{precision:>14.2f}%"
        f"{recall:>14.2f}%"
        f"{f1:>14.2f}%"
    )

print("-" * 75)

best_model = max(results, key=lambda x: results[x]["f1"])

print(f"\nBest Model based on F1-Score: {best_model}")
print(f"F1-Score: {results[best_model]['f1']:.2f}%")
print(f"Accuracy: {results[best_model]['accuracy']:.2f}%")

print("=" * 75)