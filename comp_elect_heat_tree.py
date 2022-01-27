import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import itertools
import constants
import restructure_data

ELECT_INDEX = 0
HEAT_INDEX = 1

def main():
    """
    Generates plot of the buildings impacts cause by operations - distributed into electricity and heating.
    :return:
    """
    data = restructure_data.tree_structure('res/api_saved_res/output_case2_conf_gen2/case2_results_collected.json')

    indicator = 'GWP'
    res_dict = {}
    config_names = []

    for conf in data:
        # Store the name og the configuration to use in plots
        if conf not in config_names:
            config_names.append(conf)

        # Finding the information for the utilities
        building_data = restructure_data.find_building(data, conf)
        operation = restructure_data.find_one_child_of_type(building_data, 'Operation')
        utilities = restructure_data.find_children_of_type(operation, 'OperationUtilityInstance')

        # List containing electricity and heating - therefore always two elements
        res_dict[conf] = [None, None]
        for energy_type in utilities:
            if energy_type['operation_calc_type'] == 'Electricity':
                op_elect_id = energy_type['id']
                res = data[conf]['output']['results'][op_elect_id]['Sum']['9999'][indicator]
                res_dict[conf][ELECT_INDEX] = res
            elif energy_type['operation_calc_type'] == 'Heating':
                op_heat_id = energy_type['id']
                res = data[conf]['output']['results'][op_heat_id]['Sum']['9999'][indicator]
                res_dict[conf][HEAT_INDEX] = res
            if res_dict[conf][ELECT_INDEX] and res_dict[conf][HEAT_INDEX]:  # explicit
                break


    # Begin plot
    mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=constants.colors_transparent) # Hvad gøre denne?
    mpl.rcParams["figure.figsize"] = (10, 7)

    cycler1 = itertools.cycle(constants.colors)
    cycler2 = itertools.cycle(reversed(constants.colors))
    # TODO: Play more with color cycles, and test using index from constants.py
    cycler3 = itertools.cycle(constants.colors)

    labels = list(res_dict.keys())
    values = list(res_dict.values())

    # Row takes all the first elements of each row and puts it together as a column in list
    column_elect = [row[0] for row in values]
    print(column_elect)
    column_heat = [row[1] for row in values]

    x = np.arange(len(labels))  # The label locations
    width = 0.3  # The width of the bars used in LCAbyg

    fig, ax = plt.subplots()
    next(cycler2)  # Cycle over ugly green
    rects1 = ax.bar(x - width/2, column_elect, width, linewidth=2, label='Electricity', fill=True, facecolor=next(cycler2), edgecolor=('black'))
    rects2 = ax.bar(x + width/2, column_heat, width, linewidth=2, label='Heating', fill=True, facecolor=next(cycler2), edgecolor=('black'))


    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_edgecolor('grey')
    ax.spines['left'].set_edgecolor('grey')
    plt.rc('axes', axisbelow=True)
    plt.grid(axis='y')
    # comp_elect_heat_legends
    plt.ylabel(constants.comp_elect_heat_y_axis_labels['indicators'].replace("#", constants.indicator_with_units['gwp'].replace("#", constants.normalized_indicator_unit['total'])))
    plt.figtext(.5, .93, constants.comp_elect_heat_title['total'], fontsize=18, ha='center')

    ax.set_xticks(x, labels)
    ax.legend()
    ax.bar_label(rects1, padding=1)
    print(ax.bar_label(rects1, padding=1))
    ax.bar_label(rects2, padding=1)

    # Finding the best position for legends and putting it
    plt.legend(loc='lower center', ncol=100, bbox_to_anchor=(0.5, -0.13), frameon=False)

    plt.show()

if __name__ == '__main__':
    main()
