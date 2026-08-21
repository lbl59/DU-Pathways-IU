import numpy as np
import pandas as pd
import sys, os
import matplotlib.pyplot as plt

from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.cm import ScalarMappable

# user can modify these values to select which solutions to plot 
# and where to store the output figure
sol_num = 29
action_mode = 'base'  # change to 'IU' for IU social planner solution
util_to_plot = 'watertown'  # change to 'dryville' or 'fallsland' for other utilities
compsol_type = 'SP base'
output_figure_filepath = f'figures/pathways_boxplot_likelihood_freq_s{sol_num}_{util_to_plot[0]}.pdf'

# set up plotting parameters
num_sol_dict = {'base': 46, 'IU': 628}
color_dict_coop = {'SP base': "#39563D", 'SP IU': "#B66D0D"}
color_selected = color_dict_coop[compsol_type]

num_reals = 200
num_perturbations = 500 

infra_names = {
    'watertown': ['New River\nReservoir', 'College Rock\nExp. Low',
                    'College Rock\nExp. High', 'Water\nReuse', 'Water\nReuse II'],
    'dryville': ['Sugar Creek\nReservoir', 'Water\nReuse'],
    'fallsland': ['New River\nReservoir', 'Water\nReuse']
}

# take mode, solution number, and utility as arguments
figsize_dict = {'watertown': (4, 4), 'dryville': (4, 2), 'fallsland': (4, 2)}
figsize = figsize_dict[util_to_plot]
color = color_dict_coop[compsol_type]

original_file = f'../../results/IU Reevaluation/Pathways_s{sol_num}_original.out'

# check if the file exists
try: 
    with open(original_file, 'r') as f:
        pass
except FileNotFoundError:
    print(f"Error: The file {original_file} does not exist.")
    sys.exit(1)

perturbed_dir = f'../../results/IU Reevalaution/perturbed_pathways_{action_mode}/pathways_ptb_s{sol_num}'
# check if the directory exists
if os.path.isdir(perturbed_dir):
    pass
else:
    print(f"Error: The directory {perturbed_dir} does not exist.")

plt.rcParams.update({
    'font.size': 10,
    'font.family': 'sans-serif',
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 9,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
})

def load_pathway_data(filepath, num_reals=200):
    # Load pathway data
    try:
        df = pd.read_csv(filepath, sep='\t')
        return df
    except Exception as e:
        print(f'Error reading {filepath}: {e}')
        return None

def extract_timing_by_utility(pathways_df, utility_name, num_reals=200):
    # Extract infrastructure timing for a specific utility.
    cluster_input = np.ones([num_reals, 13]) * 2344
    
    for real in range(num_reals):
        # not all realizations have all infrastructure        
        current_real = pathways_df[pathways_df['Realization'] == real]
        for inf in [3, 4, 5, 7, 8, 9, 10, 11, 12]:
            if not current_real.empty:
                for index, row in current_real.iterrows():
                    if row['infra.'] == inf:
                        cluster_input[real, inf] = row['week']
    
    cluster_input = cluster_input[:, [4, 5, 7, 8, 9, 10, 11, 12]]
    
    if utility_name == 'watertown':
        return cluster_input[:, [0, 2, 3, 4, 5]]
    elif utility_name == 'dryville':
        return cluster_input[:, [1, 6]]
    else:
        return cluster_input[:, [0, 7]]

def calculate_construction_frequency(pathway_data, max_time=2344):
    # Calculate percentage of realizations that build each infrastructure.

    n_reals, n_infra = pathway_data.shape
    frequencies = np.zeros(n_infra)
    
    for i in range(n_infra):
        # Count how many realizations build this infrastructure
        built = np.sum(pathway_data[:, i] < max_time)
        frequencies[i] = (built / n_reals) * 100.0
    
    return frequencies

