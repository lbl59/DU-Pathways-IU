from __future__ import annotations

from method_step_explorer import render_method_step

HELPER_SCRIPTS = [
    dict(
        name="helper_custom_colormap.py",
        kind="Helper module",
        description=(
            "Defines `custom_cmap()`, which builds a 3-color "
            "(light → base → dark) `LinearSegmentedColormap` (optionally "
            "reversed) for use in other plotting scripts."
        ),
    ),
    dict(
        name="helper_functions_iu.py",
        kind="Helper module",
        description=(
            "Plotting helpers for decision-variable (DV) distributions: "
            "`plot_histogram`, `plot_kde`, `plot_cdf` (histogram/KDE/CDF of "
            "a DV column with optional highlighted solutions), plus "
            "`find_sols()` for selecting solutions matching cooperation-"
            "behavior criteria (e.g. 'high_coop'/'low_coop' based on "
            "infrastructure/transfer-trigger DV thresholds)."
        ),
    ),
    dict(
        name="helper_functions_objs.py",
        kind="Helper module",
        description=(
            "Objective-focused variant of `helper_functions_iu.py`: similar "
            "`plot_histogram`/`plot_kde` functions (using a normalized "
            "`statsmodels` KDE instead of seaborn) for visualizing decision-"
            "variable or objective distributions."
        ),
    ),
    dict(
        name="helper_functions_robustness.py",
        kind="Helper module",
        description=(
            "Core robustness computation and plotting: "
            "`find_regional_minimax()` (aggregates per-utility objectives "
            "into regional worst-case values), `convert_to_df()`, "
            "`calc_robustness()` (fraction of RDMs where a solution meets "
            "reliability/restriction-frequency/worst-case-cost thresholds), "
            "and `plot_robustness_bar()`."
        ),
    ),
    dict(
        name="helper_parallel_plot_functions.py",
        kind="Helper module",
        description=(
            "Parallel-coordinates plotting utilities: `reorganize_objs()` "
            "normalizes/orients objective columns for a parallel-axis plot "
            "(per-axis min/max, ideal direction, min/max sense) ahead of "
            "rendering with `pandas.plotting.parallel_coordinates` or a "
            "custom variant."
        ),
    ),
    dict(
        name="helper_pathways_processing_functions.py",
        kind="Helper module",
        description=(
            "Infrastructure 'pathways' data processing: defines an "
            "`infra_dict` mapping infrastructure-option IDs to names/colors "
            "and per-utility infrastructure lists, plus `get_infra_byutil()` "
            "which reads `Pathways_s<sol>_RDM<rdm>.out` files to extract "
            "first-build weeks per infrastructure option across RDMs."
        ),
    ),
    dict(
        name="helper_plot_pathways_functions.py",
        kind="Helper module",
        description=(
            "Infrastructure pathway clustering/plotting, adapted from Gold "
            "et al. 2022 'Power and Pathways': `calc_num_clusters()` "
            "(silhouette-score-based k-means cluster count selection) and "
            "`cluster_pathways()` (reads a solution's `Pathways_s<sol>.out` "
            "file and clusters realizations by infrastructure-build "
            "timing)."
        ),
    ),
    dict(
        name="helper_quantify_perturbations.py",
        kind="Helper module",
        description=(
            "Degradation-quantification logic for the perturbation-"
            "sensitivity analysis: `calc_freq_degradation()` compares an "
            "original solution's objectives to its perturbed-instance "
            "objectives, computing the frequency of degradation and "
            "(weighted/unweighted) percent degradation per objective, "
            "normalized by each objective's observed range. Also uses "
            "`SALib.analyze.delta` for delta-moment sensitivity indices."
        ),
    ),
]

