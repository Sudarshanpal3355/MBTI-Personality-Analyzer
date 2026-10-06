# import os, json, numpy as np, pandas as pd, streamlit as st, plotly.graph_objects as go, tensorflow as tf
# from data_utils import texts_to_padded, bits_to_mbti, basic_emotions, MAXLEN

# st.set_page_config(page_title="MBTI Personality Analyzer", page_icon="🧠", layout="wide")

# # Load CSS
# ASSETS_DIR = "assets"
# os.makedirs(ASSETS_DIR, exist_ok=True)
# style_path = os.path.join(ASSETS_DIR, "style.css")
# if os.path.exists(style_path):
#     with open(style_path, "r", encoding="utf-8") as f:
#         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# MODELS_DIR = "models"

# @st.cache_resource(show_spinner=False)
# def load_models():
#     models = {}
#     if not os.path.isdir(MODELS_DIR):
#         return models
#     for fn in sorted(os.listdir(MODELS_DIR)):
#         if fn.endswith(".keras") and not fn.endswith("_final.keras"):
#             name = fn.replace(".keras", "")
#             try:
#                 models[name] = tf.keras.models.load_model(os.path.join(MODELS_DIR, fn))
#             except Exception as e:
#                 st.warning(f"Failed to load {fn}: {e}")
#     return models

# def gauge(title, percent):
#     fig = go.Figure(go.Indicator(
#         mode="gauge+number",
#         value=percent,
#         number={'suffix': "%"},
#         gauge={'axis': {'range':[0,100]}, 'bar': {'thickness':0.3}},
#         title={'text': title}
#     ))
#     fig.update_layout(height=260, margin=dict(l=20,r=20,t=40,b=20))
#     return fig

# def ensemble_predict(text: str, models: dict):
#     X = texts_to_padded(text)  # integer padded input
#     preds, per_model = [], {}
#     for name, m in models.items():
#         p = m.predict(X, verbose=0)[0]  # [4]
#         preds.append(p)
#         per_model[name] = p.tolist()
#     if not preds:
#         return None, {}
#     avg = np.mean(np.stack(preds, axis=0), axis=0)  # [4]
#     return avg, per_model

# def present_results(avg):
#     pairs = [("E","I"),("S","N"),("T","F"),("J","P")]
#     letters, rows = [], []
#     for i,(pos,neg) in enumerate(pairs):
#         toward_pos = float(avg[i])           # prob toward E/S/T/J
#         pos_pct = round(toward_pos*100,2)
#         neg_pct = round((1-toward_pos)*100,2)
#         letter = pos if toward_pos>=0.5 else neg
#         letters.append(letter)
#         rows.append({
#             "Dimension": f"{pos}/{neg}",
#             f"{pos} %": pos_pct,
#             f"{neg} %": neg_pct,
#             "Binary (Chosen)": letter
#         })
#     mbti = "".join(letters)
#     return mbti, pd.DataFrame(rows)

# st.markdown("<h1 class='gradient-title'>MBTI Personality Analyzer</h1>", unsafe_allow_html=True)
# st.write("Enter a paragraph. The app predicts MBTI letters with percentages, shows gauges, a table, per-model scores, and emotion bars.")

# models = load_models()
# if not models:
#     st.info("No models found in ./models. Run `python train.py` to train and save them.")

# with st.sidebar:
#     st.subheader("Controls")
#     demo = st.toggle("Prefill demo text", value=True)
#     st.caption("Tip: After training, accuracy reports and confusion matrices appear in the **models/** folder. This app will read and show validation accuracy if available.")

# default_text = ("I enjoy spending time with close friends discussing ideas late into the night. "
#                 "I prefer planning ahead but I can adapt when needed. Logic matters to me, "
#                 "but I still care deeply about how decisions affect people.") if demo else ""

# text = st.text_area("Enter your text:", value=default_text, height=180, placeholder="Paste a paragraph...")

# col1, col2 = st.columns([1,1])
# with col1:
#     run = st.button("Analyze ✨", type="primary", use_container_width=True)
# with col2:
#     st.download_button("Download Sample Input", data="I love brainstorming abstract ideas and planning my week carefully.", file_name="sample.txt", mime="text/plain", use_container_width=True)

