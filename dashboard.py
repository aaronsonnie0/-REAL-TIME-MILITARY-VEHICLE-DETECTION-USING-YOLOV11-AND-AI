import streamlit as st
import pandas as pd
import os
from PIL import Image

st.set_page_config(page_title="Military Alert Dashboard", layout="wide")
st.title("🛡️ Military AI Alert Dashboard")

# Load detection log
def load_log():
    log_path = os.path.join(os.getcwd(), "detection_log.csv")
    if os.path.exists(log_path):
        try:
            # Try loading with error skipping
            log = pd.read_csv(log_path, on_bad_lines='skip')
            # Optionally, warn if lines were skipped (no direct count, so check shape)
            with open(log_path, 'r', encoding='utf-8') as f:
                n_lines = sum(1 for _ in f) - 1  # minus header
            # No warning if rows are skipped
            return log
        except Exception as e:
            st.error(f"Error loading detection log: {e}")
            return pd.DataFrame()
    else:
        return pd.DataFrame()

def threat_color(level):
    if isinstance(level, str):
        if level.lower() == "high": return "#ff4d4d"
        if level.lower() == "medium": return "#ffd700"
        if level.lower() == "low": return "#90ee90"
    return "#d3d3d3"

log = load_log()

if log.empty:
    st.warning("No detection data found.")
else:
    st.dataframe(log, use_container_width=True)
    st.markdown("---")
    # Show recent annotated images
    st.subheader("Recent Detections")
    cols = st.columns(3)
    for i, row in log.tail(9).iterrows():
        with cols[i % 3]:
            st.markdown(f"**{row['timestamp']}**")
            if os.path.exists(row['output_file']):
                img = Image.open(row['output_file'])
                st.image(img, caption=f"Threat: {row['threat_level']}", width=300)
                st.markdown(f"<div style='background-color:{threat_color(row['threat_level'])};padding:5px;border-radius:5px'><b>Threat Level:</b> {row['threat_level']}</div>", unsafe_allow_html=True)
            else:
                st.write("Image not found.")
