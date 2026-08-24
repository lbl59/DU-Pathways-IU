from __future__ import annotations

import streamlit as st


def render_method_step(
    *,
    page_heading: str,
    intro: str,
    folder_relpath: str,
    scripts: list[dict],
    about_text: str,
    note: str | None = None,
) -> None:
    """Render a "methods walkthrough" page describing one step's scripts folder.

    This is the shared rendering engine behind every "Step N" page in
    ``pages/methods/``. Each page just supplies its own heading, intro
    paragraph, the ``scripts/`` subfolder it documents, and a list of script
    dicts (each with ``name``, ``kind``, and ``description``).

    Note: this function intentionally does *not* call ``st.set_page_config``
    — that can only be called once per app run, and ``streamlit_app.py``
    (the ``st.navigation`` router) already calls it once for the whole app.

    Parameters
    ----------
    page_heading:
        Heading shown via ``st.title`` at the top of the page.
    intro:
        Intro paragraph(s) shown under the heading, explaining what this
        step accomplishes and how it fits into the overall DU/IU workflow.
    folder_relpath:
        Path to the scripts subfolder, relative to the repo root (e.g.
        ``"scripts/0-Gen DU SOWs"``), shown as a caption.
    scripts:
        List of dicts, each with keys ``name`` (filename), ``kind`` (short
        tag like "Python script" or "SLURM launcher"), and ``description``.
    about_text:
        Text shown inside the "About this page" expander.
    note:
        Optional callout text (e.g. data subfolders, known issues) shown
        in an ``st.info`` box above the script list.
    """
    st.title(page_heading)
    st.write(intro)
    st.caption(f"📁 `{folder_relpath}`")

    if note:
        st.info(note)

    st.markdown("---")
    st.subheader("Scripts in this step")
    st.caption("Click a script to see what it does.")

    if not scripts:
        st.warning("No scripts documented for this step yet.")
    else:
        for s in scripts:
            label = f"`{s['name']}`"
            if s.get("kind"):
                label += f" — {s['kind']}"
            with st.expander(label):
                st.write(s["description"])

    st.markdown("---")
    with st.expander("About this page"):
        st.write(about_text)
