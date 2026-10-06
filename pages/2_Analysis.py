# # Analysis.py

# import os, numpy as np, pandas as pd, streamlit as st, tensorflow as tf
# from data_utils import texts_to_padded, bits_to_mbti

# from sidebar import sidebar_header
# sidebar_header()

# st.set_page_config(page_title="Analysis", page_icon="📊", layout="wide")
# st.title("📊 Detailed Analysis")

# MODELS_DIR = "models"

# @st.cache_resource(show_spinner=False)
# def load_models():
#     models = {}
#     if not os.path.isdir(MODELS_DIR):
#         return models
#     for fn in os.listdir(MODELS_DIR):
#         if fn.endswith(".keras") and not fn.endswith("_final.keras"):
#             name = fn.replace(".keras","")
#             try:
#                 models[name] = tf.keras.models.load_model(os.path.join(MODELS_DIR, fn))
#             except Exception as e:
#                 st.warning(f"Failed to load {fn}: {e}")
#     return models

# models = load_models()

# text_samples = st.text_area("Paste multiple lines (each is a separate input):", height=180, placeholder="Line 1...\nLine 2...\nLine 3...")

# if st.button("Batch Predict", use_container_width=True):
#     lines = [t.strip() for t in text_samples.splitlines() if t.strip()]
#     if not lines:
#         st.warning("Please paste at least one non-empty line.")
#         st.stop()
#     if not models:
#         st.error("No models found. Train first with `python train.py`.")
#         st.stop()

#     X = texts_to_padded(lines)
#     preds = []
#     for name, m in models.items():
#         preds.append(m.predict(X, verbose=0))  # [n,4]
#     avg = np.mean(np.stack(preds, axis=0), axis=0)  # [n,4]

#     rows = []
#     for i, line in enumerate(lines):
#         bits = avg[i]
#         mbti = bits_to_mbti(bits)
#         rows.append({
#             "Text": (line[:120] + "…") if len(line)>120 else line,
#             "MBTI": mbti,
#             "E%": round(float(bits[0])*100,2),
#             "S%": round(float(bits[1])*100,2),
#             "T%": round(float(bits[2])*100,2),
#             "J%": round(float(bits[3])*100,2),
#         })
#     st.dataframe(pd.DataFrame(rows), use_container_width=True)









# # Analysis.py

# import os, numpy as np, pandas as pd, streamlit as st, tensorflow as tf, json
# import plotly.graph_objects as go
# from data_utils import texts_to_padded, bits_to_mbti
# from sidebar import sidebar_header

# sidebar_header()

# st.set_page_config(page_title="Analysis", page_icon="📊", layout="wide")
# st.title("📊 Detailed Analysis")

# MODELS_DIR = "models"

# @st.cache_resource(show_spinner=False)
# def load_models():
#     models = {}
#     if not os.path.isdir(MODELS_DIR):
#         return models
#     for fn in os.listdir(MODELS_DIR):
#         if fn.endswith(".keras") and not fn.endswith("_final.keras"):
#             name = fn.replace(".keras","")
#             try:
#                 models[name] = tf.keras.models.load_model(os.path.join(MODELS_DIR, fn))
#             except Exception as e:
#                 st.warning(f"Failed to load {fn}: {e}")
#     return models

# models = load_models()

# text_samples = st.text_area(
#     "Paste multiple lines (each is a separate input):",
#     height=180,
#     placeholder="Line 1...\nLine 2...\nLine 3..."
# )

# if st.button("Batch Predict", use_container_width=True):
#     lines = [t.strip() for t in text_samples.splitlines() if t.strip()]
#     if not lines:
#         st.warning("Please paste at least one non-empty line.")
#         st.stop()
#     if not models:
#         st.error("No models found. Train first with `python train.py`.")
#         st.stop()

#     X = texts_to_padded(lines)
#     preds = []
#     for name, m in models.items():
#         preds.append(m.predict(X, verbose=0))  # [n,4]
#     avg = np.mean(np.stack(preds, axis=0), axis=0)  # [n,4]

#     # --- Tabs for Predictions and Metrics ---
#     tabs = st.tabs(["🔮 Predictions", "📊 Metrics"])