# st.markdown("---")

# if run and text.strip():
#     avg, per_model = ensemble_predict(text, models)
#     if avg is None:
#         st.warning("No models loaded. Train models first.")
#         st.stop()

#     mbti, df = present_results(avg)
#     st.markdown(f"### Predicted Type: **`{mbti}`**")

#     # Gauges
#     pairs = [("E","I"),("S","N"),("T","F"),("J","P")]
#     c1,c2,c3,c4 = st.columns(4)
#     for i, col in enumerate([c1,c2,c3,c4]):
#         pos, neg = pairs[i]
#         val = float(avg[i])*100
#         col.plotly_chart(gauge(f"{pos} ↔ {neg}", val), use_container_width=True)

#     # Table
#     st.dataframe(df, use_container_width=True)

#     # Emotions
#     st.markdown("### Emotions")
#     em = basic_emotions(text)
#     em_df = pd.DataFrame({"Emotion": list(em.keys()), "Score": list(em.values())}).sort_values("Score", ascending=False)
#     st.bar_chart(em_df.set_index("Emotion"))

#     # Per-model probabilities
#     if per_model:
#         st.markdown("### Per-Model Probabilities (toward E/S/T/J)")
#         rows = []
#         for name, v in per_model.items():
#             rows.append({"Model": name,
#                          "EI→E %": round(v[0]*100,2),
#                          "SN→S %": round(v[1]*100,2),
#                          "TF→T %": round(v[2]*100,2),
#                          "JP→J %": round(v[3]*100,2)})
#         st.dataframe(pd.DataFrame(rows), use_container_width=True)

#     # Read model validation accuracy reports
#     acc_reports = {}
#     if os.path.isdir(MODELS_DIR):
#         for fn in os.listdir(MODELS_DIR):
#             if fn.endswith("_report.json"):
#                 name = fn.replace("_report.json","")
#                 try:
#                     with open(os.path.join(MODELS_DIR, fn),"r") as f:
#                         acc_reports[name] = json.load(f)
#                 except Exception:
#                     pass

#     if acc_reports:
#         st.markdown("### Model Validation Accuracy (per dichotomy)")
#         rows = []
#         for name, rep in sorted(acc_reports.items()):
#             rows.append({
#                 "Model": name,
#                 "EI Acc": round(rep.get("EI",{}).get("accuracy", float("nan")), 3),
#                 "SN Acc": round(rep.get("SN",{}).get("accuracy", float("nan")), 3),
#                 "TF Acc": round(rep.get("TF",{}).get("accuracy", float("nan")), 3),
#                 "JP Acc": round(rep.get("JP",{}).get("accuracy", float("nan")), 3)
#             })
#         st.dataframe(pd.DataFrame(rows), use_container_width=True)

#     st.success("Analysis complete!")
# else:
#     st.info("Enter some text and click **Analyze ✨**.")




# import os, re, json, numpy as np, pandas as pd, streamlit as st, plotly.graph_objects as go, plotly.express as px, tensorflow as tf
# from data_utils import texts_to_padded, bits_to_mbti, basic_emotions, MAXLEN

# st.set_page_config(page_title="MBTI Personality Analyzer", page_icon="🧠", layout="wide")

# # Load CSS
# ASSETS_DIR = "assets"
# os.makedirs(ASSETS_DIR, exist_ok=True)
# style_path = os.path.join(ASSETS_DIR, "style.css")
# if os.path.exists(style_path):
#     with open(style_path, "r", encoding="utf-8") as f:
#         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# MODELS_DIR = "models"

# @st.cache_resource(show_spinner=False)
# def load_models():
#     models = {}
#     if not os.path.isdir(MODELS_DIR):
#         return models
#     for fn in sorted(os.listdir(MODELS_DIR)):
#         if fn.endswith(".keras") and not fn.endswith("_final.keras"):
#             name = fn.replace(".keras", "")
#             try:
#                 models[name] = tf.keras.models.load_model(os.path.join(MODELS_DIR, fn))
#             except Exception as e:
#                 st.warning(f"Failed to load {fn}: {e}")
#     return models

