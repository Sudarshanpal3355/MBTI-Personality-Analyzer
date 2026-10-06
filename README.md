# 🧠 MBTI Personality Analyzer

An AI-powered web application that analyzes personality traits and predicts the **Myers-Briggs Type Indicator (MBTI)** personality dimensions using deep learning models.

The application provides an interactive Streamlit interface for personality analysis, model comparison, dataset exploration, and prediction results.

---

## 📌 Project Overview

The **MBTI Personality Analyzer** is a deep learning-based personality classification system designed to predict the four MBTI personality dimensions:

- **E / I** — Extraversion / Introversion
- **S / N** — Sensing / Intuition
- **T / F** — Thinking / Feeling
- **J / P** — Judging / Perceiving

The system processes personality-related text and uses multiple deep learning architectures to classify the user's personality traits.

---

## ✨ Features

- 🧠 MBTI personality trait prediction
- 📊 Interactive data analysis
- 🔍 Dataset exploration
- 🤖 Multiple deep learning models
- 📈 Model performance comparison
- 📋 Classification reports
- 📉 Confusion matrix visualization
- 📊 Prediction confidence/results
- 🖥️ Interactive Streamlit dashboard
- 🔤 OCR-based text input functionality
- 📱 Responsive and user-friendly interface

---

## 🧠 Deep Learning Models

The project implements and compares multiple deep learning architectures:

| Model | Purpose |
|---|---|
| LSTM | Sequential text classification |
| BiLSTM | Bidirectional sequence learning |
| CNN | Feature extraction from text |
| CNN-BiLSTM | Hybrid CNN and BiLSTM architecture |
| Transformer | Attention-based text representation |

The models are evaluated using standard classification metrics such as:

- Accuracy
- Precision
- Recall
- F1-Score

---

## 📊 MBTI Personality Dimensions

The system predicts four personality dimensions:

| Dimension | Categories |
|---|---|
| Energy | E / I |
| Information | S / N |
| Decision | T / F |
| Lifestyle | J / P |

These predictions can be combined to determine an overall MBTI personality type such as:

```text
INTJ
INFP
ENTP
ESFJ

🛠️ Technologies Used
Programming Language
Python
Machine Learning / Deep Learning
TensorFlow
Keras
Scikit-learn
NumPy
Pandas
Natural Language Processing
Text preprocessing
Tokenization
Sequence processing
Web Application
Streamlit
Data Visualization
Matplotlib
Seaborn
Development Tools
VS Code
Git
GitHub

📁 Project Structure
MBTI-Personality-Analyzer/
│
├── assets/
│   └── Application assets
│
├── data/
│   └── mbti_1.csv
│
├── models/
│   ├── LSTM models
│   ├── BiLSTM models
│   ├── CNN models
│   ├── CNN-BiLSTM models
│   ├── Transformer models
│   ├── Tokenizer
│   └── Evaluation results
│
├── pages/
│   ├── 1_Home.py
│   ├── 2_Analysis.py
│   ├── 3_Models.py
│   ├── 4_Dataset_Exploration.py
│   └── 5_About.py
│
├── static/
│   └── Static images and resources
│
├── app.py
├── compare_models.py
├── data_utils.py
├── eda.py
├── models_def.py
├── ocr_utils.py
├── sidebar.py
├── train.py
├── requirements.txt
├── IMAGE_OCR_FEATURE.md
├── README.md
└── .gitignore

⚙️ Installation

1. Clone the repository
git clone https://github.com/Sudarshanpal3355/MBTI-Personality-Analyzer.git

2. Navigate to the project
cd MBTI-Personality-Analyzer

3. Create a virtual environment
python -m venv .venv

4. Activate the virtual environment
Windows

.venv\Scripts\activate
Linux / macOS
source .venv/bin/activate
5. Install dependencies
pip install -r requirements.txt
🚀 Running the Application

Start the Streamlit application using:

streamlit run app.py

The application will be available at:

http://localhost:8501

📈 Model Evaluation

The project evaluates different deep learning architectures using:

Accuracy
Precision
Recall
F1-Score
Confusion Matrix

The application provides model comparison and evaluation visualizations through the Streamlit interface.

🔍 OCR Feature

The application also includes OCR functionality that allows text to be extracted from images and used for personality analysis.

OCR-related functionality is implemented in:

ocr_utils.py

Additional documentation:

IMAGE_OCR_FEATURE.md
🔮 Future Improvements

Potential future enhancements include:

Improved transformer-based architectures
Multilingual personality analysis
Real-time personality analysis
Improved model optimization
Cloud deployment
User authentication
Personality-based recommendations
Larger and more diverse datasets
🎯 Project Goals

The main goal of this project is to demonstrate how deep learning and natural language processing can be applied to personality trait classification through an interactive web application.

👨‍💻 Author

Sudarshan Pal

Computer Science & Engineering
GIET University

GitHub:
https://github.com/Sudarshanpal3355

⭐ Acknowledgement

This project was developed as an academic and portfolio project to explore deep learning, natural language processing, and interactive machine learning applications.

🖥️ Application Pages

The Streamlit application is organized into multiple pages:

🏠 Home

Introduction to the MBTI Personality Analyzer and its functionality.

📊 Analysis

Provides personality and model-related analysis.

🤖 Models

Displays information and results related to the implemented deep learning models.

📂 Dataset Exploration

Allows exploration and analysis of the MBTI dataset.

ℹ️ About

Provides information about the project and its development.

🔮 Future Enhancements

Possible future improvements include:

🌐 Multilingual personality analysis
⚡ Faster model inference
📱 Mobile-friendly deployment
☁️ Cloud deployment
🔐 User authentication
📊 Improved visualization and analytics
🧠 Advanced transformer-based architectures
📚 Larger and more diverse datasets
💡 Personalized recommendations based on predicted personality traits
🎓 Project Objective

The primary objective of this project is to explore the application of Deep Learning and Natural Language Processing for personality trait classification.

The project also demonstrates how multiple neural network architectures can be integrated into an interactive machine learning application using Streamlit.