def calculate_frequency_changes(original_data, perturbed_data_list, max_time=2344):
    # Calculate how construction frequency changes across perturbations.
    
    n_infrastructure = original_data.shape[1]
    n_perturbations = len(perturbed_data_list)
    
    # Original construction frequencies
    original_freq = calculate_construction_frequency(original_data, max_time)
    
    # Calculate frequency for each perturbation
    all_changes = np.zeros((n_perturbations, n_infrastructure))
    
    for p_idx, pert_data in enumerate(perturbed_data_list):
        pert_freq = calculate_construction_frequency(pert_data, max_time)
        # Calculate signed change (positive = more frequent, negative = less frequent)
        all_changes[p_idx, :] = pert_freq - original_freq
    
    # Calculate statistics
    max_increase = np.max(all_changes, axis=0)
    max_decrease = np.min(all_changes, axis=0)
    mean_change = np.mean(all_changes, axis=0)
    
    return max_increase, max_decrease, mean_change, all_changes, original_freq

def calculate_frequency_changes(original_data, perturbed_data_list, max_time=2344):
    """
    Calculate how construction frequency changes across perturbations.
    
    Returns
    -------
    max_increase : np.ndarray
        Maximum increase in construction frequency for each infrastructure
    max_decrease : np.ndarray
        Maximum decrease in construction frequency for each infrastructure
    mean_change : np.ndarray
        Mean change in construction frequency (preserves sign)
    all_changes : np.ndarray
        All frequency changes (n_perturbations, n_infrastructure)
    """
    n_infrastructure = original_data.shape[1]
    n_perturbations = len(perturbed_data_list)
    
    # Original construction frequencies
    original_freq = calculate_construction_frequency(original_data, max_time)
    
    # Calculate frequency for each perturbation
    all_changes = np.zeros((n_perturbations, n_infrastructure))
    
    for p_idx, pert_data in enumerate(perturbed_data_list):
        pert_freq = calculate_construction_frequency(pert_data, max_time)
        # Calculate signed change (positive = more frequent, negative = less frequent)
        all_changes[p_idx, :] = pert_freq - original_freq
    
    # Calculate statistics
    max_increase = np.max(all_changes, axis=0)
    max_decrease = np.min(all_changes, axis=0)
    mean_change = np.mean(all_changes, axis=0)
    
    return max_increase, max_decrease, mean_change, all_changes, original_freq

