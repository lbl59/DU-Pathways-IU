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
        "This app hosts an interactive companion to the paper: a step-by-step "
        "walkthrough of the methods, and clickable versions of the results "
        "figures. Select a section below, or use the sidebar, to navigate."
    )

    st.markdown("---")

    st.subheader("Walk through our methods")
    st.write(
        "Follow the full workflow from generating the deeply uncertain states "
        "of the world through synthetic streamflow generation, ROF table "
        "generation, DU optimization, DU re-evaluation, IU re-evaluation, and "
        "figure plotting — with every script along the way documented."
    )
    st.page_link(methods_overview_page, label="Open Methods Walkthrough", icon="🧭")

    st.markdown("---")

    st.subheader("Explore our results")
    st.write(
        "Learn about the Sedento Valley regional test case, and browse "
        "interactive, clickable versions of all results figures from the "
        "paper, including performance trade-offs, robustness, degradation, "
        "decision variables, compromise solutions, infrastructure timing, and "
        "sensitivity analysis."
    )
    st.page_link(regional_test_case_page, label="Open Regional Test Case Explorer", icon="🗺️")
    st.page_link(results_page, label="Open Results Gallery", icon="📊")

    st.markdown("---")
    with st.expander("About this repository"):
        st.write(
            "This is the interactive companion site for the paper's metarepo. "
            "The methods walkthrough pages document the scripts under "
            "`scripts/`, static figures live in `figures/`, the plotting "
            "scripts that produced them live in "
            "`scripts/6-Figure Plotting/`, and each interactive explorer "
            "lives as its own page under `pages/`. New figures can be added "
            "by dropping a new `N_Figure_Name.py` file into `pages/` — along "
            "with a matching `figures/results_figN_*.jpg` thumbnail — and it "
            "will automatically appear in the sidebar and gallery."
        )


def render_methods_overview() -> None:
    st.title("DU Pathways IU — Methods Walkthrough")
    st.write(
        "Follow the full workflow used to produce this paper's results, from "
        "sampling deeply uncertain states of the world through to plotting "
        "the final figures. Each step below documents the scripts in its "
        "matching `scripts/` subfolder — what each script does, and how it "
        "connects to the rest of the pipeline."
    )

    st.markdown("---")
    st.subheader("Follow the steps below")
    st.caption("Click a step to see its scripts and how it fits into the overall workflow.")

    for page_path, title, icon, _url_path, description in METHOD_STEPS:
        with st.container(border=True):
            st.markdown(f"#### {icon} {title}")
            st.write(description)
            st.page_link(page_path, label=f"Open {title}", icon=icon)

    st.markdown("---")
    with st.expander("About this repository"):
        st.write(
            "Each step's page documents the scripts under its matching "
            "`scripts/` subfolder (e.g. `scripts/0-Gen DU SOWs` for Step 0). "
            "Once you've walked through the methods, see **Explore our "
            "results** in the sidebar for interactive versions of the "
            "figures these scripts produce."
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

# Each entry mirrors a subfolder under `scripts/`: (page file, sidebar title,
# icon, url slug, one-line description). Titles intentionally spell out
# "Step N" since that's how the paper's methodology is organized, even
# though the underlying folder names are just topic names
# (e.g. `scripts/0-Gen DU SOWs`).
METHOD_STEPS = [
    (
        "pages/methods/0_Gen_DU_SOWs.py",
        "Step 0: Generate the DU SOWs",
        "🧪",
        "Step_0_Generate_the_DU_SOWs",
        "Sample 250 deeply uncertain states of the world (RDMs) via Latin "
        "hypercube sampling — the foundation every later step is "
        "conditioned on.",
    ),
    (
        "pages/methods/1_Synthetic_Streamflow_Generation.py",
        "Step 1: Generate Synthetic Inputs",
        "🌊",
        "Step_1_Generate_Synthetic_Inputs",
        "Build the synthetic hydrology and demand ensembles — annual "
        "demand growth, weekly streamflow/evaporation, and conditioned "
        "weekly demand — for each sampled state of the world.",
    ),
    (
        "pages/methods/2_ROF_Table_Generation.py",
        "Step 2: Generate ROF Tables",
        "📈",
        "Step_2_Generate_ROF_Tables",
        "Pre-compute risk-of-failure lookup tables so the WaterPaths "
        "simulator doesn't have to recalculate ROF at every timestep "
        "during optimization and re-evaluation.",
    ),
    (
        "pages/methods/3_DU_Optimization.py",
        "Step 3: Perform DU Optimization",
        "⚙️",
        "Step_3_Perform_DU_Optimization",
        "Search for candidate pathway strategies with the Borg MOEA, "
        "running parallel Baseline DU and IU-DU optimizations across "
        "thousands of MPI ranks.",
    ),
    (
        "pages/methods/4_DU_Reevaluation.py",
        "Step 4: Perform DU Re-Evaluation",
        "🔁",
        "Step_4_Perform_DU_Reevaluation",
        "Re-simulate every candidate strategy across the full 200×200 "
        "deep-uncertainty ensemble to measure its true robustness.",
    ),
    (
        "pages/methods/5_IU_Reevaluation.py",
        "Step 5: Perform IU Re-Evaluation",
        "🔄",
        "Step_5_Perform_IU_Reevaluation",
        "Perturb selected high-performing strategies' decision variables "
        "and re-simulate them to quantify performance degradation under "
        "imperfect implementation.",
    ),
    (
        "pages/methods/6_Figure_Plotting.py",
        "Step 6: Plot the Figures",
        "🖼️",
        "Step_6_Plot_the_Figures",
        "Turn the raw optimization and re-evaluation output into the "
        "paper's figures, using reusable helper modules and per-figure "
        "driver scripts.",
    ),
]

method_step_pages = [
    st.Page(page_path, title=title, icon=icon, url_path=url_path)
    for page_path, title, icon, url_path, _description in METHOD_STEPS
]

methods_overview_page = st.Page(
    render_methods_overview,
    title="Methods Overview",
    icon="🧭",
    url_path="Methods_Overview",
)

method_pages = [methods_overview_page, *method_step_pages]

# ---------------------------------------------------------------------------
# Navigation: sections group pages visually in the sidebar.
# Empty-string key creates an untitled section for the home page.
# ---------------------------------------------------------------------------
nav = st.navigation(
    {
        "": [home_page],
        "Walk through our methods": method_pages,
        "Explore our results": [regional_test_case_page, results_page, *figure_pages],
    }
)
nav.run()
