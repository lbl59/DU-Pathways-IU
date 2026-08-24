from __future__ import annotations

from method_step_explorer import render_method_step

SCRIPTS = [
    dict(
        name="genROFTables_opt.sh",
        kind="SLURM launcher",
        description=(
            "SLURM/debug-QOS script (1 node, 30 min) that runs "
            "`./SedentoValleySimulation` with `-T 256` threads, `-r 200` "
            "realizations, mode `-m 0` (ROF table generation), against "
            "`sample_solutions.csv`, writing to "
            "`rof_tables_opt_IU_smallExp/` using the bootstrap-200 RDM "
            "test-file set "
            "(`rdm_utilities/dmp/water_sources/actions_test_problem_opt_bs200.csv`)."
        ),
    ),
    dict(
        name="genROFTables_reeval.sh",
        kind="SLURM launcher",
        description=(
            "SLURM script (4 nodes × 50 tasks, 4 cpus/task, 2h) that "
            "launches `genROFTables_reeval_script.py` via `srun -n 200 -c 4`."
        ),
    ),
    dict(
        name="genROFTables_reeval_script.py",
        kind="MPI dispatcher",
        description=(
            "MPI (mpi4py) driver that splits 200 RDMs across ranks and, per "
            "RDM, calls `SedentoValleySimulation` in ROF-table mode "
            "(`-m 0`) against a fixed decision-variable set "
            "(`objectives_dvs/dvs_base_shaved_56.csv`), writing per-RDM "
            "tables to `rof_tables_reeval_new/rdm_<n>/` using the "
            "reevaluation RDM test-file set."
        ),
    ),
]

render_method_step(
    page_heading="Step 2: Generate ROF Tables",
    intro=(
        "Risk-of-failure (ROF) is the trigger metric that drives every "
        "utility's restriction, transfer, and infrastructure decisions "
        "inside the WaterPaths simulation — but computing it on the fly "
        "during optimization would be prohibitively slow. This step "
        "pre-computes lookup tables of ROF values across the synthetic "
        "streamflow/demand ensemble, once for the optimization sample and "
        "once for the larger reevaluation sample, so the simulator can "
        "look up ROF values instead of recalculating them at every "
        "timestep."
    ),
    folder_relpath="scripts/2-ROF Table Generation",
    scripts=SCRIPTS,
    about_text=(
        "The ROF tables generated here are consumed by the "
        "`SedentoValleySimulation` WaterPaths executable during both the DU "
        "Optimization (Step 3) and every re-evaluation step (Steps 4-5). "
        "See `scripts/2-ROF Table Generation` in the repository for the "
        "underlying code."
    ),
)
