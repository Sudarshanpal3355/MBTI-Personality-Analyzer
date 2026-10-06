# 🧠 MBTI Personality Analyzer

An AI-powered personality analysis web application that predicts **Myers-Briggs Type Indicator (MBTI)** personality dimensions using Natural Language Processing (NLP) and Deep Learning.

The application provides an interactive **Streamlit dashboard** for personality prediction, dataset exploration, model evaluation, model comparison, OCR-based text extraction, and visualization.

---

## 📌 Project Overview

The **MBTI Personality Analyzer** is a deep learning-based personality classification system designed to analyze text and predict the four MBTI personality dimensions:

| Dimension | Categories | Description |
|---|---|---|
| Energy | E / I | Extraversion / Introversion |
| Information | S / N | Sensing / Intuition |
| Decision | T / F | Thinking / Feeling |
| Lifestyle | J / P | Judging / Perceiving |

The four predictions can be combined to determine an overall MBTI personality type such as:

```text
INTJ
INFP
ENTP
ESFJ

## **🧠 Deep Learning Models**

The project implements and compares multiple neural network architectures for text classification.

Model	Purpose
LSTM	Sequential text classification
BiLSTM	Bidirectional sequence learning
CNN	Local feature extraction from text
CNN-BiLSTM	Hybrid CNN and BiLSTM architecture
Transformer	Attention-based text representation
Evaluation Metrics

The models are evaluated using:

Accuracy
Precision
Recall
F1-Score
Confusion Matrix
Classification Report

## **🔄 Project Workflow**
User Input
    │
    ▼
Text Preprocessing
    │
    ▼
Tokenization
    │
    ▼
Feature / Sequence Preparation
    │
    ▼
Deep Learning Model
    │
    ├── LSTM
    ├── BiLSTM
    ├── CNN
    ├── CNN-BiLSTM
    └── Transformer
    │
    ▼
MBTI Dimension Prediction
    │
    ▼
E/I + S/N + T/F + J/P
    │
    ▼
Final MBTI Personality Type

## **🛠️ Technologies Used**

Programming Language
Python
Deep Learning
TensorFlow
Keras
Machine Learning
Scikit-learn
Natural Language Processing
Text preprocessing
Tokenization
Sequence processing
NLP-based text classification
Data Processing
NumPy
Pandas
Data Visualization
Matplotlib
Seaborn
Web Application
Streamlit
OCR
Tesseract OCR
Development Tools
VS Code
Git
GitHub
Model Storage
Git LFS

## **📊 Dataset**

The project uses the MBTI personality dataset containing personality-related text and corresponding MBTI personality types.

Dataset location:

data/mbti_1.csv

The dataset is processed and transformed into the required format for training the different deep learning models.

## **📁 Project Structure**

MBTI-Personality-Analyzer/
│
├── assets/
│   ├── script.js
│   └── style.css
│
├── data/
│   └── mbti_1.csv
│
├── models/
│   ├── bilstm.keras
│   ├── bilstm_final.keras
│   ├── cnn.keras
│   ├── cnn_final.keras
│   ├── cnn_bilstm.keras
│   ├── cnn_bilstm_final.keras
│   ├── lstm.keras
│   ├── lstm_final.keras
│   ├── transformer.keras
│   ├── transformer_final.keras
│   ├── tokenizer.pkl
│   └── evaluation results
│
├── pages/
│   ├── 1_Home.py
│   ├── 2_Analysis.py
│   ├── 3_Models.py
│   ├── 4_Dataset_Explorer.py
│   └── 5_About.py
│
├── static/
│   └── images and resources
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

## **⚙️ Installation**

1. Clone the Repository
git clone https://github.com/Sudarshanpal3355/MBTI-Personality-Analyzer.git
2. Navigate to the Project
cd MBTI-Personality-Analyzer
3. Create a Virtual Environment
python -m venv .venv
4. Activate the Virtual Environment
Windows
.venv\Scripts\activate
Linux / macOS
source .venv/bin/activate
5. Install Dependencies
pip install -r requirements.txt

## **🚀 Running the Application**

Start the Streamlit application:

streamlit run app.py

The application will normally be available at:

http://localhost:8501
🖥️ Application Pages
🏠 Home

Provides an introduction to the MBTI Personality Analyzer and its main functionality.

📊 Analysis

Provides personality-related analysis and visualizations.

🤖 Models

Displays information about the implemented deep learning models and their evaluation results.

📂 Dataset Explorer

Allows users to explore and analyze the MBTI dataset.

ℹ️ About

Provides information about the project, technologies, and development.

📈 Model Evaluation

The application provides model evaluation using:

Accuracy
Precision
Recall
F1-Score
Confusion Matrix
Classification Reports

The models can also be compared to understand their relative performance.

🔍 OCR Feature

The application includes an OCR-based input feature that allows users to extract text from images and use the extracted text for personality analysis.

OCR functionality is implemented in:

ocr_utils.py

Additional documentation:

IMAGE_OCR_FEATURE.md
🔬 Model Comparison

The project includes functionality for comparing the performance of the implemented models.

Models compared include:

LSTM
BiLSTM
CNN
CNN-BiLSTM
Transformer

The comparison can be performed using:

python compare_models.py
🎯 Project Objective

The primary objective of this project is to demonstrate how Deep Learning and Natural Language Processing can be applied to personality trait classification.

The project also demonstrates how multiple neural network architectures can be integrated into an interactive machine learning application using Streamlit.

🔮 Future Enhancements

Potential future improvements include:

🌐 Multilingual personality analysis
⚡ Faster model inference
📱 Mobile-friendly deployment
☁️ Cloud deployment
🔐 User authentication
📊 Advanced analytics and visualization
🧠 Improved Transformer architectures
📚 Larger and more diverse datasets
💡 Personalized recommendations based on personality
🔄 Real-time personality analysis
📸 Screenshots

Screenshots of the application can be added here to demonstrate:

Home Dashboard
Personality Prediction
Model Comparison
Dataset Explorer
Analysis Dashboard
OCR Feature

Example:

screenshots/
├── home.png
├── prediction.png
├── models.png
├── analysis.png
└── dataset.png
👨‍💻 Author
Sudarshan Pal

Computer Science & Engineering
GIET University

GitHub:
https://github.com/Sudarshanpal3355

⭐ Acknowledgement

This project was developed as an academic and portfolio project to explore:

Deep Learning
Natural Language Processing
Text Classification
Personality Analysis
Interactive Machine Learning Applications
📄 License

This project is licensed under the MIT License.

See the LICENSE file for more information.

⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.


### After replacing the README

Since you've **already pushed the repository**, you'll need to push this README update too.

Save `README.md`, then run:

```powershell
git add README.md

