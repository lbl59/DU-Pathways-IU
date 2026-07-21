from __future__ import annotations

import csv
from pathlib import Path

import streamlit as st


def _load_csv_rows(raw_text: str) -> list[dict[str, str]]:
    reader = csv.DictReader(raw_text.splitlines())
    return [row for row in reader if row]


def _to_float(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


st.set_page_config(page_title="DU Pathways Interactive Results", layout="wide")
st.title("DU Pathways Interactive Results")
st.write("Upload a CSV of model results and interactively filter numeric columns.")

uploaded_file = st.file_uploader("Upload results CSV", type=["csv"])
rows: list[dict[str, str]] = []

if uploaded_file is not None:
    rows = _load_csv_rows(uploaded_file.getvalue().decode("utf-8"))
else:
    default_csv = Path("results.csv")
    if default_csv.exists():
        rows = _load_csv_rows(default_csv.read_text(encoding="utf-8"))

if not rows:
    st.info("No data loaded yet. Upload a CSV file to begin.")
    st.stop()

numeric_columns = [
    column
    for column in rows[0]
    if any(_to_float(row.get(column, "")) is not None for row in rows)
]

if not numeric_columns:
    st.write(rows)
    st.stop()

selected_column = st.selectbox("Numeric column to filter", options=numeric_columns)
numeric_values = [
    _to_float(row.get(selected_column, ""))
    for row in rows
    if _to_float(row.get(selected_column, "")) is not None
]

threshold = st.slider(
    "Minimum value",
    min_value=float(min(numeric_values)),
    max_value=float(max(numeric_values)),
    value=float(min(numeric_values)),
)

filtered_rows = [
    row
    for row in rows
    if (_to_float(row.get(selected_column, "")) or float("-inf")) >= threshold
]

st.metric("Rows after filter", len(filtered_rows))
st.dataframe(filtered_rows, use_container_width=True)
