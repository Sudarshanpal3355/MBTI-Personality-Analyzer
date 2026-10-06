# import os, re, json, pickle
# from typing import Tuple, Dict, List
# import numpy as np
# import pandas as pd

# # ---------- Column detection ----------
# TEXT_CANDIDATES = ["posts","text","content","message","sentence","paragraph","post"]
# LABEL_CANDIDATES = ["type","mbti","label"]

# def _clean_text(s: str) -> str:
#     if not isinstance(s, str): return ""
#     s = s.lower()
#     s = re.sub(r"http\S+"," ", s)
#     s = re.sub(r"[\r\n]+"," ", s)
#     s = re.sub(r"[^a-z0-9.,;:!?()'\"/\-\s]"," ", s)
#     s = re.sub(r"\s+"," ", s).strip()
#     return s

# def find_columns(df: pd.DataFrame) -> Tuple[str,str]:
#     text_col = next((c for c in TEXT_CANDIDATES if c in df.columns), None)
#     label_col = next((c for c in LABEL_CANDIDATES if c in df.columns), None)
#     if not text_col or not label_col:
#         raise ValueError(f"Could not find text/label columns. Available: {list(df.columns)}")
#     return text_col, label_col

# # ---------- MBTI mapping ----------
# # 1.0 means leaning toward the FIRST letter in the pair (E/S/T/J)
# def mbti_to_bits(mbti: str) -> np.ndarray:
#     mbti = str(mbti).upper()
#     if len(mbti) != 4:
#         return np.array([np.nan, np.nan, np.nan, np.nan], dtype=float)
#     return np.array([
#         1.0 if mbti[0] == "E" else 0.0,
#         1.0 if mbti[1] == "S" else 0.0,
#         1.0 if mbti[2] == "T" else 0.0,
#         1.0 if mbti[3] == "J" else 0.0,
#     ], dtype=float)

# def bits_to_mbti(bits: np.ndarray) -> str:
#     e = "E" if bits[0]>=0.5 else "I"
#     s = "S" if bits[1]>=0.5 else "N"
#     t = "T" if bits[2]>=0.5 else "F"
#     j = "J" if bits[3]>=0.5 else "P"
#     return f"{e}{s}{t}{j}"

# # ---------- Dataset loader for training ----------
# def load_dataset(path: str) -> Tuple[pd.DataFrame, str, str]:
#     df = pd.read_csv(path)
#     text_col, label_col = find_columns(df)
#     df = df[[text_col, label_col]].dropna()
#     df[text_col] = df[text_col].astype(str).map(_clean_text)
#     df = df[df[text_col].str.len() > 0]
#     df = df[df[label_col].astype(str).str.len() == 4]
#     y = np.vstack(df[label_col].map(mbti_to_bits).values).astype("float32")
#     for i, col in enumerate(["EI","SN","TF","JP"]):
#         df[col] = y[:, i]
#     return df, text_col, label_col

# # ---------- Tokenizer utilities ----------
# MODELS_DIR = "models"
# TOKENIZER_PATH = os.path.join(MODELS_DIR, "tokenizer.pkl")
# MAXLEN = 220  # keep in sync with train.py

# def save_tokenizer(tokenizer) -> None:
#     os.makedirs(MODELS_DIR, exist_ok=True)
#     with open(TOKENIZER_PATH, "wb") as f:
#         pickle.dump(tokenizer, f, protocol=pickle.HIGHEST_PROTOCOL)

# def load_tokenizer():
#     if not os.path.exists(TOKENIZER_PATH):
#         raise FileNotFoundError(f"Tokenizer not found at {TOKENIZER_PATH}. Train models first.")
#     with open(TOKENIZER_PATH, "rb") as f:
#         return pickle.load(f)