# def gauge(title, percent):
#     fig = go.Figure(go.Indicator(
#         mode="gauge+number",
#         value=percent,
#         number={'suffix': "%"},
#         gauge={'axis': {'range':[0,100]}, 'bar': {'thickness':0.3}},
#         title={'text': title}
#     ))
#     fig.update_layout(height=260, margin=dict(l=20,r=20,t=40,b=20))
#     return fig

# def ensemble_predict(text: str, models: dict):
#     X = texts_to_padded(text)  # integer padded input
#     preds, per_model = [], {}
#     for name, m in models.items():
#         p = m.predict(X, verbose=0)[0]  # [4]
#         preds.append(p)
#         per_model[name] = p.tolist()
#     if not preds:
#         return None, {}
#     avg = np.mean(np.stack(preds, axis=0), axis=0)  # [4]
#     return avg, per_model

# def present_results(avg):
#     pairs = [("E","I"),("S","N"),("T","F"),("J","P")]
#     letters, rows = [], []
#     for i,(pos,neg) in enumerate(pairs):
#         toward_pos = float(avg[i])           # prob toward E/S/T/J
#         pos_pct = round(toward_pos*100,2)
#         neg_pct = round((1-toward_pos)*100,2)
#         letter = pos if toward_pos>=0.5 else neg
#         letters.append(letter)
#         rows.append({
#             "Dimension": f"{pos}/{neg}",
#             f"{pos} %": pos_pct,
#             f"{neg} %": neg_pct,
#             "Binary (Chosen)": letter
#         })
#     mbti = "".join(letters)
#     return mbti, pd.DataFrame(rows)

# st.markdown("<h1 class='gradient-title'>MBTI Personality Analyzer</h1>", unsafe_allow_html=True)
# st.write("Enter a paragraph. The app predicts MBTI letters with percentages, shows gauges, a table, per-model scores, and emotion charts.")

# models = load_models()
# if not models:
#     st.info("No models found in ./models. Run `python train.py` to train and save them.")

# with st.sidebar:
#     st.subheader("Controls")
#     demo = st.toggle("Prefill demo text", value=True)
#     st.caption("Tip: After training, accuracy reports and confusion matrices appear in the **models/** folder. This app will read and show validation accuracy if available.")

# default_text = ("I enjoy spending time with close friends discussing ideas late into the night. "
#                 "I prefer planning ahead but I can adapt when needed. Logic matters to me, "
#                 "but I still care deeply about how decisions affect people.") if demo else ""

# text = st.text_area("Enter your text:", value=default_text, height=180, placeholder="Paste a paragraph...")

# col1, col2 = st.columns([1,1])
# with col1:
#     run = st.button("Analyze ✨", type="primary", use_container_width=True)
# with col2:
#     st.download_button("Download Sample Input", data="I love brainstorming abstract ideas and planning my week carefully.", file_name="sample.txt", mime="text/plain", use_container_width=True)

# st.markdown("---")

# if run and text.strip():
#     avg, per_model = ensemble_predict(text, models)
#     if avg is None:
#         st.warning("No models loaded. Train models first.")
#         st.stop()

#     mbti, df = present_results(avg)
#     st.markdown(f"### Predicted Type: **`{mbti}`**")

#     # Gauges
#     pairs = [("E","I"),("S","N"),("T","F"),("J","P")]
#     c1,c2,c3,c4 = st.columns(4)
#     for i, col in enumerate([c1,c2,c3,c4]):
#         pos, neg = pairs[i]
#         val = float(avg[i])*100
#         col.plotly_chart(gauge(f"{pos} ↔ {neg}", val), use_container_width=True)

#     # Table
#     st.dataframe(df, use_container_width=True)

#     # -------------------
#     # Emotions Section
#     # -------------------
#     st.markdown("### Emotions")

#     em = basic_emotions(text)
#     em_df = pd.DataFrame({"Emotion": list(em.keys()), "Score": list(em.values())}).sort_values("Score", ascending=False)

#     # Show table + bar chart
#     st.dataframe(em_df.set_index("Emotion"), use_container_width=True)
#     st.bar_chart(em_df.set_index("Emotion"))

#     # Radar / Spider Chart with dominant color
#     emotion_colors = {
#         "joy": "green",
#         "sadness": "blue",
#         "anger": "red",
#         "fear": "purple",
#         "surprise": "orange",
#         "trust": "teal",
#         "disgust": "brown",
#         "anticipation": "pink"
#     }

