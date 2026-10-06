import tensorflow as tf
from tensorflow.keras import layers, models

# ----- LSTM -----
def build_lstm(vocab_size, maxlen, emb_dim=128):
    model = models.Sequential([
        layers.Embedding(vocab_size, emb_dim, input_length=maxlen),
        layers.LSTM(128, return_sequences=False),
        layers.Dropout(0.3),
        layers.Dense(4, activation="sigmoid")  # 4 heads: EI, SN, TF, JP
    ])
    return model

# ----- BiLSTM -----
def build_bilstm(vocab_size, maxlen, emb_dim=128):
    model = models.Sequential([
        layers.Embedding(vocab_size, emb_dim, input_length=maxlen),
        layers.Bidirectional(layers.LSTM(128, return_sequences=False)),
        layers.Dropout(0.3),
        layers.Dense(4, activation="sigmoid")
    ])
    return model

# ----- CNN -----
def build_cnn(vocab_size, maxlen, emb_dim=128):
    model = models.Sequential([
        layers.Embedding(vocab_size, emb_dim, input_length=maxlen),
        layers.Conv1D(128, 5, activation="relu"),
        layers.GlobalMaxPooling1D(),
        layers.Dropout(0.3),
        layers.Dense(4, activation="sigmoid")
    ])
    return model

# ----- CNN + BiLSTM hybrid -----
def build_cnn_bilstm(vocab_size, maxlen, emb_dim=128):
    inputs = layers.Input(shape=(maxlen,))
    x = layers.Embedding(vocab_size, emb_dim)(inputs)
    x = layers.Conv1D(128, 5, activation="relu")(x)
    x = layers.Bidirectional(layers.LSTM(128))(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(4, activation="sigmoid")(x)
    return models.Model(inputs, outputs)

# ----- Minimal Transformer-like -----
def build_transformer(vocab_size, maxlen, emb_dim=128, num_heads=4, ff_dim=128):
    inputs = layers.Input(shape=(maxlen,))
    x = layers.Embedding(vocab_size, emb_dim)(inputs)

    attn = layers.MultiHeadAttention(num_heads=num_heads, key_dim=emb_dim)(x, x)
    x = layers.Add()([x, attn])
    x = layers.LayerNormalization()(x)

    ff = layers.Dense(ff_dim, activation="relu")(x)
    ff = layers.Dense(emb_dim)(ff)
    x = layers.Add()([x, ff])
    x = layers.LayerNormalization()(x)

    x = layers.GlobalAveragePooling1D()(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(4, activation="sigmoid")(x)
    return models.Model(inputs, outputs)