# def texts_to_padded(texts: List[str], tokenizer=None, maxlen: int = MAXLEN) -> np.ndarray:
#     if tokenizer is None:
#         tokenizer = load_tokenizer()
#     if isinstance(texts, str):
#         texts = [texts]
#     seqs = tokenizer.texts_to_sequences(texts)
#     from tensorflow.keras.preprocessing.sequence import pad_sequences
#     X = pad_sequences(seqs, maxlen=maxlen, padding="post")
#     return X

# # ---------- Simple emotion scorer ----------
# def basic_emotions(text: str) -> Dict[str, float]:
#     emo = {
#         "joy": ["happy","delight","joy","glad","love","excited","cheer","grateful","pleased","optimistic"],
#         "sadness": ["sad","unhappy","down","depressed","cry","tears","lonely","mourn","regret"],
#         "anger": ["angry","mad","furious","rage","annoyed","irritated","hate","resent"],
#         "fear": ["fear","scared","afraid","terrified","panic","nervous","anxious","worry","alarmed"],
#         "surprise": ["surprise","shocked","amazed","astonished","wow","unexpected"],
#         "trust": ["trust","secure","safe","confident","faith","rely","dependable"],
#         "disgust": ["disgust","gross","nasty","revolting","repulsed"],
#         "anticipation": ["anticipate","expect","hope","eager","await","soon","upcoming","plan"]
#     }
#     s = _clean_text(text)
#     scores = {k:0 for k in emo}
#     for k, words in emo.items():
#         for w in words:
#             scores[k] += s.count(" " + w + " ")
#             if s.startswith(w + " "): scores[k] += 1
#             if s.endswith(" " + w): scores[k] += 1
#     total = sum(scores.values())
#     return {k: (0.0 if total==0 else round(v/total,4)) for k,v in scores.items()}



import os, re, json, pickle
from typing import Tuple, Dict, List
import numpy as np
import pandas as pd

try:
    import nltk
    from nltk.sentiment import SentimentIntensityAnalyzer
except Exception:
    nltk = None
    SentimentIntensityAnalyzer = None

# ---------- Column detection ----------
TEXT_CANDIDATES = ["posts","text","content","message","sentence","paragraph","post"]
LABEL_CANDIDATES = ["type","mbti","label"]

def _clean_text(s: str) -> str:
    if not isinstance(s, str): return ""
    s = s.lower()
    s = re.sub(r"http\S+"," ", s)
    s = re.sub(r"[\r\n]+"," ", s)
    s = re.sub(r"[^a-z0-9.,;:!?()'\"/\-\s]"," ", s)
    s = re.sub(r"\s+"," ", s).strip()
    return s

def find_columns(df: pd.DataFrame) -> Tuple[str,str]:
    text_col = next((c for c in TEXT_CANDIDATES if c in df.columns), None)
    label_col = next((c for c in LABEL_CANDIDATES if c in df.columns), None)
    if not text_col or not label_col:
        raise ValueError(f"Could not find text/label columns. Available: {list(df.columns)}")
    return text_col, label_col

# ---------- MBTI mapping ----------
# 1.0 means leaning toward the FIRST letter in the pair (E/S/T/J)
def mbti_to_bits(mbti: str) -> np.ndarray:
    mbti = str(mbti).upper()
    if len(mbti) != 4:
        return np.array([np.nan, np.nan, np.nan, np.nan], dtype=float)
    return np.array([
        1.0 if mbti[0] == "E" else 0.0,
        1.0 if mbti[1] == "S" else 0.0,
        1.0 if mbti[2] == "T" else 0.0,
        1.0 if mbti[3] == "J" else 0.0,
    ], dtype=float)

def bits_to_mbti(bits: np.ndarray) -> str:
    e = "E" if bits[0]>=0.5 else "I"
    s = "S" if bits[1]>=0.5 else "N"
    t = "T" if bits[2]>=0.5 else "F"
    j = "J" if bits[3]>=0.5 else "P"
    return f"{e}{s}{t}{j}"