#     top_emotion = em_df.iloc[0]["Emotion"]
#     color = emotion_colors.get(top_emotion, "lightblue")

#     radar_df = em_df.copy()
#     radar_df = pd.concat([radar_df, radar_df.iloc[[0]]])  # close loop

#     fig = px.line_polar(
#         radar_df,
#         r="Score",
#         theta="Emotion",
#         line_close=True,
#         template="plotly_dark",
#         markers=True
#     )
#     fig.update_traces(fill='toself', line_color=color, fillcolor=color, opacity=0.5)
#     fig.update_layout(height=500, margin=dict(l=20,r=20,t=40,b=20))

#     st.plotly_chart(fig, use_container_width=True)

#     st.success(f"**Dominant Emotion → {top_emotion.upper()}** 🎨 (color-coded in radar chart)")

#     # -------------------
#     # Per-model probabilities
#     # -------------------
#     if per_model:
#         st.markdown("### Per-Model Probabilities (toward E/S/T/J)")
#         rows = []
#         for name, v in per_model.items():
#             rows.append({"Model": name,
#                          "EI→E %": round(v[0]*100,2),
#                          "SN→S %": round(v[1]*100,2),
#                          "TF→T %": round(v[2]*100,2),
#                          "JP→J %": round(v[3]*100,2)})
#         st.dataframe(pd.DataFrame(rows), use_container_width=True)

#     # -------------------
#     # Validation accuracy reports
#     # -------------------
#     acc_reports = {}
#     if os.path.isdir(MODELS_DIR):
#         for fn in os.listdir(MODELS_DIR):
#             if fn.endswith("_report.json"):
#                 name = fn.replace("_report.json","")
#                 try:
#                     with open(os.path.join(MODELS_DIR, fn),"r") as f:
#                         acc_reports[name] = json.load(f)
#                 except Exception:
#                     pass

#     if acc_reports:
#         st.markdown("### Model Validation Accuracy (per dichotomy)")
#         rows = []
#         for name, rep in sorted(acc_reports.items()):
#             rows.append({
#                 "Model": name,
#                 "EI Acc": round(rep.get("EI",{}).get("accuracy", float("nan")), 3),
#                 "SN Acc": round(rep.get("SN",{}).get("accuracy", float("nan")), 3),
#                 "TF Acc": round(rep.get("TF",{}).get("accuracy", float("nan")), 3),
#                 "JP Acc": round(rep.get("JP",{}).get("accuracy", float("nan")), 3)
#             })
#         st.dataframe(pd.DataFrame(rows), use_container_width=True)

#     st.success("Analysis complete!")
# else:
#     st.info("Enter some text and click **Analyze ✨**.")




# import os, re, json, numpy as np, pandas as pd, streamlit as st
# import plotly.graph_objects as go
# import plotly.express as px
# import tensorflow as tf

# from data_utils import texts_to_padded, bits_to_mbti, basic_emotions, MAXLEN

# # ---------------- Page Config -----------------
# st.set_page_config(page_title="MBTI Analyzer", page_icon="🧩", layout="wide")

# # ---------------- Custom CSS -----------------
# st.markdown("""
# <style>
# .gradient-title {
#     font-size: 2rem;
#     font-weight: 700;
#     background: -webkit-linear-gradient(45deg, #3B82F6, #9333EA);
#     -webkit-background-clip: text;
#     -webkit-text-fill-color: transparent;
#     margin-bottom: 10px;
# }
# </style>
# """, unsafe_allow_html=True)

# # ---------------- Load Models -----------------
# MODELS_DIR = "models"

# @st.cache_resource(show_spinner=False)
# def load_models():
#     models = {}
#     if not os.path.isdir(MODELS_DIR):
#         return models
#     for fn in sorted(os.listdir(MODELS_DIR)):
#         if fn.endswith(".keras") and not fn.endswith("_final.keras"):
#             name = fn.replace(".keras", "")
#             try:
#                 models[name] = tf.keras.models.load_model(os.path.join(MODELS_DIR, fn))
#             except Exception as e:
#                 st.warning(f"⚠️ Failed to load {fn}: {e}")
#     return models

