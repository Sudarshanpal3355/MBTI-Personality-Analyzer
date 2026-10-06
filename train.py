# import os, json, argparse
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score, confusion_matrix
# from tensorflow.keras.preprocessing.text import Tokenizer
# from tensorflow.keras import optimizers, losses, metrics, callbacks
# from models_def import build_lstm, build_bilstm, build_cnn, build_cnn_bilstm, build_transformer
# from data_utils import load_dataset, save_tokenizer, texts_to_padded, MAXLEN

# DEFAULT_DATA = "data/mbti_1.csv"
# MODELS_DIR = "models"
# MAX_TOKENS = 30000
# EMB_DIM = 128

# def compile_model(model):
#     model.compile(
#         optimizer=optimizers.Adam(2e-3),
#         loss=losses.BinaryCrossentropy(),
#         metrics=[metrics.BinaryAccuracy(name="bin_acc"), metrics.AUC(name="auc")]
#     )
#     return model

# def ensure_dirs():
#     os.makedirs(MODELS_DIR, exist_ok=True)

# def main(args):
#     ensure_dirs()

#     # 1) Load & prep data
#     df, text_col, label_col = load_dataset(args.data)
#     texts = df[text_col].astype(str).tolist()
#     y = df[["EI","SN","TF","JP"]].values.astype("float32")

#     # Stratify by rounded sum to keep class balance-ish across splits
#     X_train_texts, X_val_texts, y_train, y_val = train_test_split(
#         texts, y, test_size=0.15, random_state=42, stratify=(y.sum(axis=1).round())
#     )

#     # 2) Fit tokenizer on train texts only
#     tokenizer = Tokenizer(num_words=MAX_TOKENS, oov_token="<OOV>")
#     tokenizer.fit_on_texts(X_train_texts)
#     save_tokenizer(tokenizer)

#     # 3) Integerize & pad
#     X_train = texts_to_padded(X_train_texts, tokenizer=tokenizer, maxlen=MAXLEN)
#     X_val   = texts_to_padded(X_val_texts, tokenizer=tokenizer, maxlen=MAXLEN)

#     # 4) Build models
#     builders = [
#         ("lstm", build_lstm),
#         ("bilstm", build_bilstm),
#         ("cnn", build_cnn),
#         ("cnn_bilstm", build_cnn_bilstm),
#         ("transformer", build_transformer),
#     ]
#     hist = {}

#     for name, fn in builders:
#         print(f"\n=== Building {name} ===")
#         model = fn(vocab_size=MAX_TOKENS, maxlen=MAXLEN, emb_dim=EMB_DIM) if "emb_dim" in fn.__code__.co_varnames \
#                 else fn(vocab_size=MAX_TOKENS, maxlen=MAXLEN)
#         model = compile_model(model)
#         model.summary(print_fn=lambda x: print(f"[{name}] {x}"))

#         ckpt = callbacks.ModelCheckpoint(
#             filepath=os.path.join(MODELS_DIR, f"{name}.keras"),
#             monitor="val_auc", mode="max",
#             save_best_only=True, verbose=1
#         )
#         es = callbacks.EarlyStopping(monitor="val_auc", mode="max", patience=2, restore_best_weights=True)

#         h = model.fit(
#             X_train, y_train,
#             validation_data=(X_val, y_val),
#             epochs=args.epochs, batch_size=args.batch_size,
#             callbacks=[ckpt, es], verbose=1
#         )

#         # Save final snapshot + history
#         model.save(os.path.join(MODELS_DIR, f"{name}_final.keras"))
#         hist[name] = {k: [float(x) for x in v] for k, v in h.history.items()}

#         # --- Evaluation ---
#         print(f"Evaluating {name} on validation set …")
#         val_probs = model.predict(X_val, verbose=0)              # (N, 4)
#         val_preds = (val_probs > 0.5).astype(int)