#     # ---------- Predictions ----------
#     with tabs[0]:
#         rows = []
#         for i, line in enumerate(lines):
#             bits = avg[i]
#             mbti = bits_to_mbti(bits)
#             rows.append({
#                 "Text": (line[:120] + "…") if len(line) > 120 else line,
#                 "MBTI": mbti,
#                 "E%": round(float(bits[0]) * 100, 2),
#                 "S%": round(float(bits[1]) * 100, 2),
#                 "T%": round(float(bits[2]) * 100, 2),
#                 "J%": round(float(bits[3]) * 100, 2),
#             })
#         st.subheader("Prediction Results")
#         st.dataframe(pd.DataFrame(rows), use_container_width=True)

#     # ---------- Metrics ----------
#     with tabs[1]:
#         st.subheader("Evaluation Metrics")
#         metric_files = [f for f in os.listdir(MODELS_DIR) if f.endswith("_metrics.json")]
#         if not metric_files:
#             st.warning("⚠️ No metrics found. Please run train.py first to generate evaluation results.")
#         else:
#             model_choice = st.selectbox("Choose a model to view metrics:", metric_files)
#             metrics_path = os.path.join(MODELS_DIR, model_choice)
#             with open(metrics_path, "r") as f:
#                 metrics = json.load(f)

#             # Table
#             df = pd.DataFrame(metrics).T
#             st.dataframe(df.style.highlight_max(axis=0, color="lightgreen"))

#             # Bar chart (F1 per dimension)
#             dims = ["E/I", "S/N", "T/F", "J/P"]
#             f1s = [metrics[d]["f1"] for d in dims]
#             fig = go.Figure([go.Bar(x=dims, y=f1s, text=[f"{v:.2f}" for v in f1s], textposition="auto")])
#             fig.update_layout(yaxis=dict(range=[0, 1]))
#             st.plotly_chart(fig, use_container_width=True)

#             # Radar chart (macro averages)
#             categories = ["accuracy", "precision", "recall", "f1"]
#             values = [metrics["macro"][c] for c in categories]
#             fig2 = go.Figure()
#             fig2.add_trace(go.Scatterpolar(r=values, theta=categories, fill='toself'))
#             fig2.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,1])), showlegend=False)
#             st.plotly_chart(fig2, use_container_width=True)














# Analysis.py

import os, numpy as np, pandas as pd, streamlit as st, tensorflow as tf, json
import plotly.graph_objects as go
from data_utils import texts_to_padded, bits_to_mbti
from sidebar import sidebar_header
from ocr_utils import extract_text_from_uploaded_file

sidebar_header()

st.set_page_config(page_title="Analysis", page_icon="📊", layout="wide")
st.title("📊 Detailed Analysis")

MODELS_DIR = "models"

@st.cache_resource(show_spinner=False)
def load_models():
    models = {}
    if not os.path.isdir(MODELS_DIR):
        return models
    for fn in os.listdir(MODELS_DIR):
        if fn.endswith(".keras") and not fn.endswith("_final.keras"):
            name = fn.replace(".keras", "")
            try:
                models[name] = tf.keras.models.load_model(os.path.join(MODELS_DIR, fn))
            except Exception as e:
                st.warning(f"Failed to load {fn}: {e}")
    return models

models = load_models()

# Create tabs for input methods
input_method = st.radio(
    "Choose input method:",
    ["📝 Manual Text", "🖼️ Image Upload (OCR)"],
    horizontal=True
)

text_samples = ""

if input_method == "📝 Manual Text":
    text_samples = st.text_area(
        "Paste multiple lines (each is a separate input):",
        height=180,
        placeholder="Line 1...\nLine 2...\nLine 3..."
    )
else:  # Image Upload
    st.markdown("### Upload an image containing text")
    uploaded_file = st.file_uploader(
        "Choose an image file (PNG, JPG, JPEG)",
        type=['png', 'jpg', 'jpeg']
    )
    
    if uploaded_file is not None:
        col1, col2 = st.columns(2)
        with col1:
            st.image(uploaded_file, caption="Uploaded Image", width="stretch")
        
        with col2:
            st.write("**Extracting text from image...**")
            with st.spinner("Processing image with OCR..."):
                extracted_text, image_bytes = extract_text_from_uploaded_file(uploaded_file)
                
            if extracted_text:
                st.success("✅ Text extracted successfully!")
                st.text_area(
                    "Extracted Text:",
                    extracted_text,
                    height=200,
                    disabled=False
                )
                text_samples = extracted_text
            else:
                st.warning("⚠️ No text could be extracted from the image. Please try another image.")
                text_samples = ""

