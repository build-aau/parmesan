import matplotlib.pyplot as plt
import restructure_data
import constants
import matplotlib as mpl

def accum(list_values):
    """
    Creates a list og accumulated values from a list of values
    :param list_values: Values to accumulate
    :return:
    """
    accum_value = 0
    accum_value_list = []
    for value in list_values:
        accum_value += value
        accum_value_list.append(accum_value)
    return accum_value_list

def find_results(data, config, indicator_type, res_id, res_type):
    """
    Funktion to find results for chosen indicator and types of results
    The funktion is adding a value to those

    :param data: Tree structured dictionary containing the model and results for each configuration
    :param config: string containing name of configuration in data
    :param indicator_type: string containing name of indicator
    :param res_id: string containing the id for which the result will be found
    :param res_type: string of the type of result to extract
    :return: Dictionary containing years as keys and impacts as values
    """
    dict_year = {}
    for year, indicators in data[config]['output']['results'][res_id][res_type].items():
        year_int = int(year)
        res = indicators[indicator_type]
        if len(data[config]['output']['results'][res_id][res_type]) < 3:
            if year_int != 9999 and year_int != 0:
                initial_year, lifetime, end_year = find_lifetime(data, config)
                if year_int == end_year - 1:
                    dict_year[initial_year] = 0
                    dict_year[year_int - 1] = 0
                    dict_year[year_int] = res
                elif year_int == initial_year:
                    dict_year[year_int] = res
                    dict_year[end_year] = 0
        elif year_int != 9999 and year_int != 0:
            dict_year[year_int] = res
    return dict_year

def plot_all_stages_summed(data, config, indicator_type, res_id):
    """
    This function is specifically used for plotting the accumulated embodied graph split up into stages.
    Only one configuration plotted per call
    :param data: Tree structured dictionary containing the model and results for each configuration
    :param config: String with the name of Configuration to plot for
    :param indicator_type: String with name of indicator type
    :param res_id: string containing the id for which the result will be found operation or embodied
    :return:
    """
    stages = ['A1to3', 'B4', 'C3', 'C4']
    res_dict = {}
    count_lowest_year = 10000
    latest_year = 0
    latest_indicator = 0
    count = 0
    accumulated_indicators = 0
    initial_year, lifetime, end_year = find_lifetime(data, config)
    for stage in stages:
        dict_year = {}
        for year, indicators in data[config]['output']['results'][res_id][stage].items():
            year_int = int(year)
            if count < len(stage):
                for end_year_for_stage, indicator in data[config]['output']['results'][res_id][stages[count + 1]].items():
                    end_year_stage = int(end_year_for_stage)
                    if end_year_stage < count_lowest_year and end_year_stage != initial_year:
                        count_lowest_year = end_year_stage
            count += 1
            res = indicators[indicator_type]
            if len(data[config]['output']['results'][res_id][stage]) < 3:
                if year_int != 9999 and year_int != 0:
                    if year_int == end_year - 1 and stage == 'C3':
                        accumulated_indicators += res
                        dict_year[latest_year] = latest_indicator
                        dict_year[end_year] = accumulated_indicators
                        latest_year = year_int

                        latest_indicator = accumulated_indicators

                    elif year_int == end_year - 1 and stage == 'C4':
                        accumulated_indicators += res
                        dict_year[latest_year] = latest_indicator
                        dict_year[end_year] = accumulated_indicators
                    elif year_int == initial_year:
                        accumulated_indicators += res
                        dict_year[year_int] = accumulated_indicators
                        dict_year[count_lowest_year] = accumulated_indicators
                        latest_year = year_int
                        latest_indicator = accumulated_indicators
            elif year_int != 9999 and year_int != 0:
                if len(dict_year) == 0:
                    dict_year[count_lowest_year] = accumulated_indicators
                    accumulated_indicators += res
                if year_int not in dict_year:
                    accumulated_indicators += res
                    dict_year[year_int] = accumulated_indicators


            elif year_int == 9999:
                dict_year[end_year-1] = accumulated_indicators
                latest_year = end_year-1
                latest_indicator = accumulated_indicators

        res_dict[config + ' embodied ' + stage] = dict_year
        plot_graph(res_dict, config + ' embodied ' + stage, 'solid')
        text_y_position = (list(dict_year.values())[0] + list(dict_year.values())[-1]) / 2
        if stage == 'A1to3' or stage == 'B4':
            text_x_position = (list(dict_year.keys())[0] + list(dict_year.keys())[-1]) / 2 - 3.5
            text_y_position += 0.05 * text_y_position
        else:
            text_x_position = (list(dict_year.keys())[0] + list(dict_year.keys())[-1]) / 2 - 2.5
        plt.text(text_x_position, text_y_position, stage, ha='center', fontsize=12)
    return res_dict

def plot_graph(results, config, linestyle):
    """
    Function used to plot graphs
    :param results: nested dictionary with results for the configurations
    :param config: string with name for the configurations to be plotted
    :param linestyle: string with name of the line type to use
    :return: adds the plot of results to graph
    """
    mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=constants.colors_accum)
    res = results[config]
    years = list(res.keys())
    values = list(res.values())
    plt.step(years, values, linestyle=linestyle, linewidth=4)

def plot_graph_acucum(results, config, linestyle):
    """
    Function used to plot graphs using accum to create accumulated results
    :param results: nested dictionary with results for the configurations
    :param config: string with name for the configurations to be plotted
    :param linestyle: string with name of the line type to use
    :return: adds the plot of results to graph
    """
    mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=constants.colors_accum)
    res = results[config]
    years = list(res.keys())
    values = list(res.values())
    plt.step(years, accum(values), linestyle=linestyle, linewidth=2)

