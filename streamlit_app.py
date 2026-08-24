from __future__ import annotations

import re
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="DU Pathways IU Interactive Repo", layout="wide")

REPO_ROOT = Path(__file__).resolve().parent
PAGES_DIR = REPO_ROOT / "pages"
FIGURES_DIR = REPO_ROOT / "figures"

GALLERY_COLUMNS = 3


def _label_from_filename(path: Path) -> str:
    """Turn '1_Figure_1_Performance_Objectives.py' into 'Figure 1 Performance Objectives'."""
    stem = re.sub(r"^\d+_?", "", path.stem)
    return stem.replace("_", " ").strip()


def _figure_number(path: Path) -> str | None:
    """Turn '1_Figure_1_Performance_Objectives.py' into '1'."""
    match = re.match(r"^(\d+)_", path.stem)
    return match.group(1) if match else None


def _thumbnail_for(path: Path) -> Path | None:
    """Find the figures/results_fig<N>_*.jpg matching a page's leading number."""
    number = _figure_number(path)
    if number is None or not FIGURES_DIR.exists():
        return None
    matches = sorted(FIGURES_DIR.glob(f"results_fig{number}_*.jpg"))
    return matches[0] if matches else None


def _discover_figure_pages() -> list[tuple[Path, str]]:
    """Return results-figure pages (prefix 1–9), excluding the regional test case."""
    if not PAGES_DIR.exists():
        return []
    page_files = sorted(
        (p for p in PAGES_DIR.glob("[1-9]*.py") if not p.name.startswith("_")),
        key=lambda p: p.name,
    )
    return [(p, _label_from_filename(p)) for p in page_files]


def _url_path_for(label: str) -> str:
    """Turn 'Figure 1 Performance Objectives' into 'Figure_1_Performance_Objectives'."""
    return label.replace(" ", "_")


def render_home() -> None:
    st.title("DU Pathways IU — Interactive Results Explorer")
    st.write(
        "This app hosts interactive, clickable versions of the figures from the "
        "accompanying paper. Select a section below, or use the sidebar, to navigate."
    )

    st.markdown("---")

    st.subheader("Explore the Regional Test Case")
    st.write(
        "Learn about the Sedento Valley regional test case: the three cooperating "
        "utilities (Watertown, Dryville, Fallsland), their water sources, "
        "infrastructure options, and demand growth projections."
    )
    st.page_link(regional_test_case_page, label="Open Regional Test Case Explorer", icon="🗺️")

    st.markdown("---")

    st.subheader("View the Results")
    st.write(
        "Browse interactive, clickable versions of all results figures from the "
        "paper, including performance trade-offs, robustness, degradation, "
        "decision variables, compromise solutions, infrastructure timing, and "
        "sensitivity analysis."
    )
    st.page_link(results_page, label="Open Results Gallery", icon="📊")

    st.markdown("---")
    with st.expander("About this repository"):
        st.write(
            "This is the interactive companion site for the paper's metarepo. "
            "Static figures live in `figures/`, the plotting scripts that "
            "produced them live in `scripts/Figure Plotting/`, and each "
            "interactive explorer lives as its own page under `pages/`. "
            "New figures can be added by dropping a new `N_Figure_Name.py` file "
            "into `pages/` — along with a matching `figures/results_figN_*.jpg` "
            "thumbnail — and it will automatically appear in the sidebar and gallery."
        )


def render_results_gallery() -> None:
    st.title("DU Pathways IU — Results Gallery")
    st.write(
        "Interactive, clickable versions of the results figures from the "
        "accompanying paper. Use the gallery below, or the sidebar, to open a "
        "figure explorer."
    )

    st.markdown("---")
    st.subheader("Explore the figures below")
    st.caption("Click a thumbnail to open its interactive explorer.")

    pages = _discover_figure_pages()

    if not pages:
        st.info("No figure explorer pages found yet in `pages/`.")
    else:
        for row_start in range(0, len(pages), GALLERY_COLUMNS):
            row = pages[row_start : row_start + GALLERY_COLUMNS]
            cols = st.columns(GALLERY_COLUMNS)
            for col, (page_path, label) in zip(cols, row):
                with col:
                    with st.container(border=True):
                        thumbnail = _thumbnail_for(page_path)
                        url_path = _url_path_for(label)
                        if thumbnail is not None:
                            st.image(str(thumbnail), width="stretch", link=url_path)
                        else:
                            st.info("No preview image found.")
                        st.page_link(
                            f"pages/{page_path.name}",
                            label=label,
                            icon="📊",
                        )

    st.markdown("---")
    with st.expander("About this repository"):
        st.write(
            "Static figures live in `figures/`, plotting scripts in "
            "`scripts/Figure Plotting/`, and each interactive explorer lives as "
            "its own page under `pages/`. New figures can be added by dropping a "
            "new `N_Figure_Name.py` file into `pages/` — along with a matching "
            "`figures/results_figN_*.jpg` thumbnail — and it will automatically "
            "appear in the sidebar and gallery."
        )


# ---------------------------------------------------------------------------
# Page definitions
# ---------------------------------------------------------------------------
regional_test_case_page = st.Page(
    "pages/0_Regional_Test_Case.py",
    title="Regional Test Case",
    icon="🗺️",
    url_path="Regional_Test_Case",
)

results_page = st.Page(
    render_results_gallery,
    title="View the Results",
    icon="📊",
    url_path="View_the_Results",
)

figure_pages = [
    st.Page(
        str(page_path),
        title=label,
        icon="📊",
        url_path=_url_path_for(label),
    )
    for page_path, label in _discover_figure_pages()
]

home_page = st.Page(render_home, title="Home Page", icon="🏠", default=True)

# ---------------------------------------------------------------------------
# Navigation: sections group pages visually in the sidebar.
# Empty-string key creates an untitled section for the home page.
# ---------------------------------------------------------------------------
nav = st.navigation(
    {
        "": [home_page],
        "Regional Test Case": [regional_test_case_page],
        "Results": [results_page, *figure_pages],
    }
)
nav.run()