def create_frequency_colored_boxplot(original_data, perturbed_data_list,
                                     infra_names,
                                     figsize=(12, 9),
                                     overlap=0.5,
                                     fill_alpha=0.8,
                                     show_quartiles=False,
                                     show_original=True,
                                     bar_color='black',
                                     save_path=None):
    # Create box plot with colors based on construction frequency change.  
    n_infrastructure = original_data.shape[1]
    n_perturbations = len(perturbed_data_list)
    
    print(f"\n{'='*70}")
    print(f"Analyzing Construction Frequency Changes (Boxplot)")
    print(f"{'='*70}")
    
    # Data is in weeks, will be displayed in years on x-axis
    # Time range is fixed to 20-50 years.
    original_scaled = original_data.copy()
    perturbed_scaled = perturbed_data_list
    max_time = 2344  # Maximum time in weeks
    xlabel = 'Median Construction\nTime (years)'
    
    # Calculate frequency changes (always use original week-based data)
    max_increase, max_decrease, mean_change, all_changes, original_freq = \
        calculate_frequency_changes(original_data, perturbed_data_list, max_time=2344)
    
    # Collect median timing values across perturbations (not all individual values)
    all_perturbation_medians = []
    for i_idx in range(n_infrastructure):
        medians_across_perturbations = []
        for pert_data in perturbed_scaled:
            valid_data = pert_data[:, i_idx][pert_data[:, i_idx] < max_time]
            if len(valid_data) > 0:
                medians_across_perturbations.append(np.median(valid_data))
        all_perturbation_medians.append(medians_across_perturbations)
    
    # Calculate original medians
    original_medians = np.zeros(n_infrastructure)
    for i_idx in range(n_infrastructure):
        valid_data = original_scaled[:, i_idx][original_scaled[:, i_idx] < max_time]
        if len(valid_data) > 0:
            original_medians[i_idx] = np.median(valid_data)
        else:
            original_medians[i_idx] = np.nan
    
    # Calculate original and perturbed frequencies 
    # Original construction frequencies (number of realizations that build)
    original_freq_count = np.zeros(n_infrastructure)
    for i in range(n_infrastructure):
        freq_built_inf = (np.sum(original_data[:, i] < max_time)/original_data.shape[0])*100.0
        original_freq_count[i] = freq_built_inf
    
    # Median construction frequencies across perturbations (number of realizations)
    perturbed_freq_median = np.zeros(n_infrastructure)
    for i in range(n_infrastructure):
        freq_per_pert = []
        for pert_data in perturbed_data_list:
            # count number of rows where realization value is > 0
            freq_built_inf = (np.sum(pert_data[:, i] < max_time)/pert_data.shape[0])*100.0
            freq_per_pert.append(freq_built_inf)
        perturbed_freq_median[i] = np.median(freq_per_pert)
    

    # Set up diverging colormap centered at 0 to show direction of change
    # Blue = decreased frequency, Red = increased frequency
    max_abs_change = max(abs(np.min(max_decrease)), abs(np.max(max_increase)), 10)
    norm = Normalize(vmin=-25, vmax=25)
    
    # Create figure with two subplots (main boxplot + frequency bar plot)
    from matplotlib.gridspec import GridSpec
    fig = plt.figure(figsize=figsize)
    gs = fig.add_gridspec(1, 2, width_ratios=[4, 1], wspace=0.1)
    
    # Main plot axis
    ax = fig.add_subplot(gs[0])
    
    # Calculate vertical spacing
    # For boxplots, simply use integer positions 0, 1, 2...
    y_positions = np.arange(n_infrastructure)
    
    # Plot each infrastructure with color based on frequency change
    for i, infra_name in enumerate(infra_names):
        y_pos = y_positions[i]
        
        # Get color based on max frequency change (preserves direction)
        # Use whichever has larger absolute value: max_increase or max_decrease
        if abs(max_increase[i]) >= abs(max_decrease[i]):
            freq_change = max_increase[i]
        else:
            freq_change = max_decrease[i]
        
        # Get median timing values for this infrastructure across all perturbations
        perturbation_medians = all_perturbation_medians[i]
        
        if len(perturbation_medians) < 10:  # needs at least some data to show a boxplot
            print(f"\nWarning: Not enough data for {infra_name}")
            # Plot a marker for original if available
            if not np.isnan(original_medians[i]):
                 # Original pathway median (White circle)
                ax.plot(original_medians[i], y_pos, 'o', markeredgewidth=1.5,
                        markeredgecolor='black', markerfacecolor='white',
                        markersize=8, zorder=100)
            continue
        else:
            # Create Box Plot with median values across perturbations
            # vert=False for horizontal boxplots
            box_width = 0.5
            bp = ax.boxplot(perturbation_medians, positions=[y_pos], vert=False, 
                            widths=box_width, patch_artist=True,
                            showfliers=False) # Hide outliers primarily for cleaner look, or verify if needed
            
            # Style the box
            for patch in bp['boxes']:
                patch.set_facecolor(bar_color)
                patch.set_alpha(fill_alpha)
                patch.set_edgecolor('black')
            
            for element in ['whiskers', 'caps', 'medians']:
                plt.setp(bp[element], color='black', linewidth=1.5)
                
            # Original pathway median (White circle)
            if show_original and not np.isnan(original_medians[i]):
                orig_median = original_medians[i]
                
                # Add dot at y_pos (centered on box)
                ax.plot(orig_median, y_pos, 'o', markeredgewidth=1.5,
                    markeredgecolor='black', markerfacecolor='white',
                    markersize=8, zorder=i+301, label='Original median' if i==0 else "")

            # Median of medians across all perturbations (Colored dot matching bar plot)
            median_of_medians = np.median(perturbation_medians)
            if not np.isnan(median_of_medians):
                ax.plot(median_of_medians, y_pos, 'o',
                        color=bar_color, markeredgewidth=1.5,
                        markeredgecolor='black', markersize=8, zorder=i+301, 
                        label='Median of perturbations' if i==0 else "")
            
            # Add infrastructure label with frequency change - centered at box middle
            sign = '+' if freq_change >= 0 else ''
            label_text = f"{infra_name}\n({sign}{freq_change:.0f}% built)"
            ax.text(20*52, y_pos, label_text,
                ha='right', va='center', fontsize=9)

    # Formatting main axis
    ax.set_xlabel(xlabel, fontsize=9)
    
    # Set x-axis limits to 20-50 years (in weeks: 1040-2600)
    ax.set_xlim(20*52, 50*52)
    ax.set_xticks(np.arange(20, 51, 5) * 52)  # Ticks every 5 years in weeks
    ax.set_xticklabels(np.arange(20, 51, 5))

    # Adjust Y-limits to fit boxes
    ax.set_ylim(-0.6, y_positions[-1] + 0.6)
    ax.set_yticks([])
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    # Grid with solid lines to match gradient style
    ax.grid(axis='x', alpha=0.3, linestyle='-', linewidth=0.8, color='gray')
    
    # Right panel: Construction frequency bar plot
    ax_bar = fig.add_subplot(gs[1])
    
    # Horizontal bar plot for median perturbed frequencies
    y_pos = y_positions  # Use the same y_positions as the Box plots for alignment
    
    # Horizontal bar plot for median perturbed frequencies
    # make the bars thinner
    ax_bar.barh(y_pos, perturbed_freq_median, height=0.5,
                    color=bar_color, alpha=0.85, edgecolor='black', 
                    linewidth=1.0, label='Med. across perturbations')

    # scatter plot for median perturbed frequencies
    ax_bar.scatter(original_freq_count, y_pos, color='white', s=60, 
                   alpha=0.65,
                   marker='o', edgecolors='black', linewidths=1.5,
                   label='Original freq.', zorder=10)

    # Format bar plot axis
    ax_bar.set_yticks(y_pos)
    ax_bar.set_yticklabels([])  # Remove labels since they're on the left
    ax_bar.set_xlabel('% realizations\nbuilt', fontsize=9)
    ax_bar.set_xlim(0, np.max([50.0, np.max(perturbed_freq_median)+5, np.max(original_freq_count)+5]))
    ax_bar.grid(axis='x', alpha=0.3, linestyle='--', linewidth=0.5)
    ax_bar.legend(loc='upper center', fontsize=8, frameon=False, 
                  bbox_to_anchor=(0.5, 1.29))

    # remove top and right spines
    ax_bar.spines['top'].set_visible(False)
    ax_bar.spines['right'].set_visible(False)

    ax.invert_yaxis()
    ax_bar.invert_yaxis()
    
    # Title
    title = (f'Infrastructure timing & construction frequency \n'
            f'achanges across 500 perturbations')
    ax.set_title(title, fontsize=9, pad=35)
    
    # Create colorbar axis at the bottom of the figure
    cax = plt.axes([0.1, -0.05, 0.8, 0.05])
        
    if save_path:
        plt.savefig(save_path,)
    print(f"\nFrequency-colored boxplot saved to: {save_path}")
    
    return fig, ax

# Load data
print(f"\nLoading original: {original_file}")
original_df = load_pathway_data(original_file)
original_data = extract_timing_by_utility(original_df, util_to_plot, num_reals)
infra_names = infra_names[util_to_plot]

print(f"Loading {num_perturbations} perturbations...")
perturbed_data_list = []
for i in range(num_perturbations):
    pert_path = f'Pathways_s{i}.out'
    pert_df = load_pathway_data(pert_path)
    if pert_df is not None:
        pert_data = extract_timing_by_utility(pert_df, util_to_plot, num_reals)
        perturbed_data_list.append(pert_data)

print(f"Successfully loaded {len(perturbed_data_list)} perturbations")

# plot only if there are infrastructure that was built
if len(perturbed_data_list) > 0:
    # Create frequency-colored ridgeline (weeks data, years axis labels)
    print("\n" + "="*70)
    print("Creating frequency-colored ridgeline...")
    print("="*70)
    fig, ax = create_frequency_colored_boxplot(
        original_data, perturbed_data_list, infra_names,
        bar_color=color_selected,
        overlap=0.3,
        figsize=figsize,
        save_path=output_figure_filepath
    )
    
    print("COMPLETE!")
    print(f"Figure saved in {output_figure_filepath}")

