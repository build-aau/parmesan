import matplotlib.pyplot as plt
from operator import add
import restructure_data

def get_results(data, indicator):
    """
    Function to extract results from data for specified indicator
    The funktion sorts the results by stages in dictionaries with lists of results as values.
    Each list represents a stage and contains the results for each configuration.
    :param data: Tree structured dictionary containing the model and results for each configuration
    :param indicator: String containing name of indicator
    :return: Tuple with dictionary containing results and list of configuration names
    """
    stages = ['A1to3', 'B4', 'B6', 'C3', 'C4'] # The stages which are supported at the moment
    # TODO: incorporate all stages, but discard those with no value
    res_dict = {}
    config_names = []
    for stage in stages:
        res_dict[stage] = []
        for conf in data:
            # List to collect the of the configurations
            if conf not in config_names:
                config_names.append(conf)
            building_data = restructure_data.find_building(data, conf)
            id_building = building_data['id']

            res = data[conf]['output']['results'][id_building][stage]['9999'][indicator]
            res_dict[stage].append(res)
    return res_dict, config_names;

def plot_results(config_names, res_dict, indicator):
    """
    Function to plot stacked bar plot.
    :param config_names: List with strings as configuration names.
    :param res_dict: Dictionary with stages as keys and lists with results as values
    :param indicator: String containing name of indicator
    :return:
    """
    stages = ['A1to3', 'B4', 'B6', 'C3', 'C4']
    width = 0.35
    fig, graph_stages = plt.subplots()

    # List to contain the accumulated results for stacking the bars
    accum = []
    for i in range(len(stages)):
        accum.append(0)
    count = 0

    # Each group of results per stage are placed on top of the previous bar
    for stage in stages:
        if count == 0:
            graph_stages.bar(config_names, res_dict[stages[count]], width, label=stages[count])
            accum = list(map(add, accum, res_dict[stages[count]]))
        else:
            graph_stages.bar(config_names, res_dict[stages[count]], width, bottom=accum,
                             label=stages[count])
            accum = list(map(add, accum, res_dict[stages[count]]))
        count += 1
    print('kurt')
    graph_stages.set_ylabel(indicator + ' [kg CO2-eq]')
    graph_stages.set_title('Impact distributed on stages for ' + indicator)
    graph_stages.legend()

def main():
    """
    restructure_data.tree_structure to add a tree structure to the model data.
    restructure_data.find_building to locate the building id.
    :return:
    """

    data = restructure_data.tree_structure('res/api_saved_res/output_case2_conf_gen2/case2_results_collected.json')

    indicator = 'GWP'

    res_dict, config_names = get_results(data, indicator)
    plot_results(config_names, res_dict, indicator)
    plt.show()

if __name__ == '__main__':
    main()