# # ---------------- Helper Charts -----------------
# def gauge(title, percent):
#     fig = go.Figure(go.Indicator(
#         mode="gauge+number",
#         value=percent,
#         number={'suffix': "%"},
#         gauge={'axis': {'range':[0,100]}, 'bar': {'thickness':0.3}},
#         title={'text': title}
#     ))
#     fig.update_layout(height=250, margin=dict(l=20,r=20,t=40,b=20))
#     return fig

# def ensemble_predict(text: str, models: dict):
#     X = texts_to_padded(text)
#     preds, per_model = [], {}
#     for name, m in models.items():
#         p = m.predict(X, verbose=0)[0]  # [4]
#         preds.append(p)
#         per_model[name] = p.tolist()
#     if not preds:
#         return None, {}
#     avg = np.mean(np.stack(preds, axis=0), axis=0)  # [4]
#     return avg, per_model

# def present_results(avg):
#     pairs = [("E","I"),("S","N"),("T","F"),("J","P")]
#     letters, rows = [], []
#     for i,(pos,neg) in enumerate(pairs):
#         toward_pos = float(avg[i])
#         pos_pct = round(toward_pos*100,2)
#         neg_pct = round((1-toward_pos)*100,2)
#         letter = pos if toward_pos>=0.5 else neg
#         letters.append(letter)
#         rows.append({
#             "Dimension": f"{pos}/{neg}",
#             f"{pos} %": pos_pct,
#             f"{neg} %": neg_pct,
#             "Chosen": letter
#         })
#     mbti = "".join(letters)
#     return mbti, pd.DataFrame(rows)

# # ---------------- UI -----------------
# st.markdown("<h1 class='gradient-title'>🧩 MBTI Personality Analyzer</h1>", unsafe_allow_html=True)
# st.write("Enter text, and the app will predict MBTI letters, show gauges, emotions, sentiment, and model accuracy.")

# models = load_models()
# if not models:
#     st.warning("⚠️ No models found in ./models. Run `python train.py` first.")

# with st.sidebar:
#     st.subheader("⚙️ Controls")
#     demo = st.toggle("Use demo text", value=True)

# default_text = ("I enjoy spending time with close friends discussing ideas late into the night. "
#                 "I prefer planning ahead but I can adapt when needed. Logic matters to me, "
#                 "but I still care deeply about how decisions affect people.") if demo else ""

# text = st.text_area("✍️ Enter text:", value=default_text, height=180)

# col1, col2 = st.columns([1,1])
# with col1:
#     run = st.button("🔮 Analyze", type="primary", use_container_width=True)
# with col2:
#     st.download_button("⬇️ Download Sample Input",
#                        data="I love brainstorming abstract ideas and planning my week carefully.",
#                        file_name="sample.txt", mime="text/plain", use_container_width=True)

# st.markdown("---")

# # ---------------- Run Analysis -----------------
# if run and text.strip():
#     avg, per_model = ensemble_predict(text, models)
#     if avg is None:
#         st.warning("⚠️ No models loaded.")
#         st.stop()

#     # MBTI Prediction
#     mbti, df = present_results(avg)
#     st.markdown(f"## 🎯 Predicted Type: **`{mbti}`**")

#     # Gauges
#     pairs = [("E","I"),("S","N"),("T","F"),("J","P")]
#     c1,c2,c3,c4 = st.columns(4)
#     for i, col in enumerate([c1,c2,c3,c4]):
#         pos, neg = pairs[i]
#         val = float(avg[i])*100
#         col.plotly_chart(gauge(f"{pos} ↔ {neg}", val), use_container_width=True)

#     # Results Table
#     st.markdown("### 📊 Prediction Breakdown")
#     st.dataframe(df, use_container_width=True)

#     # Emotions
#     st.markdown("### 🎭 Emotion Analysis")
#     em = basic_emotions(text)
#     em_df = pd.DataFrame({"Emotion": list(em.keys()), "Score": list(em.values())}).sort_values("Score", ascending=False)

#     # Table + Bar
#     st.dataframe(em_df.set_index("Emotion"), use_container_width=True)
#     st.bar_chart(em_df.set_index("Emotion"))

