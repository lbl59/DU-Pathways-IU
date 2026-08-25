from __future__ import annotations

from method_step_explorer import render_method_step

SCRIPTS = [
    dict(
        name="make_perturbed_solutions.py",
        kind="Python script",
        description=(
            "Generates the perturbed decision-variable files consumed by "
            "the reevaluation scripts below. For a set of selected "
            "solutions, it applies decision-variable "
            "perturbations (drawn from `rdm_ranges_actions_500conf_h.csv`) "
            "to each solution's baseline decision-variable values, clips "
            "the results to [0, 1], and writes "
            "`objectives_dvs/dvs_reeval_perturbed/dvs_perturbations_<mode>_s<sol>.csv`."
        ),
    ),
    dict(
        name="full_reeval_w_ptb_IU.sh",
        kind="SLURM launcher",
        description=(
            "SLURM script (4 nodes × 100 tasks, 2 cpus/task, regular QOS, "
            "35 min) that runs "
            "`full_reeval_w_ptb_IU_script_v2.py 'IU' 175 400` (400 MPI "
            "ranks) — i.e., reevaluate perturbations of IU solution #175."
        ),
    ),
    dict(
        name="full_reeval_w_ptb_IU_script_v2.py",
        kind="MPI dispatcher",
        description=(
            "Builds all (perturbation, RDM) work-item pairs (100 "
            "perturbations × 200 RDMs, with an offset argument) and, per "
            "pair, runs `SedentoValleySimulation` on a perturbed decision-"
            "variable file "
            "(`objectives_dvs/dvs_reeval_perturbed/dvs_perturbations_<mode>_s<sol>.csv`), "
            "writing results to "
            "`full_reeval_perturbations_<mode>/sol<sol>_rdm<rdm>/`. Takes "
            "CLI args `mode solution_number ptb_offset`."
        ),
    ),
    dict(
        name="full_reeval_w_ptb_base.sh",
        kind="SLURM launcher",
        description=(
            "Same as `full_reeval_w_ptb_IU.sh` but for the base solution "
            "set: runs `full_reeval_w_ptb_base_script_v2.py 'base' 29 400` "
            "— i.e., perturbations of base solution #29."
        ),
    ),
    dict(
        name="full_reeval_w_ptb_base_script_v2.py",
        kind="MPI dispatcher",
        description=(
            "Functionally identical script to the IU v2 dispatcher (same "
            "code, same `rof_tables_reeval_base` table path), driven with "
            "`mode='base'`."
        ),
    ),
]

render_method_step(
    page_heading="Step 5: Perform IU Re-Evaluation",
    intro=(
        "This step asks a different question from Step 4: not 'how good "
        "is a strategy,' but 'how much worse does it get when its planned "
        "actions are implemented imperfectly?' Selected high-performing "
        "base and IU solutions have their decision variables perturbed "
        "(hundreds of perturbed instances each) and are re-simulated "
        "across the full RDM ensemble, producing the data behind the "
        "paper's performance-degradation, infrastructure-timing, and "
        "sensitivity-analysis figures."
    ),
    folder_relpath="scripts/5-IU Reevaluation",
    scripts=SCRIPTS,
    about_text=(
        "The perturbed-solution re-evaluations produced here feed Figure 3 "
        "(degradation), Figure 6 (infrastructure timing), and Figure 7 "
        "(sensitivity analysis) in Step 6. See "
        "`scripts/5-IU Reevaluation` in the repository for the underlying "
        "code."
    ),
)