# ---------- Dataset loader for training ----------
def load_dataset(path: str) -> Tuple[pd.DataFrame, str, str]:
    df = pd.read_csv(path)
    text_col, label_col = find_columns(df)
    df = df[[text_col, label_col]].dropna()
    df[text_col] = df[text_col].astype(str).map(_clean_text)
    df = df[df[text_col].str.len() > 0]
    df = df[df[label_col].astype(str).str.len() == 4]
    y = np.vstack(df[label_col].map(mbti_to_bits).values).astype("float32")
    for i, col in enumerate(["EI","SN","TF","JP"]):
        df[col] = y[:, i]
    return df, text_col, label_col

# ---------- Tokenizer utilities ----------
MODELS_DIR = "models"
TOKENIZER_PATH = os.path.join(MODELS_DIR, "tokenizer.pkl")
MAXLEN = 220  # keep in sync with train.py

def save_tokenizer(tokenizer) -> None:
    os.makedirs(MODELS_DIR, exist_ok=True)
    with open(TOKENIZER_PATH, "wb") as f:
        pickle.dump(tokenizer, f, protocol=pickle.HIGHEST_PROTOCOL)

def load_tokenizer():
    if not os.path.exists(TOKENIZER_PATH):
        raise FileNotFoundError(f"Tokenizer not found at {TOKENIZER_PATH}. Train models first.")
    with open(TOKENIZER_PATH, "rb") as f:
        return pickle.load(f)

def texts_to_padded(texts: List[str], tokenizer=None, maxlen: int = MAXLEN) -> np.ndarray:
    if tokenizer is None:
        tokenizer = load_tokenizer()
    if isinstance(texts, str):
        texts = [texts]
    seqs = tokenizer.texts_to_sequences(texts)
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    X = pad_sequences(seqs, maxlen=maxlen, padding="post")
    return X

# ---------- Emotion scorer (keywords + VADER sentiment) ----------
if SentimentIntensityAnalyzer is None:
    sia = None
else:
    try:
        sia = SentimentIntensityAnalyzer()
    except LookupError:
        try:
            if nltk is not None:
                nltk.download("vader_lexicon")
                sia = SentimentIntensityAnalyzer()
            else:
                sia = None
        except Exception:
            sia = None
    except Exception:
        sia = None

def basic_emotions(text: str) -> Dict[str, float]:
    emo = {
        "joy": ["happy","delight","joy","glad","love","excited","cheer","grateful","pleased","optimistic"],
        "sadness": ["sad","unhappy","down","depressed","cry","tears","lonely","mourn","regret"],
        "anger": ["angry","mad","furious","rage","annoyed","irritated","hate","resent"],
        "fear": ["fear","scared","afraid","terrified","panic","nervous","anxious","worry","alarmed"],
        "surprise": ["surprise","shocked","amazed","astonished","wow","unexpected"],
        "trust": ["trust","secure","safe","confident","faith","rely","dependable"],
        "disgust": ["disgust","gross","nasty","revolting","repulsed"],
        "anticipation": ["anticipate","expect","hope","eager","await","soon","upcoming","plan"]
    }

    s = _clean_text(text)
    scores = {k:0.0 for k in emo}

    # keyword counts
    for k, words in emo.items():
        for w in words:
            pattern = r"\b" + re.escape(w) + r"\b"
            scores[k] += len(re.findall(pattern, s))

    # sentiment scores
    if sia is not None:
        vader_scores = sia.polarity_scores(text)
        pos = max(0.0, vader_scores.get("pos", 0.0))
        neg = max(0.0, vader_scores.get("neg", 0.0))
        scores["joy"] += pos
        scores["trust"] += pos * 0.5
        scores["sadness"] += neg
        scores["anger"] += neg * 0.6
        scores["fear"] += neg * 0.4
        scores["disgust"] += neg * 0.3

    total = sum(scores.values())
    if total == 0:
        return {k: 1/len(scores) for k in scores}  # uniform if nothing found
    return {k: round(v/total, 4) for k,v in scores.items()}
