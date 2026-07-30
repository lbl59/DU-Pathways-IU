from __future__ import annotations

import re
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="DU Pathways IU Interactive Repo", layout="wide")

REPO_ROOT = Path(__file__).resolve().parent
PAGES_DIR = REPO_ROOT / "pages"


def _label_from_filename(path: Path) -> str:
    """Turn '1_Figure_1_Explorer.py' into 'Figure 1 Explorer'."""
    stem = re.sub(r"^\d+_?", "", path.stem)  # drop Streamlit's leading order number
    return stem.replace("_", " ").strip()


def _discover_pages() -> list[tuple[Path, str]]:
    if not PAGES_DIR.exists():
        return []
    page_files = sorted(
        (p for p in PAGES_DIR.glob("*.py") if not p.name.startswith("_")),
        key=lambda p: p.name,
    )
    return [(p, _label_from_filename(p)) for p in page_files]


st.title("DU Pathways IU — Interactive Results Explorer")
st.write(
    "This app hosts interactive, clickable versions of the figures from the "
    "accompanying paper. Use the sidebar, or the links below, to open a "
    "figure explorer."
)

st.markdown("---")
st.subheader("Available figure explorers")

pages = _discover_pages()

if not pages:
    st.info("No figure explorer pages found yet in `pages/`.")
else:
    for page_path, label in pages:
        st.page_link(f"pages/{page_path.name}", label=label, icon="📊")

st.markdown("---")
with st.expander("About this repository"):
    st.write(
        "This is the interactive companion site for the paper's metarepo. "
        "Static figures live in `figures/`, the plotting scripts that "
        "produced them live in `scripts/Figure Plotting/`, and each "
        "interactive explorer lives as its own page under `pages/`. New "
        "figures can be added by dropping a new `N_Figure_Name.py` file into "
        "`pages/` — it will automatically appear both in Streamlit's sidebar "
        "navigation and in the list above."
    )