#     # Radar Chart
#     emotion_colors = {
#         "joy": "green","sadness": "blue","anger": "red","fear": "purple",
#         "surprise": "orange","trust": "teal","disgust": "brown","anticipation": "pink"
#     }
#     top_emotion = em_df.iloc[0]["Emotion"]
#     color = emotion_colors.get(top_emotion, "lightblue")
#     radar_df = pd.concat([em_df, em_df.iloc[[0]]])  # close loop

#     fig = px.line_polar(radar_df, r="Score", theta="Emotion", line_close=True, markers=True)
#     fig.update_traces(fill='toself', line_color=color, fillcolor=color, opacity=0.5)
#     st.plotly_chart(fig, use_container_width=True)

#     st.success(f"**Dominant Emotion → {top_emotion.upper()} 🎨**")

#     # Sentiment Pie
#     st.markdown("### 😊 Sentiment Balance")
#     sentiment = {
#         "Positive": float(em.get("joy",0)+em.get("trust",0)+em.get("anticipation",0)),
#         "Negative": float(em.get("anger",0)+em.get("fear",0)+em.get("sadness",0)+em.get("disgust",0)),
#         "Neutral": float(em.get("surprise",0))
#     }
#     pie_df = pd.DataFrame({"Sentiment": sentiment.keys(), "Value": sentiment.values()})
#     fig2 = px.pie(pie_df, names="Sentiment", values="Value", hole=0.4,
#                   color="Sentiment", color_discrete_map={"Positive":"green","Negative":"red","Neutral":"gray"})
#     st.plotly_chart(fig2, use_container_width=True)

#     # Per-model probs
#     if per_model:
#         st.markdown("### 🤖 Per-Model Probabilities")
#         rows = []
#         for name, v in per_model.items():
#             rows.append({
#                 "Model": name,
#                 "EI→E %": round(v[0]*100,2),
#                 "SN→S %": round(v[1]*100,2),
#                 "TF→T %": round(v[2]*100,2),
#                 "JP→J %": round(v[3]*100,2)
#             })
#         st.dataframe(pd.DataFrame(rows), use_container_width=True)

#     # Validation Accuracy Reports
#     acc_reports = {}
#     if os.path.isdir(MODELS_DIR):
#         for fn in os.listdir(MODELS_DIR):
#             if fn.endswith("_report.json"):
#                 name = fn.replace("_report.json","")
#                 try:
#                     with open(os.path.join(MODELS_DIR, fn),"r") as f:
#                         acc_reports[name] = json.load(f)
#                 except: pass

#     if acc_reports:
#         st.markdown("### 📈 Model Validation Accuracy")
#         rows = []
#         for name, rep in sorted(acc_reports.items()):
#             rows.append({
#                 "Model": name,
#                 "EI Acc": rep.get("EI",{}).get("accuracy", None),
#                 "SN Acc": rep.get("SN",{}).get("accuracy", None),
#                 "TF Acc": rep.get("TF",{}).get("accuracy", None),
#                 "JP Acc": rep.get("JP",{}).get("accuracy", None)
#             })
#         acc_df = pd.DataFrame(rows)
#         st.dataframe(acc_df, use_container_width=True)

#         # Heatmap for quick view
#         acc_melt = acc_df.melt(id_vars="Model", var_name="Dichotomy", value_name="Accuracy")
#         fig3 = px.density_heatmap(acc_melt, x="Dichotomy", y="Model", z="Accuracy",
#                                   color_continuous_scale="Blues", text_auto=True)
#         st.plotly_chart(fig3, use_container_width=True)

#     st.success("✅ Analysis complete!")
# else:
#     st.info("✍️ Enter some text and click **Analyze 🔮**.")





import os, re, json, numpy as np, pandas as pd, streamlit as st, plotly.graph_objects as go, plotly.express as px, tensorflow as tf
from data_utils import texts_to_padded, bits_to_mbti, basic_emotions, MAXLEN
from ocr_utils import extract_text_from_uploaded_file

st.set_page_config(page_title="MBTI Personality Analyzer", page_icon="🧠", layout="wide")

