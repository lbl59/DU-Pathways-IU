from __future__ import annotations

from method_step_explorer import render_method_step

SCRIPTS = [
    dict(
        name="full_optimization_loop_base.sh",
        kind="SLURM launcher",
        description=(
            "Submits 5 SLURM jobs (seeds 1-5, one `sbatch` per seed via a "
            "heredoc loop), each using 32 nodes × 64 tasks/node × 4 "
            "cpus/task (2048 MPI ranks), running `SedentoValleySimulation` "
            "for the 'base' (non-IU) action set: `-r 200` realizations, "
            "`-C -1` (full simulation/optimization mode), Borg parameters "
            "`-b true -n 200000 -o 2000 -i 4` (NFE, output frequency, "
            "number of islands), writing to `output_raw_base_fullExp/` and "
            "`rof_tables_opt_base/`."
        ),
    ),
    dict(
        name="full_optimization_loop_IU.sh",
        kind="SLURM launcher",
        description=(
            "Same as `full_optimization_loop_base.sh` but for the 'IU' "
            "(inter-utility / cooperative-action) formulation, adding an "
            "`-A TestFiles/rdm_actions_test_problem_opt_bs200.csv` actions "
            "file and writing to `output_raw_IU_fullExp/` / "
            "`rof_tables_opt_IU/`."
        ),
    ),
    dict(
        name="full_optimization_oneseed.sh",
        kind="SLURM launcher",
        description=(
            "Single-seed, small/debug-scale SLURM run (4 nodes × 64 tasks, "
            "4 cpus/task, debug QOS) of the same optimization "
            "(`-n 10000 -o 1000 -e 1 -i 4`), used for quickly testing the "
            "'base' (IU-actions) configuration before launching the full "
            "multi-seed jobs."
        ),
    ),
    dict(
        name="objectives_avg.cpp",
        kind="C++ source (WaterPaths)",
        description=(
            "Implements the 'average-case' (expected-value) formulation of "
            "the WaterPaths objective functions — reliability, restriction "
            "frequency, infrastructure NPC, peak financial cost, worst-case "
            "cost — computing each as a mean across hydrologic "
            "realizations. Part of the WaterPaths `ObjectivesCalculator` "
            "class; compiled into the `SedentoValleySimulation` executable "
            "rather than run directly."
        ),
    ),
    dict(
        name="objectives_p10.cpp",
        kind="C++ source (WaterPaths)",
        description=(
            "Near-identical to `objectives_avg.cpp` but implementing the "
            "'worst-case' / robust formulation: instead of averaging across "
            "realizations, each objective is computed from the 90th-"
            "percentile (worst decile — hence 'p10') value across sorted "
            "per-realization results, and reliability uses the maximum-"
            "failure-year count rather than an average. Together with "
            "`objectives_avg.cpp`, these two files represent alternate "
            "objective-formulation builds compiled into different "
            "optimization runs (average vs. robust/percentile-based "
            "objectives)."
        ),
    ),
]

render_method_step(
    page_heading="Step 3: Perform DU Optimization",
    intro=(
        "This is where the many-objective search happens: the Borg MOEA "
        "explores candidate pathway strategies for the Sedento Valley "
        "utilities, using the WaterPaths `SedentoValleySimulation` "
        "executable (pre-computed ROF tables from Step 2) to evaluate each "
        "candidate's performance. Two parallel optimization runs are "
        "launched — a **Baseline DU Optimization** that only searches "
        "using the expected future, and an **IU-DU Optimization** that "
        "also searches using the worst 10th-percentile of simulated "
        "futures — each run as 5 independent seeds across thousands of MPI "
        "ranks on an HPC cluster."
    ),
    folder_relpath="scripts/3-DU Optimization",
    scripts=SCRIPTS,
    note=(
        "The two `.cpp` files aren't scripts you run yourself — they're "
        "WaterPaths source files that get compiled into the "
        "`SedentoValleySimulation` executable invoked by the `.sh` "
        "launchers above (and by the ROF/Reevaluation scripts in other "
        "steps)."
    ),
    about_text=(
        "The output of this step is the raw, seed-by-seed Pareto front "
        "later merged and re-evaluated in Steps 4-5, and visualized as "
        "Figure 1 in Step 6. See `scripts/3-DU Optimization` in the "
        "repository for the underlying code."
    ),
)
