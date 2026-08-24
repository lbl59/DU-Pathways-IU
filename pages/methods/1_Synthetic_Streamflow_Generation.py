from __future__ import annotations

from method_step_explorer import render_method_step

SCRIPTS = [
    dict(
        name="1_gen_annual_historical_demands.py",
        kind="Python script",
        description=(
            "Builds annual demand projections (in MGD) for each of six "
            "utilities (OWASA, Durham, Raleigh, Cary, Pittsboro, Chatham) by "
            "linearly interpolating multi-year utility planning-report "
            "projections (hardcoded arrays in the script) out to a full "
            "annual series, writing results to "
            "`historical/demands/annual_demand_projections/`."
        ),
    ),
    dict(
        name="1_run_gen_annual_historical_demands.sh",
        kind="SLURM launcher",
        description=(
            "SLURM batch script (1 node/1 task, 24h) that simply runs "
            "`1_gen_annual_historical_demands.py`."
        ),
    ),
    dict(
        name="2_gen_annual_pwl_syn_demands.py",
        kind="Python script",
        description=(
            "CLI script (`<num_rdm> <output_dir>`) that generates "
            "piecewise-linear (4-period) stochastic variants of the annual "
            "demand projections for each RDM/SOW, by applying per-period "
            "growth-rate multipliers (loaded from "
            "`rdm_demand_pwl_period{1-4}_200_with_header.csv`) to the "
            "historical projections."
        ),
    ),
    dict(
        name="2_run_gen_annual_pwl_syn_demands.sh",
        kind="Misnamed file (contains Python)",
        description=(
            "Despite the `.sh` extension, this file's contents are Python "
            "— a near-duplicate of `2_gen_annual_pwl_syn_demands.py` — and "
            "appears to be a copy/misnamed file rather than a real shell "
            "driver."
        ),
    ),
    dict(
        name="3_gen_syn_inflow_evap.py",
        kind="Python script",
        description=(
            "The core synthetic streamflow/evaporation generator. For a "
            "given RDM row, it bootstraps historical weekly inflow/"
            "evaporation series (log-space, Cholesky-correlated, seasonally "
            "shifted) and applies a sinusoidal mean-adjustment "
            "(`mu_sinusoid`, parameterized by RDM amplitude/period/phase) to "
            "produce multiple realizations per SOW. CLI args: "
            "`rdm_to_run reals_per_rdm num_syn_years output_dir hist_dir`."
        ),
    ),
    dict(
        name="3_run_gen_syn_inflow_evap.sh",
        kind="SLURM launcher",
        description=(
            "SLURM script (2 nodes × 20 tasks/node, 24h) that runs "
            "`3_submit_gen_syn_inflow_evap.py` via `mpirun -np 40`."
        ),
    ),
    dict(
        name="3_submit_gen_syn_inflow_evap.py",
        kind="MPI dispatcher",
        description=(
            "Splits 200 RDMs across 40 MPI ranks (mpi4py, 5 RDMs/rank) and "
            "shells out to `3_gen_syn_inflow_evap.py` for each, with "
            "`N_REALIZATIONS=200`, `N_YEARS=48`."
        ),
    ),
    dict(
        name="4_combine_hist_syn_inflows_evap.py",
        kind="Python script",
        description=(
            "CLI script (`rdm_to_run output_dir hist_dir mode[csv|parquet]`) "
            "that stitches the last 50 years of historical inflow/"
            "evaporation onto each RDM's synthetic series (inserting "
            "specific historical 'anchor' weeks), and derives OWASA "
            "sub-source inflows (Cane Creek, University Lake, Stone Quarry, "
            "via fixed scaling factors) and combined Durham inflow. Writes "
            "CSV or Parquet (zstd-compressed) output."
        ),
    ),
    dict(
        name="4_run_combine_hist_syn_inflows_evap.sh",
        kind="SLURM launcher",
        description=(
            "SLURM script (2 nodes × 20 tasks/node, 24h) that runs "
            "`4_submit_combine_hist_syn_inflows_evap.py` via "
            "`mpirun -np 40`."
        ),
    ),
    dict(
        name="4_submit_combine_hist_syn_inflows_evap.py",
        kind="MPI dispatcher",
        description=(
            "Splits 200 RDMs across 40 ranks and calls "
            "`4_combine_hist_syn_inflows_evap.py` per RDM in `parquet` mode "
            "with `N_YEARS=200`."
        ),
    ),
    dict(
        name="5_condition_build_demands.py",
        kind="Python script",
        description=(
            "The largest and most complex script in this step. It builds "
            "historical inflow-demand joint PDFs/CDFs per utility "
            "(irrigation vs. non-irrigation weeks), applies those historical "
            "distributions to synthetic inflows to generate synthetic "
            "weekly demand variation, and finally combines that variation "
            "with the RDM's piecewise-linear annual demand projections to "
            "produce full synthetic weekly demand time series per utility "
            "(written as Parquet, zstd level 22). CLI args: "
            "`rdm_to_run syn_dir hist_dir write_data delete_syn mode`."
        ),
    ),
    dict(
        name="5_run_condition_build_demands.sh",
        kind="SLURM launcher",
        description=(
            "SLURM script (2 nodes × 20 tasks/node, 24h) that runs "
            "`5_submit_condition_build_demands.py` via `mpirun -np 40`."
        ),
    ),
    dict(
        name="5_submit_condition_build_demands.py",
        kind="MPI dispatcher",
        description=(
            "Splits 200 RDMs across 40 ranks and calls "
            "`5_condition_build_demands.py` per RDM "
            "(`WRITE_DATA=1`, `DELETE_DATA=0`, `MODE='parquet'`)."
        ),
    ),
    dict(
        name="compare_parquet_csv.py",
        kind="Validation script",
        description=(
            "Standalone validation script that loads a matching CSV/Parquet "
            "pair (hardcoded to `synthetic/rdm_0/demands/Chatham_demands`) "
            "and checks numeric equality within `1e-6` tolerance, printing "
            "the first differing value if any — used to sanity-check the "
            "CSV→Parquet output pipeline above."
        ),
    ),
]

render_method_step(
    page_heading="Step 1: Generate Synthetic Inputs",
    intro=(
        "With a sample of States of the World in hand, we generate the "
        "synthetic hydrology and demand ensembles that each SOW will be "
        "stress-tested against. This is a five-part pipeline: build "
        "historical annual demand baselines, perturb them into "
        "piecewise-linear growth trajectories per RDM, bootstrap synthetic "
        "weekly inflow/evaporation realizations, splice historical anchor "
        "years back in, and finally condition synthetic weekly demand "
        "variation on the synthetic inflows using historical inflow-demand "
        "relationships. Each numbered stage (1–5) has a driver script and, "
        "for the larger stages, an MPI dispatcher that parallelizes the "
        "work across all 200 RDMs on an HPC cluster."
    ),
    folder_relpath="scripts/1-Synthetic Streamflow Generation",
    scripts=SCRIPTS,
    note=(
        "This folder also contains a `historical/` subfolder holding the "
        "historical input data organized into `demands/`, `evaporation/`, "
        "`inflow_demand_distributions/`, `inflows/`, and `log_inflows/` "
        "subdirectories — these are the raw inputs (and intermediate "
        "outputs) that the scripts below read from and write to."
    ),
    about_text=(
        "This step turns the sampled DU SOWs from Step 0 into the actual "
        "streamflow, evaporation, and demand time series that the "
        "WaterPaths simulation consumes. See "
        "`scripts/1-Synthetic Streamflow Generation` in the repository for "
        "the underlying code."
    ),
)