# Load CSS
ASSETS_DIR = "assets"
os.makedirs(ASSETS_DIR, exist_ok=True)
style_path = os.path.join(ASSETS_DIR, "style.css")
if os.path.exists(style_path):
    with open(style_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

MODELS_DIR = "models"

@st.cache_resource(show_spinner=False)
def load_models():
    models = {}
    if not os.path.isdir(MODELS_DIR):
        return models
    for fn in sorted(os.listdir(MODELS_DIR)):
        if fn.endswith(".keras") and not fn.endswith("_final.keras"):
            name = fn.replace(".keras", "")
            try:
                models[name] = tf.keras.models.load_model(os.path.join(MODELS_DIR, fn))
            except Exception as e:
                st.warning(f"Failed to load {fn}: {e}")
    return models

def gauge(title, percent):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=percent,
        number={'suffix': "%"},
        gauge={'axis': {'range':[0,100]}, 'bar': {'thickness':0.3}},
        title={'text': title}
    ))
    fig.update_layout(height=260, margin=dict(l=20,r=20,t=40,b=20))
    return fig

def ensemble_predict(text: str, models: dict):
    X = texts_to_padded(text)  # integer padded input
    preds, per_model = [], {}
    for name, m in models.items():
        p = m.predict(X, verbose=0)[0]  # [4]
        preds.append(p)
        per_model[name] = p.tolist()
    if not preds:
        return None, {}
    avg = np.mean(np.stack(preds, axis=0), axis=0)  # [4]
    return avg, per_model

def present_results(avg):
    pairs = [("E","I"),("S","N"),("T","F"),("J","P")]
    letters, rows = [], []
    for i,(pos,neg) in enumerate(pairs):
        toward_pos = float(avg[i])           # prob toward E/S/T/J
        pos_pct = round(toward_pos*100,2)
        neg_pct = round((1-toward_pos)*100,2)
        letter = pos if toward_pos>=0.5 else neg
        letters.append(letter)
        rows.append({
            "Dimension": f"{pos}/{neg}",
            f"{pos} %": pos_pct,
            f"{neg} %": neg_pct,
            "Binary (Chosen)": letter
        })
    mbti = "".join(letters)
    return mbti, pd.DataFrame(rows)

st.markdown("<h1 class='gradient-title'>MBTI Personality Analyzer</h1>", unsafe_allow_html=True)
st.write("Enter text or upload an image containing text. The app predicts MBTI letters with percentages, shows gauges, a table, per-model scores, and emotion charts.")

models = load_models()
if not models:
    st.info("No models found in ./models. Run `python train.py` to train and save them.")

with st.sidebar:
    st.subheader("Controls")
    demo = st.toggle("Prefill demo text", value=True)
    input_method = st.radio(
        "Input Method:",
        ["📝 Text", "🖼️ Image (OCR)"],
        index=0
    )
    st.caption("Tip: After training, accuracy reports and confusion matrices appear in the **models/** folder. This app will read and show validation accuracy if available.")

text = ""
uploaded_image = None

if input_method == "📝 Text":
    default_text = ("I enjoy spending time with close friends discussing ideas late into the night. "
                    "I prefer planning ahead but I can adapt when needed. Logic matters to me, "
                    "but I still care deeply about how decisions affect people.") if demo else ""
    text = st.text_area("Enter your text:", value=default_text, height=180, placeholder="Enter a paragraph...")
else:
    st.markdown("### Upload an image with text")
    uploaded_image = st.file_uploader(
        "Choose an image file (PNG, JPG, JPEG)",
        type=['png', 'jpg', 'jpeg'],
        help="Upload an image containing text. The app will extract text using OCR and analyze it."
    )
    
    if uploaded_image is not None:
        col1, col2 = st.columns(2)
        with col1:
            st.image(uploaded_image, caption="Uploaded Image", width="stretch")
        
        with col2:
            st.write("**Extracting text from image...**")
            with st.spinner("Processing image with OCR..."):
                extracted_text, image_bytes = extract_text_from_uploaded_file(uploaded_image)
                
            if extracted_text:
                st.success("✅ Text extracted successfully!")
                st.text_area(
                    "Extracted Text:",
                    extracted_text,
                    height=150,
                    disabled=True
                )
                text = extracted_text
            else:
                st.warning("⚠️ No text could be extracted from the image. Please try another image.")
                text = ""

