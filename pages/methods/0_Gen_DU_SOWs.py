from __future__ import annotations

from method_step_explorer import render_method_step

SCRIPTS = [
    dict(
        name="gen_RDM_samples.sh",
        kind="Shell script",
        description=(
            "Invokes the MOEAFramework `SampleGenerator` (Java, via "
            "`MOEAFramework-3.5-Demo.jar`) with Latin hypercube sampling "
            "(`-m latin`, `-n 250`) over parameter ranges defined in "
            "`rdm_ranges_actions_conf.txt`, producing "
            "`rdm_ranges_actions_conf_neg.txt`. It then converts the "
            "space-delimited output to a CSV "
            "(`rdm_ranges_actions_conf_neg.csv`) via `sed`."
        ),
    ),
    dict(
        name="0_convert_to_csv.py",
        kind="Python script",
        description=(
            "Command-line utility (`python 0_convert_to_csv.py <input_file> "
            "<output_file>`) that reads a whitespace-delimited `.txt` file, "
            "drops the first column, and writes the result as two CSVs — one "
            "with a header row and one plain-values file. Used to "
            "post-process outputs like the RDM sample file above."
        ),
    ),
]

render_method_step(
    page_heading="Step 0: Generate the DU SOWs",
    intro=(
        "Before any simulation runs, we need a sample of Deeply Uncertain "
        "(DU) States of the World (SOWs) — combinations of demand growth, "
        "hydrology, and financial/regulatory parameters that the region "
        "might plausibly face. This step uses Latin Hypercube sampling to "
        "draw 200 candidate DU SOWs (also called RDMs, for Robust Decision-Making parameters"
        "spanning wide ranges for each uncertain parameter, "
        "then converts the sampled values into the CSV format consumed by "
        "every downstream step."
    ),
    folder_relpath="scripts/0-Gen DU SOWs",
    scripts=SCRIPTS,
    about_text=(
        "This is the first step in the DU Pathways IU methodology: Sampling "
        "the deeply uncertain states of the world that everything else — "
        "synthetic streamflow generation, ROF tables, optimization, and "
        "re-evaluation — is conditioned on. See `scripts/0-Gen DU SOWs` in "
        "the repository for the underlying code."
    ),
)