DRIVER_SCRIPTS = [
    dict(
        name="plot_results_fig1_objs_parallel.py",
        kind="Figure driver",
        description=(
            "Generates a parallel-coordinates figure of the DU-optimization "
            "objective tradeoffs (regional, `avg`/`p90` mode configurable), "
            "reading `objectives_<mode>_<mode2>_nd.csv` from "
            "`results/DU Optimization/` and saving to "
            "`figures/parallel_refset_<mode>_<mode>_regional.pdf`."
        ),
    ),
    dict(
        name="plot_results_fig1_objs_scatter.py",
        kind="Figure driver",
        description=(
            "Builds a 2-color-gradient scatterplot (restriction frequency "
            "as color, peak financial cost as marker size) comparing two "
            "objective sets (e.g. base vs. IU) per utility, via a local "
            "`two_color_cmap()` helper and `plot_scatter()`."
        ),
    ),
    dict(
        name="plot_results_fig2_robustness.py",
        kind="Figure driver",
        description=(
            "Reads precomputed robustness CSVs "
            "(`results/DU Reevaluation/robustness_sim_<mode>_refset_{IU,base}.csv`) "
            "and plots per-utility robustness-rank bar charts comparing "
            "base vs. IU solution sets, saved to "
            "`figures/robustness_<mode>_conditions.pdf`."
        ),
    ),
    dict(
        name="plot_results_fig3_degradation.py",
        kind="Figure driver",
        description=(
            "Loads original (non-perturbed) IU and base objective sets from "
            "`results/DU Optimization/`, combines them with "
            "`helper_quantify_perturbations`, and plots degradation-"
            "frequency histograms and a robustness-degradation heatmap "
            "(`figures/freq_degradation_histograms_pct.pdf`, "
            "`figures/robustness_degradation_histograms.pdf`)."
        ),
    ),
    dict(
        name="plot_results_fig4_dvs.py",
        kind="Figure driver",
        description=(
            "Plots decision-variable distributions (trigger and allocation "
            "DVs) comparing base vs. IU truncated non-dominated solution "
            "sets "
            "(`results/DU Optimization/dvs_{base,IU}_nd_truncated_extremes.csv`), "
            "output to `figures/dvs_IU_base_hist_triggersnd.pdf`."
        ),
    ),
    dict(
        name="plot_results_fig5_degradation.py",
        kind="Figure driver",
        description=(
            "Plots perturbation degradation statistics for two selected "
            "solutions (base #29, IU #401) from "
            "`results/IU Reevaluation/perturbations_{IU,base}/`, output to "
            "`figures/perturbations_allsols_3dscatter_p90.pdf`."
        ),
    ),
    dict(
        name="plot_results_fig5_parallel.py",
        kind="Figure driver",
        description=(
            "Parallel-coordinates comparison of base vs. IU objective "
            "tradeoffs for a chosen utility, highlighting two specific "
            "'social planner' solutions (IU #401, base #29), saved to "
            "`figures/parallel_objs_IUbase_<util>_p90.pdf`."
        ),
    ),
    dict(
        name="plot_results_fig5_robustness.py",
        kind="Figure driver",
        description=(
            "3D scatter plot of robustness (Watertown/Dryville/Fallsland "
            "axes) for all base and IU solutions, highlighting selected "
            "base/IU solutions, saved to "
            "`figures/robustness_3Dscatter_base_IU_p90.pdf`."
        ),
    ),
    dict(
        name="plot_results_fig6_fig7_matchstick.py",
        kind="Figure driver",
        description=(
            "'Matchstick'-style plot of percent-change in objectives due to "
            "the worst-case perturbation instance for a chosen solution "
            "(default IU #401), reading "
            "`perturbations_<mode>/percent_degradation/sol<sol>_sim_p90_weighted.csv`, "
            "output to "
            "`figures/percentchange_objs_enoki_sol<sol>_ptb<n>.pdf`."
        ),
    ),
    dict(
        name="plot_results_fig6_fig7_pathways.py",
        kind="Figure driver",
        description=(
            "Plots clustered infrastructure-development pathways (using "
            "`helper_plot_pathways_functions`) for a selected solution/RDM "
            "set, with hardcoded utility infrastructure-option labels for "
            "Watertown, Dryville, and Fallsland."
        ),
    ),
    dict(
        name="plot_results_fig8_sensitivity_analysis.py",
        kind="Figure driver",
        description=(
            "Builds an 'owner bubble matrix' sensitivity-analysis figure "
            "showing which utility's decision variables most affect "
            "degradation of which other utility's objectives, for selected "
            "base/IU solutions, output to "
            "`results/sensitivity_analysis_<refset>_<mode>_sol_<sol>.png`."
        ),
    ),
]

EXPLORATORY_SCRIPTS = [
    dict(
        name="explore_robustness.ipynb",
        kind="Jupyter notebook",
        description=(
            "Exploratory notebook (companion to `explore_robustness.py`) "
            "that computes and plots solution robustness (parallel-"
            "coordinate plots, 3D scatter, bar charts) comparing 'base' vs. "
            "'IU' solution sets and highlighting specific high-cooperation/"
            "social-planner solutions. Contains commented-out robustness-"
            "calculation code plus several plotting cells that appear to be "
            "iterative drafts of the final figures."
        ),
    ),
    dict(
        name="explore_robustness.py",
        kind="Python script (early draft)",
        description=(
            "Script-form counterpart/setup cell of the notebook above: "
            "defines shared plotting constants (utility names, objective "
            "names, color palettes, solution counts) for `p90`-mode "
            "robustness exploration. Appears to be an early/incomplete "
            "extraction rather than a full standalone script."
        ),
    ),
]

SCRIPTS = HELPER_SCRIPTS + DRIVER_SCRIPTS + EXPLORATORY_SCRIPTS

render_method_step(
    page_heading="Step 6: Plot the Figures",
    intro=(
        "The final step turns all the raw optimization and re-evaluation "
        "output into the paper's figures. This folder splits into reusable "
        "**helper modules** (robustness calculations, DV/objective "
        "distribution plotting, pathway clustering, degradation "
        "quantification) and per-figure **driver scripts** that load "
        "results and call those helpers to produce each numbered figure — "
        "the same figures you can explore interactively under "
        "**Explore our results** below."
    ),
    folder_relpath="scripts/6-Figure Plotting",
    scripts=SCRIPTS,
    note=(
        "A few driver scripts use relative imports that don't match this "
        "flat folder layout — `plot_results_fig2_robustness.py` and "
        "`plot_results_fig4_dvs.py` use `from ..helper_functions_* import "
        "*`, `plot_results_fig5_degradation.py` uses "
        "`from ..quantify_perturbations import *`, and "
        "`plot_results_fig8_sensitivity_analysis.py` uses "
        "`from quantify_perturbations import *` (no such module exists — "
        "only `helper_quantify_perturbations.py` does). These scripts "
        "likely need their imports fixed before they'll run standalone."
    ),
    about_text=(
        "This step documents the plotting code behind every figure in the "
        "paper. To interact with the resulting figures themselves — "
        "hover, click, and read callouts explaining each panel — see "
        "**Explore our results** in the sidebar. See "
        "`scripts/6-Figure Plotting` in the repository for the underlying "
        "code."
    ),
)