col1, col2 = st.columns([1,1])
with col1:
    run = st.button("Analyze ✨", type="primary", width="stretch")
with col2:
    st.download_button("Download Sample Input", data="I love brainstorming abstract ideas and planning my week carefully.", file_name="sample.txt", mime="text/plain", width="stretch")

st.markdown("---")

if run and text.strip():
    avg, per_model = ensemble_predict(text, models)
    if avg is None:
        st.warning("No models loaded. Train models first.")
        st.stop()

    mbti, df = present_results(avg)
    st.markdown(f"### Predicted Type: **`{mbti}`**")

    # Gauges
    pairs = [("E","I"),("S","N"),("T","F"),("J","P")]
    c1,c2,c3,c4 = st.columns(4)
    for i, col in enumerate([c1,c2,c3,c4]):
        pos, neg = pairs[i]
        val = float(avg[i])*100
        col.plotly_chart(gauge(f"{pos} ↔ {neg}", val), width="stretch")

    # Table
    st.dataframe(df, width="stretch")

    # -------------------
    # Emotions Section
    # -------------------
    st.markdown("### Emotions")

    em = basic_emotions(text)
    em_df = pd.DataFrame({"Emotion": list(em.keys()), "Score": list(em.values())}).sort_values("Score", ascending=False)

    # Show table + bar chart
    st.dataframe(em_df.set_index("Emotion"), width="stretch")
    st.bar_chart(em_df.set_index("Emotion"))

    # Radar / Spider Chart with dominant color
    emotion_colors = {
        "joy": "green",
        "sadness": "blue",
        "anger": "red",
        "fear": "purple",
        "surprise": "orange",
        "trust": "teal",
        "disgust": "brown",
        "anticipation": "pink"
    }

    top_emotion = em_df.iloc[0]["Emotion"]
    color = emotion_colors.get(top_emotion, "lightblue")

    radar_df = em_df.copy()
    radar_df = pd.concat([radar_df, radar_df.iloc[[0]]])  # close loop

    fig = px.line_polar(
        radar_df,
        r="Score",
        theta="Emotion",
        line_close=True,
        template="plotly_dark",
        markers=True
    )
    fig.update_traces(fill='toself', line_color=color, fillcolor=color, opacity=0.5)
    fig.update_layout(height=500, margin=dict(l=20,r=20,t=40,b=20))

    st.plotly_chart(fig, width="stretch")

    st.success(f"**Dominant Emotion → {top_emotion.upper()}** 🎨 (color-coded in radar chart)")

    # -------------------
    # Per-model probabilities
    # -------------------
    if per_model:
        st.markdown("### Per-Model Probabilities (toward E/S/T/J)")
        rows = []
        for name, v in per_model.items():
            rows.append({"Model": name,
                         "EI→E %": round(v[0]*100,2),
                         "SN→S %": round(v[1]*100,2),
                         "TF→T %": round(v[2]*100,2),
                         "JP→J %": round(v[3]*100,2)})
        st.dataframe(pd.DataFrame(rows), width="stretch")

    # -------------------
    # Validation accuracy reports
    # -------------------
    acc_reports = {}
    if os.path.isdir(MODELS_DIR):
        for fn in os.listdir(MODELS_DIR):
            if fn.endswith("_report.json"):
                name = fn.replace("_report.json","")
                try:
                    with open(os.path.join(MODELS_DIR, fn),"r") as f:
                        acc_reports[name] = json.load(f)
                except Exception:
                    pass

    if acc_reports:
        st.markdown("### Model Validation Accuracy (per dichotomy)")
        rows = []
        for name, rep in sorted(acc_reports.items()):
            rows.append({
                "Model": name,
                "EI Acc": round(rep.get("EI",{}).get("accuracy", float("nan")), 3),
                "SN Acc": round(rep.get("SN",{}).get("accuracy", float("nan")), 3),
                "TF Acc": round(rep.get("TF",{}).get("accuracy", float("nan")), 3),
                "JP Acc": round(rep.get("JP",{}).get("accuracy", float("nan")), 3)
            })
        st.dataframe(pd.DataFrame(rows), width="stretch")

    st.success("Analysis complete!")
else:
    st.info("Enter some text and click **Analyze ✨**.")