#         report = {}
#         heads = ["EI","SN","TF","JP"]
#         for i, head in enumerate(heads):
#             acc = accuracy_score(y_val[:, i], val_preds[:, i])
#             report[head] = {"accuracy": float(acc)}

#             # Confusion matrix
#             cm = confusion_matrix(y_val[:, i], val_preds[:, i])
#             plt.figure(figsize=(4,3))
#             sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
#                         xticklabels=[f"{head[1]}", f"{head[0]}"],
#                         yticklabels=[f"{head[1]}", f"{head[0]}"])
#             plt.title(f"{name} - {head} Confusion Matrix")
#             plt.xlabel("Predicted")
#             plt.ylabel("True")
#             plt.tight_layout()
#             plt.savefig(os.path.join(MODELS_DIR, f"{name}_{head}_cm.png"))
#             plt.close()

#         with open(os.path.join(MODELS_DIR, f"{name}_report.json"), "w", encoding="utf-8") as f:
#             json.dump(report, f, indent=2)

#     with open(os.path.join(MODELS_DIR, "history.json"), "w", encoding="utf-8") as f:
#         json.dump(hist, f, indent=2)

#     with open(os.path.join(MODELS_DIR, "label_meta.json"), "w", encoding="utf-8") as f:
#         json.dump({"heads":["EI","SN","TF","JP"], "mapping":"1→E/S/T/J; 0→I/N/F/P"}, f, indent=2)

#     print("\nAll models trained and evaluated. Reports & confusion matrices saved in ./models")

# if __name__ == "__main__":
#     p = argparse.ArgumentParser()
#     p.add_argument("--data", default=DEFAULT_DATA)
#     p.add_argument("--epochs", type=int, default=3)
#     p.add_argument("--batch_size", type=int, default=64)
#     args = p.parse_args()
#     main(args)











import os, json, argparse
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras import optimizers, losses, metrics, callbacks
from models_def import build_lstm, build_bilstm, build_cnn, build_cnn_bilstm, build_transformer
from data_utils import load_dataset, save_tokenizer, texts_to_padded, MAXLEN

DEFAULT_DATA = "data/mbti_1.csv"
MODELS_DIR = "models"
MAX_TOKENS = 30000
EMB_DIM = 128

def compile_model(model):
    model.compile(
        optimizer=optimizers.Adam(2e-3),
        loss=losses.BinaryCrossentropy(),
        metrics=[metrics.BinaryAccuracy(name="bin_acc"), metrics.AUC(name="auc")]
    )
    return model

def ensure_dirs():
    os.makedirs(MODELS_DIR, exist_ok=True)

def compute_metrics(y_true, y_pred):
    """Compute accuracy, precision, recall, f1 for each MBTI head and macro average."""
    metrics_dict = {}
    labels = ["EI","SN","TF","JP"]

    for i, label in enumerate(labels):
        acc = accuracy_score(y_true[:, i], y_pred[:, i])
        prec = precision_score(y_true[:, i], y_pred[:, i], zero_division=0)
        rec = recall_score(y_true[:, i], y_pred[:, i], zero_division=0)
        f1 = f1_score(y_true[:, i], y_pred[:, i], zero_division=0)

        metrics_dict[label] = {
            "accuracy": round(acc, 3),
            "precision": round(prec, 3),
            "recall": round(rec, 3),
            "f1": round(f1, 3)
        }

    # macro averages
    metrics_dict["macro"] = {
        "accuracy": float(np.mean([m["accuracy"] for m in metrics_dict.values()])),
        "precision": float(np.mean([m["precision"] for m in metrics_dict.values()])),
        "recall": float(np.mean([m["recall"] for m in metrics_dict.values()])),
        "f1": float(np.mean([m["f1"] for m in metrics_dict.values()])),
    }
    return metrics_dict

