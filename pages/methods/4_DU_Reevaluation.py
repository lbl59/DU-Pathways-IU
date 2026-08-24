from __future__ import annotations

from method_step_explorer import render_method_step

SCRIPTS = [
    dict(
        name="full_reeval_loop_IU.sh",
        kind="SLURM launcher",
        description=(
            "SLURM script (4 nodes × 50 tasks, regular QOS, 10h) that times "
            "and runs `full_reeval_loop_IU_script.py` via `srun`."
        ),
    ),
    dict(
        name="full_reeval_loop_IU_script.py",
        kind="MPI dispatcher",
        description=(
            "Splits 200 RDMs across ranks (expects exactly 200 ranks) and, "
            "per RDM, runs `SedentoValleySimulation` in reevaluation mode "
            "(`-M 1`, `-p 0`) against the IU decision-variable set "
            "`objectives_dvs/dvs_IU_nd_truncated_extremes.csv` (628 "
            "solutions, `p90`/worst-case mode), writing to "
            "`output_reeval_IU_v3/`."
        ),
    ),
    dict(
        name="full_reeval_loop_base.sh",
        kind="SLURM launcher",
        description=(
            "SLURM script (4 nodes × 50 tasks, debug QOS, 30 min) that "
            "times and runs `full_reeval_loop_base_script.py`."
        ),
    ),
    dict(
        name="full_reeval_loop_base_script.py",
        kind="MPI dispatcher",
        description=(
            "Same pattern as the IU version but for the 'base' solution "
            "set: `objectives_dvs/dvs_base_nd_truncated_extremes.csv` (46 "
            "solutions, `avg` mode), writing to "
            "`output_reeval_base_avg_v3/`."
        ),
    ),
]

render_method_step(
    page_heading="Step 4: Perform DU Re-Evaluation",
    intro=(
        "Every candidate pathway strategy found in Step 3 is re-simulated "
        "here against the full, broader deep-uncertainty ensemble — all "
        "200 RDMs × 200 realizations — rather than the smaller sample used "
        "during search. This is what lets us measure each strategy's true "
        "**robustness**: the percentage of futures in which it still meets "
        "all three robustness criteria. Both the baseline and IU-DU "
        "non-dominated solution sets are re-evaluated in parallel, each "
        "with its own MPI dispatcher script."
    ),
    folder_relpath="scripts/4-DU Reevaluation",
    scripts=SCRIPTS,
    about_text=(
        "The robustness scores computed in this step feed directly into "
        "Figure 2 (robustness rankings) and Figure 3 (performance "
        "degradation) in Step 6. See `scripts/4-DU Reevaluation` in the "
        "repository for the underlying code."
    ),
)