Then:

git commit -m "Improve project documentation"

Then:

git push

Finally:

git status

You should again see:

Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean

One important point: don't run git lfs migrate again. Your model files are already correctly configured with Git LFS and successfully uploaded.

give in an single code file so that  i can copy every thing andf paste it there

Absolutely. Copy everything inside this single code block and paste it directly into your README.md file.

# 🧠 MBTI Personality Analyzer

An AI-powered personality analysis web application that predicts **Myers-Briggs Type Indicator (MBTI)** personality dimensions using **Natural Language Processing (NLP)** and **Deep Learning**.

The application provides an interactive **Streamlit dashboard** for personality prediction, dataset exploration, model evaluation, model comparison, OCR-based text extraction, and visualization.

---

## 📌 Project Overview

The **MBTI Personality Analyzer** is a deep learning-based personality classification system designed to analyze text and predict the four MBTI personality dimensions:

| Dimension | Categories | Description |
|---|---|---|
| Energy | E / I | Extraversion / Introversion |
| Information | S / N | Sensing / Intuition |
| Decision | T / F | Thinking / Feeling |
| Lifestyle | J / P | Judging / Perceiving |

The four predictions can be combined to determine an overall MBTI personality type such as:

```text
INTJ
INFP
ENTP
ESFJ
✨ Key Features
🧠 MBTI personality trait prediction
🤖 Multiple Deep Learning models
📊 Interactive Streamlit dashboard
🔍 Dataset exploration
📈 Model performance comparison
📋 Classification reports
📉 Confusion matrix visualization
🎯 Prediction confidence and results
🔤 OCR-based text input
📊 Interactive data analysis
🖥️ Responsive user interface
📚 Model evaluation and comparison
🧠 Deep Learning Models

The project implements and compares multiple neural network architectures for text classification.

Model	Purpose
LSTM	Sequential text classification
BiLSTM	Bidirectional sequence learning
CNN	Local feature extraction from text
CNN-BiLSTM	Hybrid CNN and BiLSTM architecture
Transformer	Attention-based text representation
Evaluation Metrics

The models are evaluated using:

Accuracy
Precision
Recall
F1-Score
Confusion Matrix
Classification Report
🔄 Project Workflow
User Input
    │
    ▼
Text Preprocessing
    │
    ▼
Tokenization
    │
    ▼
Feature / Sequence Preparation
    │
    ▼
Deep Learning Model
    │
    ├── LSTM
    ├── BiLSTM
    ├── CNN
    ├── CNN-BiLSTM
    └── Transformer
    │
    ▼
MBTI Dimension Prediction
    │
    ▼
E/I + S/N + T/F + J/P
    │
    ▼
Final MBTI Personality Type
🛠️ Technologies Used
Programming Language
Python
Deep Learning
TensorFlow
Keras
Machine Learning
Scikit-learn
Natural Language Processing
Text preprocessing
Tokenization
Sequence processing
NLP-based text classification
Data Processing
NumPy
Pandas
Data Visualization
Matplotlib
Seaborn
Web Application
Streamlit
OCR
Tesseract OCR
Development Tools
VS Code
Git
GitHub
Model Storage
Git LFS
📊 Dataset

The project uses the MBTI personality dataset containing personality-related text and corresponding MBTI personality types.

Dataset location:

data/mbti_1.csv

The dataset is processed and transformed into the required format for training the different deep learning models.

📁 Project Structure
MBTI-Personality-Analyzer/
│
├── assets/
│   ├── script.js
│   └── style.css
│
├── data/
│   └── mbti_1.csv
│
├── models/
│   ├── bilstm.keras
│   ├── bilstm_final.keras
│   ├── cnn.keras
│   ├── cnn_final.keras
│   ├── cnn_bilstm.keras
│   ├── cnn_bilstm_final.keras
│   ├── lstm.keras
│   ├── lstm_final.keras
│   ├── transformer.keras
│   ├── transformer_final.keras
│   ├── tokenizer.pkl
│   └── evaluation results
│
├── pages/
│   ├── 1_Home.py
│   ├── 2_Analysis.py
│   ├── 3_Models.py
│   ├── 4_Dataset_Explorer.py
│   └── 5_About.py
│
├── static/
│   └── images and resources
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
1. Clone the Repository
git clone https://github.com/Sudarshanpal3355/MBTI-Personality-Analyzer.git
2. Navigate to the Project
cd MBTI-Personality-Analyzer
3. Create a Virtual Environment
python -m venv .venv
4. Activate the Virtual Environment
Windows
.venv\Scripts\activate
Linux / macOS
source .venv/bin/activate
5. Install Dependencies
pip install -r requirements.txt
🚀 Running the Application

Start the Streamlit application:

streamlit run app.py

The application will normally be available at:

http://localhost:8501
🖥️ Application Pages
🏠 Home

Provides an introduction to the MBTI Personality Analyzer and its main functionality.

📊 Analysis

Provides personality-related analysis and visualizations.

🤖 Models

Displays information about the implemented deep learning models and their evaluation results.

📂 Dataset Explorer

Allows users to explore and analyze the MBTI dataset.

ℹ️ About

Provides information about the project, technologies, and development.

📈 Model Evaluation

The application provides model evaluation using:

Accuracy
Precision
Recall
F1-Score
Confusion Matrix
Classification Reports

The models can also be compared to understand their relative performance.

🔬 Model Comparison

The project includes functionality for comparing the performance of the implemented models.

Models compared include:

LSTM
BiLSTM
CNN
CNN-BiLSTM
Transformer

Model comparison can be performed using:

python compare_models.py
🔍 OCR Feature

The application includes an OCR-based input feature that allows users to extract text from images and use the extracted text for personality analysis.

OCR functionality is implemented in:

ocr_utils.py

Additional documentation:

IMAGE_OCR_FEATURE.md
📸 Application Screenshots

Screenshots can be added here to demonstrate the application interface.

Recommended screenshots:

Home Dashboard
Personality Prediction
Model Comparison
Dataset Explorer
Analysis Dashboard
OCR Feature

Example structure:

screenshots/
├── home.png
├── prediction.png
├── models.png
├── analysis.png
└── dataset.png
🎯 Project Objective

The primary objective of this project is to demonstrate how Deep Learning and Natural Language Processing can be applied to personality trait classification.

The project also demonstrates how multiple neural network architectures can be integrated into an interactive machine learning application using Streamlit.

🔮 Future Enhancements

Potential future improvements include:

🌐 Multilingual personality analysis
⚡ Faster model inference
📱 Mobile-friendly deployment
☁️ Cloud deployment
🔐 User authentication
📊 Advanced analytics and visualization
🧠 Improved Transformer architectures
📚 Larger and more diverse datasets
💡 Personalized recommendations based on personality
🔄 Real-time personality analysis
👨‍💻 Author
Sudarshan Pal

Computer Science & Engineering
GIET University

GitHub:

https://github.com/Sudarshanpal3355

⭐ Acknowledgement

This project was developed as an academic and portfolio project to explore:

Deep Learning
Natural Language Processing
Text Classification
Personality Analysis
Interactive Machine Learning Applications
📄 License

This project is licensed under the MIT License.

See the LICENSE file for more information.

⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

🔗 Repository

GitHub:
https://github.com/Sudarshanpal3355/MBTI-Personality-Analyzer