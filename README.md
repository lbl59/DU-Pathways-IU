# Lau et al. (2026) Deeply Uncertain Pathways under Implementation Uncertainty (DU Pathways IU)

**Leveraging evolutionary multi-objective reinforcement learning search under implementation uncertainty to discover robust and actionable water supply investment pathways**

Lillian Lau<sup>1\*</sup>, Patrick M. Reed<sup>1</sup>,  and David F. Gold<sup>2</sup>

<sup>1 </sup>Cornell University, Ithaca, NY, USA.

<sup>2 </sup>Utrecht University, Utrecht, Netherlands.

\* corresponding author:  lbl59@cornell.edu

:sparkles: Explore our Interactive Repository here :sparkles:

## :mailbox: Contents
- [Abstract](#memo-abstract)
- [Journal Reference](#pencil2-journal-reference)
- [Data and Code Reference](#1234-data-and-code-reference)
- [Contributing Software](#computer-contributing-software)
- [Explore our Interactive Repo](#microscope-explore-our-interactive-repo)
- [Reproduce my experiment](#file_folder-reproduce-my-experiment)
- [Reproduce my figures](#bar_chart-reproduce-my-figures)

## :memo: Abstract
Regional cooperation in drought management actions and infrastructure investments among water utilities is a promising approach for improving the robustness of urban water systems facing evolving drought extremes, uncertain demands, and growing financial constraints. Theoretically, regional cooperation can improve resource efficiency by realizing economies of scale, add flexibility for achieving improved supply reliability, and, ideally, limiting individual and collective financial risks. However, prior work has shown that implementation uncertainty in risk-based drought management actions or infrastructure investments (i.e., modest deviations action triggers) can significantly exacerbate collaborating actors’ vulnerabilities and drive counterparty risk. To address this challenge, we contribute the Deeply Uncertain Pathways under Implementation Uncertainty (DU Pathways IU) framework, an evolutionary multi-objective reinforcement learning (eMORL) approach that directly accounts for human-driven implementation uncertainty when optimizing for robust regional cooperative water supply management and planning pathway strategies. This framework, demonstrated on the challenging, multi-city Sedento Valley benchmarking test case, enables the discovery of a larger, more diverse set of high-performing pathway strategies that more fully leverage the full suite of cooperative management and planning actions available to all regional actors. Additionally, this broader set of pathway strategies attain higher robustness across all regional actors while limiting supply reliability and financial performance degradation when exposed to implementation uncertainty. Further sensitivity analysis reveals that these highly cooperative pathway strategies also reduce counterparty risks driven by unintentional deviations in partner utilities’ actions. Consequently, this framework affords cooperating water utilities more control over their individual performance when assessing future infrastructure investments and the timing of their drought mitigation actions. Overall, this work is broadly applicable to water utility managers seeking high performing and robust pathway strategies that directly account for the operational tolerances of their cooperative actions and can remain stable in the face of implementation uncertainty.

[Back to contents](#mailbox-contents)

## :pencil2: Journal reference
To cite this paper, please use the following citation _(Note: This work is currently in-prep and does not yet have a formal citation)_

> Lau, L.B, Reed, P.M., and Gold, D.F. (2026). Leveraging evolutionary multi-objective reinforcement learning search under implementation uncertainty to discover robust and actionable water supply investment pathways. _In prep_.

[Back to contents](#mailbox-contents)

## :1234: Data and Code Reference

### Input data
Detailed information on generating the hydroclimatic realizations used in this experiment can be found in the [Synthetic Streamflow Generation folder here](scripts/Synthetic%20Streamflow%20Generation/).

### Output data
A subset of the output data containing the values needed to calculate time-varying performance, robustness, and generate infrastructure pathways can be found at this _this MSDLive repository_ [INSERT LINK HERE]. 
To cite the data, use the citation below:

> Lau, L., Reed, P. M., & Gold, D. F. (2026). DU Pathways IU Output Files (Version v1) [Data set]. MSD-LIVE Data Repository. [INSERT LINK HERE].

### Cite the code in this repository
To cite this repository, use the citation below:

> Lau, L. B., Reed, P. M., & Gold, D. F. (2026). Data and code for 'Leveraging evolutionary multi-objective reinforcement learning search under implementation uncertainty to discover robust and actionable water supply investment pathways.' [Computer software]. [_insert Zenodo link here_]

[Back to contents](#mailbox-contents)

## :computer: Contributing software
| Model | Version | Repository Link | DOI |
|-------|---------|-----------------|-----|
| Apache Arrow | v25.0.1 | https://github.com/apache/arrow | NA | 
| HDF5 for Python | v3.12.1 | https://github.com/h5py/h5py | NA |
| MOEAFramework | v5.1 | https://github.com/MOEAFramework/MOEAFramework | NA | 
| SALib | v1.5.2 | https://github.com/salib/salib | 10.18174/sesmo.18155 | 
| Seaborn | v0.13.2 | https://github.com/mwaskom/seaborn | 10.21105/joss.03021 |
| WaterPaths | v1.0 | https://github.com/bernardoct/WaterPaths | 10.1016/j.envsoft.2020.104772 |

[Back to contents](#mailbox-contents)

## :microscope: Explore our Interactive Repo
Explore our interactive Streamlit repository here [INSERT LINK HERE] to view and interact with our code, data, and figures! 

[Back to contents](#mailbox-contents)

## :file_folder: Reproduce my experiment
Clone this repository to get access to code scripts used to generate risk of failure (ROF) tables and generate the synthetic hydrologic traces, run the IU Optimization and Baseline Optimization experiments, as well as conduct both IU Re-Evaluation and DU Re-Evaluation. This repository also provides the Python code scripts for reproducing the figures. 

_:memo: NOTE: This repository only contains the scripts to run the experiment. For the actual CSV, Parquet, and HDF5 files used as input into the different steps, please see this paper's corresponding MSDLive data repository here [INSERT LINK HERE]._

Navigate into each folder (listed below) to refer to their detailed README files that provide step-by-step guidelines on how to navigate and execute their respective scripts.

### What each folder contains 
1. [`src`](src/): Contains the source code of the latest version of [WaterPaths](https://github.com/bernardoct/WaterPaths) used in this study.
2. [scripts`](scripts/): Contains all the code required to perform the optimization, re-evaluation, and figure generation of this study. Each subfolder is numbered in order of which it should be completed.
    1. [`scripts/0-Gen DU SOWs`](scripts/0-Gen%20DU%20SOWs/): Contains all the code required to generate the deeply uncertain (DU) factors and the implementation uncertainty ranges for the optimization and re-evaluation experiments.
    1. [`scripts/1-Synthetic Streamflow Generation`](scripts/1-Synthetic%20Streamflow%20Generation/): Contains all the code required to generate synthetic traces of inflow, evaporation, and demand from historical data.
    2. [`scripts/2-ROF Table Generation`](scripts/2-ROF%20Table%20Generation/): Contains all the code required to generate the Risk of Failure (ROF) tables needed to run the subsequent experiements. 
    3. [`scripts/3-DU Optimization`](scripts/3-DU%20Optimization/): Contains all code and guidelines required to perform two versions of the DU Optimization experiment. Two types of DU Optimization experiments were conducted for this study: the Baseline Optimization experiment (no implementation uncertainty), and the IU Optimization (with implementation uncertainty).
    4. [`scripts/4-DU Reevaluation`](scripts/4-DU%20Reevaluation/): Contains the code required to perform DU Re-Evaluation for calculating the robustness of each pathway strategy discovered in the DU Optimization step.
    5. [`scripts/5-DU Reevaluation`](scripts/5-IU%20Reevaluation/): Contains the code required to perform IU Re-Evaluation for quantifying performance degradation of each pathway strategy when exposed to implementation uncertainty.
    6. [`scripts/6-Figure Plotting`](scripts/6-Figure%20Plotting/): Contains the code required to generate most of the figures found in `figures`.
3. [`figures`](figures/): Contains all the figures that can be found in the paper.

### Prerequisites
1. Install the software components required to conduct the experiment from [contributing modeling software](#contributing-modeling-software)
2. Download and install the supporting [input data](#input-data) required to conduct the experiment
3. Follow the guidelines detailed in the README files of the `scripts` directory [here](scripts/README.md)

[Back to contents](#mailbox-contents)

## :bar_chart: Reproduce my figures
Use the files found in the `figures` directory to reproduce the figures used in this publication. Follow the guidelines detailed in the README file of the [`scripts/Figure Plotting`](scripts/Figure%20Plotting/) directory.

:microscope: You can also explore the figures interactively on [our Streamlit platform here].

**Note**: Please complete all the steps listed in the `scripts` folder prior to reproducing the figures.

[Back to contents](#mailbox-contents)