# Add analysis button
if st.button("🔮 Analyze Text", width="stretch", type="primary"):
    if input_method == "🖼️ Image Upload (OCR)" and not text_samples:
        st.error("❌ No text extracted from image. Please upload a valid image with text.")
        st.stop()
    
    lines = [t.strip() for t in text_samples.splitlines() if t.strip()]
    if not lines:
        st.warning("Please enter at least one non-empty line.")
        st.stop()
    if not models:
        st.error("No models found. Train first with `python train.py`.")
        st.stop()

    X = texts_to_padded(lines)
    preds = []
    for name, m in models.items():
        preds.append(m.predict(X, verbose=0))  # [n,4]
    avg = np.mean(np.stack(preds, axis=0), axis=0)  # [n,4]

    # --- Tabs for Predictions and Metrics ---
    tabs = st.tabs(["🔮 Predictions", "📊 Metrics"])

    # ---------- Predictions ----------
    with tabs[0]:
        rows = []
        for i, line in enumerate(lines):
            bits = avg[i]
            mbti = bits_to_mbti(bits)
            rows.append({
                "Text": (line[:120] + "…") if len(line) > 120 else line,
                "MBTI": mbti,
                "E%": round(float(bits[0]) * 100, 2),
                "S%": round(float(bits[1]) * 100, 2),
                "T%": round(float(bits[2]) * 100, 2),
                "J%": round(float(bits[3]) * 100, 2),
            })
        st.subheader("Prediction Results")
        st.dataframe(pd.DataFrame(rows), width="stretch")

    # ---------- Metrics ----------
    with tabs[1]:
        st.subheader("Evaluation Metrics")
        metric_files = [f for f in os.listdir(MODELS_DIR) if f.endswith("_metrics.json")]
        if not metric_files:
            st.warning("⚠️ No metrics found. Please run train.py first to generate evaluation results.")
        else:
            model_choice = st.selectbox("Choose a model to view metrics:", metric_files)
            metrics_path = os.path.join(MODELS_DIR, model_choice)
            with open(metrics_path, "r") as f:
                metrics = json.load(f)

            # Table
            df = pd.DataFrame(metrics).T
            st.dataframe(df.style.highlight_max(axis=0, color="lightgreen"))

            # Dimensions
            dims = ["E/I", "S/N", "T/F", "J/P"]

            # Layout: 2x2 grid for bar charts
            col1, col2 = st.columns(2)

            # Accuracy Bar Chart
            with col1:
                accs = [metrics[d]["accuracy"] for d in dims]
                fig_acc = go.Figure([go.Bar(x=dims, y=accs, text=[f"{v:.2f}" for v in accs], textposition="auto")])
                fig_acc.update_layout(title="Accuracy per MBTI Dimension", yaxis=dict(range=[0,1]))
                st.plotly_chart(fig_acc, width="stretch")

            # Precision Bar Chart
            with col2:
                precs = [metrics[d]["precision"] for d in dims]
                fig_prec = go.Figure([go.Bar(x=dims, y=precs, text=[f"{v:.2f}" for v in precs], textposition="auto")])
                fig_prec.update_layout(title="Precision per MBTI Dimension", yaxis=dict(range=[0,1]))
                st.plotly_chart(fig_prec, width="stretch")

            # Recall and F1 in second row
            col3, col4 = st.columns(2)

            # Recall Bar Chart
            with col3:
                recs = [metrics[d]["recall"] for d in dims]
                fig_rec = go.Figure([go.Bar(x=dims, y=recs, text=[f"{v:.2f}" for v in recs], textposition="auto")])
                fig_rec.update_layout(title="Recall per MBTI Dimension", yaxis=dict(range=[0,1]))
                st.plotly_chart(fig_rec, width="stretch")

            # F1-score Bar Chart
            with col4:
                f1s = [metrics[d]["f1"] for d in dims]
                fig_f1 = go.Figure([go.Bar(x=dims, y=f1s, text=[f"{v:.2f}" for v in f1s], textposition="auto")])
                fig_f1.update_layout(title="F1-score per MBTI Dimension", yaxis=dict(range=[0,1]))
                st.plotly_chart(fig_f1, width="stretch")

            # Radar chart (macro averages)
            categories = ["accuracy", "precision", "recall", "f1"]
            values = [metrics["macro"][c] for c in categories]
            fig2 = go.Figure()
            fig2.add_trace(go.Scatterpolar(r=values, theta=categories, fill='toself'))
            fig2.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0,1])),
                showlegend=False,
                title="Macro Averages"
            )
            st.plotly_chart(fig2, width="stretch")