def main(args):
    ensure_dirs()

    # 1) Load & prep data
    df, text_col, label_col = load_dataset(args.data)
    texts = df[text_col].astype(str).tolist()
    y = df[["EI","SN","TF","JP"]].values.astype("float32")

    # Stratify
    X_train_texts, X_val_texts, y_train, y_val = train_test_split(
        texts, y, test_size=0.15, random_state=42, stratify=(y.sum(axis=1).round())
    )

    # 2) Fit tokenizer
    tokenizer = Tokenizer(num_words=MAX_TOKENS, oov_token="<OOV>")
    tokenizer.fit_on_texts(X_train_texts)
    save_tokenizer(tokenizer)

    # 3) Pad sequences
    X_train = texts_to_padded(X_train_texts, tokenizer=tokenizer, maxlen=MAXLEN)
    X_val   = texts_to_padded(X_val_texts, tokenizer=tokenizer, maxlen=MAXLEN)

    # 4) Build models
    builders = [
        ("lstm", build_lstm),
        ("bilstm", build_bilstm),
        ("cnn", build_cnn),
        ("cnn_bilstm", build_cnn_bilstm),
        ("transformer", build_transformer),
    ]
    hist = {}

    for name, fn in builders:
        print(f"\n=== Building {name} ===")
        model = fn(vocab_size=MAX_TOKENS, maxlen=MAXLEN, emb_dim=EMB_DIM) if "emb_dim" in fn.__code__.co_varnames \
                else fn(vocab_size=MAX_TOKENS, maxlen=MAXLEN)
        model = compile_model(model)
        model.summary(print_fn=lambda x: print(f"[{name}] {x}"))

        ckpt = callbacks.ModelCheckpoint(
            filepath=os.path.join(MODELS_DIR, f"{name}.keras"),
            monitor="val_auc", mode="max",
            save_best_only=True, verbose=1
        )
        es = callbacks.EarlyStopping(monitor="val_auc", mode="max", patience=2, restore_best_weights=True)

        h = model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=args.epochs, batch_size=args.batch_size,
            callbacks=[ckpt, es], verbose=1
        )

        # Save final snapshot + history
        model.save(os.path.join(MODELS_DIR, f"{name}_final.keras"))
        hist[name] = {k: [float(x) for x in v] for k, v in h.history.items()}

        # --- Evaluation ---
        print(f"Evaluating {name} on validation set …")
        val_probs = model.predict(X_val, verbose=0)              # (N, 4)
        val_preds = (val_probs > 0.5).astype(int)

        # Compute metrics (accuracy, precision, recall, f1)
        report = compute_metrics(y_val, val_preds)

        # Save confusion matrices
        heads = ["EI","SN","TF","JP"]
        for i, head in enumerate(heads):
            cm = confusion_matrix(y_val[:, i], val_preds[:, i])
            plt.figure(figsize=(4,3))
            sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                        xticklabels=[f"{head[1]}", f"{head[0]}"],
                        yticklabels=[f"{head[1]}", f"{head[0]}"])
            plt.title(f"{name} - {head} Confusion Matrix")
            plt.xlabel("Predicted")
            plt.ylabel("True")
            plt.tight_layout()
            plt.savefig(os.path.join(MODELS_DIR, f"{name}_{head}_cm.png"))
            plt.close()

        # Save metrics JSON
        with open(os.path.join(MODELS_DIR, f"{name}_metrics.json"), "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

    # Save history + label meta
    with open(os.path.join(MODELS_DIR, "history.json"), "w", encoding="utf-8") as f:
        json.dump(hist, f, indent=2)

    with open(os.path.join(MODELS_DIR, "label_meta.json"), "w", encoding="utf-8") as f:
        json.dump({"heads":["EI","SN","TF","JP"], "mapping":"1→E/S/T/J; 0→I/N/F/P"}, f, indent=2)

    print("\nAll models trained and evaluated. Metrics & confusion matrices saved in ./models")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--data", default=DEFAULT_DATA)
    p.add_argument("--epochs", type=int, default=3)
    p.add_argument("--batch_size", type=int, default=64)
    args = p.parse_args()
    main(args)