def find_lifetime(data, conf):
    """
    Function to find and return the lifetime for a building
    :param data: Tree structured dictionary containing the model and results for each configuration
    :param conf: String with the name of Configuration to plot for
    :return:
    """
    initial_year = 0
    calculation_timespan = 0
    end_year = 0
    for node in data[conf]['input']:
        if 'Node' in node.keys():
            if 'Building' in node['Node'].keys():
                initial_year = node['Node']['Building']['initial_year']
                calculation_timespan = node['Node']['Building']['calculation_timespan']
                end_year = initial_year + calculation_timespan
                break
    return initial_year, calculation_timespan, end_year

def plot_result_type(data, indicator, result_type, stage, config):
    """
    Function to decide which data to plot
    :param data: Tree structured dictionary containing the model and results for each configuration
    :param indicator: String with name of indicator
    :param result_type: String with name of result type, Operation, Embodied or All
    :param stage: String with name of stage or All for all stages, or All_sum for summed stages
    :param config: String with the name of Configuration to plot for
    :return:
    """
    stages = ['A1to3', 'B4', 'C3', 'C4']
    res_dict = {}

    for conf in data:
        initial_year, lifetime, end_year = find_lifetime(data, conf)
        # only plot chosen configurations
        if config != 'All' and conf != config:
            continue
        building_data = restructure_data.find_building(data, conf)
        # Results for embodied will be plotted
        if result_type == 'All' or result_type == 'Embodied':
            embedded = restructure_data.find_one_child_of_type(building_data, 'EmbodiedRoot')
            em_id = embedded['id']
            # Will plot all stages individually without summing the values
            if stage == 'All':
                for stage_type in stages:
                    res_dict[conf + ' embodied ' + stage_type] = find_results(data, conf, indicator, em_id, stage_type)
                    plot_graph_acucum(res_dict, conf + ' embodied ' + stage_type, 'solid')
                user_friendly_conf_target_name = config.replace('0', '', 5)
                plt.title(indicator + ' for ' + user_friendly_conf_target_name + ' all stages')
            # Will plot all stages individually summed
            elif stage == 'All_sum':
                res_dict = plot_all_stages_summed(data, conf, indicator, em_id)
                user_friendly_conf_target_name = config.replace('0', '', 5)
                plt.title(indicator + ' for ' + user_friendly_conf_target_name + ' all stages summed')
            # Plots the chosen stage or sum for embedded
            else:
                res_dict[conf + ' embodied ' + stage] = find_results(data, conf, indicator, em_id, stage)
                plot_graph_acucum(res_dict, conf + ' embodied ' + stage, 'solid')
                if config == 'All':
                    plt.title(stage + ' for ' + indicator + ' for configuations')
                else:
                    user_friendly_conf_target_name = config.replace('0', '', 5)
                    plt.title(stage + ' for ' + indicator + ' for ' + user_friendly_conf_target_name)
            # Plots operation on top of the graph for embodied
            if result_type == 'All':
                operation = restructure_data.find_one_child_of_type(building_data, 'Operation')
                op_id = operation['id']
                res_dict[conf + ' operation'] = find_results(data, conf, indicator, op_id, 'Sum')
                plot_graph_acucum(res_dict, conf + ' operation', 'solid')
                #plt.title(stage + ' for ' + indicator + ' for operation and embodied')
                initial_year, lifetime, end_year = find_lifetime(data, config)
                text_y_position = list(accum(res_dict[conf + ' operation'].values()))[-1]
                text_x_position = (initial_year + end_year) / 2
                #text_y_position += 0.05 * text_y_position
                plt.text(text_x_position, text_y_position, 'Operation', ha='center', fontsize=12)
            text_x_position = (initial_year + end_year) / 2
            first_year_y_position = list((list(res_dict.values())[0]).values())[0]
            last_year_y_position = list((list(res_dict.values())[-2]).values())[-1]
            text_y_position = (first_year_y_position + last_year_y_position) / 2
            text_y_position -= 0.1 * text_y_position
            plt.text(text_x_position, text_y_position, 'Embodied', ha='center', fontsize=12)
        #plots only operation if this is chosen
        elif result_type == 'Operation':
            operation = restructure_data.find_one_child_of_type(building_data, 'Operation')
            op_id = operation['id']
            res_dict[conf + ' operation'] = find_results(data, conf, indicator, op_id, 'Sum')
            plot_graph_acucum(res_dict, conf + ' operation', 'solid')
            plt.title('Sum of ' + indicator + ' for operation')
            initial_year, lifetime, end_year = find_lifetime(data, conf)
            text_y_position = list(accum(res_dict[conf + ' operation'].values()))[-1]
            text_x_position = (initial_year + end_year) / 2
            # text_y_position += 0.05 * text_y_position
            plt.text(text_x_position, text_y_position, 'Operation', ha='center', fontsize=12)
    if stage == 'All_sum' and result_type != 'Operation':
        lifetime += 1
    else:
        extract_labels = []
        for k in res_dict.keys():
            extract_labels.append(k)
        user_friendly_labels = [ele.replace('0', '', 5) for ele in extract_labels]
        plt.legend(user_friendly_labels)

def main():
    data = restructure_data.tree_structure('res/api_saved_res/output_case2_conf_gen2/case2_results_collected.json')
    indicator = 'GWP'
    result_type = 'All'
    stage = 'All_sum'
    configuration = 'conf_000002'

    plot_result_type(data, indicator, result_type, stage, configuration)


    plt.ylabel(indicator + ' [kg CO2-eq.]')
    plt.xlabel('Time [Years]')
    plt.show()

if __name__ == '__main__':
    main()