import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from data_utils import load_dataset

DATA_PATH = "data/mbti_1.csv"
STATIC_DIR = "static"
os.makedirs(STATIC_DIR, exist_ok=True)

df, text_col, label_col = load_dataset(DATA_PATH)

print("Dataset Shape:", df.shape)
print("\nSample Rows:\n", df.head())
print("\nMBTI Distribution:\n", df[label_col].value_counts())

# Distribution of MBTI Types
plt.figure(figsize=(12,6))
order = df[label_col].value_counts().index
sns.countplot(x=label_col, data=df, order=order)
plt.title("Distribution of MBTI Types")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(os.path.join(STATIC_DIR, "eda_mbti_distribution.png"))
plt.close()

# Per-dimension distributions
for col in ["EI","SN","TF","JP"]:
    plt.figure(figsize=(5,4))
    sns.countplot(x=col, data=df)
    plt.title(f"Distribution of {col} dimension (1 = first letter)")
    plt.tight_layout()
    plt.savefig(os.path.join(STATIC_DIR, f"eda_{col}.png"))
    plt.close()

print(f"EDA plots saved in ./{STATIC_DIR}/")
