import restructure_data
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import constants


def generate_plot_data(data, target_conf_nr, target_node_type, indicator,origin_node_id=None, origin_find_instance=True):
    """
    From the restructured data this function finds all the data for a requested target node type for a target configuration.

    :param data: The restructured data.
    :param target_conf_nr: The target configuration keyname.

    :param target_node_type: Type of nodes in the configurations that we wish to find and return.
    Valid input arguments: 'ElementInstance', 'ConstructionInstance' and 'ProductInstance'.

    :param indicator: User input, eg. 'GWP'
    :param origin_node_id: The user must tell what parent is to what they want to zoom down on. Eg. the id for a Roof Construction.
    Because the default is None it can be used without input argument, it can make sense
    that it can be None (then it goes from the building)
    :param origin_find_instance: find all instances
    :return:
    """

    if origin_node_id is not None:
        # If so, use the instance search function
        if origin_find_instance:
            origin_node = restructure_data.find_node_from_node_instance_id(data, conf_id = target_conf_nr, node_id = origin_node_id)
        else:
        # If it is not, use the model search function
            origin_node = restructure_data.find_node_from_node_model_id(data, conf_id = target_conf_nr, node_model_id = origin_node_id)
    else:
        origin_node = restructure_data.find_building(data, target_conf_nr)

    target_nodes = []
    # Retrieves the data we plot, based on the origin, all its children are found based on the target type
    # TODO: To make it possible for the user to search for more than one create a for loop here
    restructure_data.find_all_children_of_type_with_children(origin_node, target_node_type, target_nodes)
    # TODO: Only use stages from hardcode
    stages = ['A1to3', 'A4', 'A5', 'B4', 'B6', 'C3', 'C4']
    res_dict = {}
    output = []
    for node in target_nodes:
        # Assert that this is indeed true, as it should be true
        # Example: target_node_type can be ConstructionInstance
        assert node['node_type'] == target_node_type
        node_id = node['id']
        res_conf_target = {}
        for current_conf_nr in data:
            if current_conf_nr == target_conf_nr:

                res_target_node = data[current_conf_nr]['output']['results'][node_id]

                # Loop through list of stages
                for stage in stages:
                    if stage in res_target_node:
                        res_conf_target[stage] = (res_target_node[stage]['9999'][indicator])
                    elif stage not in res_target_node:
                        res_conf_target[stage] = 0.0

                if res_target_node['Sum']:
                    res_conf_target['Sum'] = (res_target_node['Sum']['9999'][indicator])
                elif res_target_node['Sum'] is None: # If not null, None
                    res_conf_target['Sum'] = 0.0

                # True if not empty dictionary, false if empty dictionary, or None
                if not node['name']:
                    raise Exception(f'No name found for node with id: {node_id}')
                # Force the order it looks through the different languages
                else:
                    if node['name']['English']:
                        label_name = node['name']['English']
                    elif node['name']['Danish']:
                        label_name = node['name']['Danish']
                    elif node['name']['German']:
                        label_name = node['name']['German']

                res_conf_target['id'] = node['model_id']
                res_conf_target['label'] = label_name

                output.append(res_conf_target)

    return output, target_nodes

def analysis_stacked(data, conf_target_name, target_node_type, indicator, origin_node_id, origin_find_instance):
    """
    Used when the user chooses to plot the stages stacked on top of each other.

    The target configuration is used to sort the values. The order of the target values is
    then applied to the other configurations.

    :param data: restructured data
    :param conf_target_name: the target conf that values are sorted by
    :param target_node_type: Type of nodes in the configurations that we wish to find and return.
    Valid input arguments: 'ElementInstance', 'ConstructionInstance' and 'ProductInstance'.
    :param indicator: User input, eg. 'GWP'
    :param origin_node_id: The user must tell what parent is to what they want to zoom down on. Eg. the id for a Roof Construction.
    Because the default is None it can be used without input argument, it can make sense
    that it can be None (then it goes from the building)
    :param origin_find_instance:
    :return:
    res_dict (dictionary containing all results),
    x_values (label names for elements, constructions or products),
    y_values (nested listed with nested dict of all values)
    """

    res_dict = {}
    for conf_nr in data:
        if conf_nr == conf_target_name:
            # Generate target_data. Target_data is the data for the target configuration that we wish to based our sorting of values on
            target_data,_ = generate_plot_data(data, conf_target_name, target_node_type, indicator, origin_node_id, origin_find_instance)
            # sort by sum data
            target_data.sort(key=lambda x: x['Sum'], reverse=False)
            # Choose only the 10 largest values
            res_dict[conf_nr] = target_data[0:10]

        if conf_nr != conf_target_name:
            # Generate the data for the remaining configurations (will be sorted accordingly to sorted values of the target configuration.
            other_data,_ = generate_plot_data(data, conf_nr, target_node_type, indicator, origin_node_id, origin_find_instance)
            res_dict[conf_nr] = other_data

    # Initialize list for sorting the other configurations
    y_values = [[]] # Values for each configuration
    x_values = [] # Names for elements

    # Please note that the stages are hardcoded
    stages = ['A1to3', 'A4', 'A5', 'B4', 'B6', 'C3', 'C4']

    # Updates list of element names, construction names and product names automatically
    for x in res_dict[conf_target_name]:
        x_values.append(x['label'])

    # Target
    y_values[0].append({})
    # Run through the full list of elements
    for stage in stages:
        element_values_per_stage = []
        for x in res_dict[conf_target_name]:
            element_values_per_stage.append(x[stage])
        y_values[0][0][stage] = element_values_per_stage

    for conf_nr in res_dict:
        if conf_nr != conf_target_name:
            y_values.append([])
            y_values[-1].append({})
            other_res_id = []

            for target_res in res_dict[conf_target_name]:
                # Other_value 0 represent Null (none in JSON)
                other_value = 0

                # Check if found match between other and target.
                # If not, then append empty value to ensure same dimensionality.
                found_match = False
                for other_res in res_dict[conf_nr]:
                    if target_res['id'] == other_res['id']:
                        found_match = True
                        other_res_id.append(other_res['id'])
                        # Exit inner for loop to save time
                        break
                if not found_match:
                    # Append empty construction
                    other_res_id.append(None)

            for stage in stages:
                element_values_per_stage = []
                for res in other_res_id:
                    if res is None:
                        element_values_per_stage.append(0)
                        # Continue to next iteration
                        continue
                    # If the elements had been organized as dict with ids as keys we could have avoided this loop
                    for x in res_dict[conf_nr]:
                        if x['id'] == res:
                            other_value = x[stage]
                            element_values_per_stage.append(other_value)
                            break
                y_values[-1][-1][stage] = element_values_per_stage
    # Returns variables that are used in the function generate_plot
    return res_dict, x_values, y_values

def store_accum_values(accum):
    """
    Helper-function that handles negative values.
    It is assumed that only stage A1to3 holds negative values.
    Work in progress.

    :param accum:
    :return:
    """
    count_accum = 0
    for j in accum:
        if j < 0:
            accum[count_accum] = 0
            count_accum += 1
        else:
            accum[count_accum] += j
            count_accum += 1
    return accum

def generate_plot_stacked(data, conf_target_name, target_node_type, indicator, origin_node_id, origin_find_instance, origin_english_trans):
    """
    Used when the user chooces to see all the stages stacked on top of each other.

    :param data: restructured data
    :param conf_target_name: the target conf that values are sorted by
    :param target_node_type: Type of nodes in the configurations that we wish to find and return.
    Valid input arguments: 'ElementInstance', 'ConstructionInstance' and 'ProductInstance'.
    :param indicator: User input, eg. 'GWP'
    :param origin_node_id: The user must tell what parent is to what they want to zoom down on. Eg. the id for a Roof Construction.
    Because the default is None it can be used without input argument, it can make sense
    that it can be None (then it goes from the building)
    :param origin_find_instance:
    :param origin_english_trans:
    :return:
    res_dict (dictionary containing all results),
    x_values (label names for elements, constructions or products),
    y_values (nested listed with nested dict of all values)
    """

    # TODO: Make y-axis names dobbelt line
    # Please note that the stages are hardcoded
    stages = ['A1to3', 'A4', 'A5', 'B4', 'B6', 'C3', 'C4']

    # Calls the function analysis and gets the needed variables to produce the plot
    res_dict, x_values, y_values = analysis_stacked(data, conf_target_name, target_node_type, indicator, origin_node_id, origin_find_instance)

    mpl.rcParams["figure.figsize"] = (10, 10)

    width = 0.19
    x = np.arange(len(x_values))

    # Generate user-friendly names for the configurations
    extract_labels = []
    for k in res_dict.keys():
        extract_labels.append(k)
    user_fiendly_labels = [ele.replace('0', '', 5) for ele in extract_labels]
    user_friendly_conf_target_name = conf_target_name.replace('0', '', 5)

    count_conf = 0
    fig, graph_stages = plt.subplots()
    # Each group of results per stage are placed on top of the previous bar
    graph_stages.spines['top'].set_visible(False)
    graph_stages.spines['right'].set_visible(False)
    graph_stages.spines['bottom'].set_edgecolor('grey')
    graph_stages.spines['left'].set_edgecolor('grey')

    for conf in y_values:
        count_stages = 0
        accum = []
        for i in range(len(x_values)):
            accum.append(0)
        # Runs through list of all stages, except D, and assign color
        for stage in stages:
            # a1t3
            if count_stages == 0:
                graph_stages.barh(x + width * count_conf, y_values[count_conf][0][stage], width, color='#5CB283', linewidth=0.2, edgecolor='grey')
                count_accum = 0
                for j in accum:
                    if y_values[count_conf][0][stage][count_accum] < 0:
                        accum[count_accum] = 0
                    else:
                        accum[count_accum] += y_values[count_conf][0][stage][count_accum]
                    count_accum += 1
                count_stages += 1
            # a4
            elif count_stages == 1:
                graph_stages.barh(x + width * count_conf, y_values[count_conf][0][stage], width, left=accum, color='#C5CD7D', linewidth=0.2, edgecolor='grey')
                count_accum = 0
                for j in accum:
                    accum[count_accum] += y_values[count_conf][0][stage][count_accum]
                    count_accum += 1
                count_stages += 1
            # a5
            elif count_stages == 2:
                graph_stages.barh(x + width * count_conf, y_values[count_conf][0][stage], width, left=accum, color='#324951AA', linewidth=0.2, edgecolor='grey')
                count_accum = 0
                for j in accum:
                    accum[count_accum] += y_values[count_conf][0][stage][count_accum]
                    count_accum += 1
                count_stages += 1
            # b4
            elif count_stages == 3:
                graph_stages.barh(x + width * count_conf, y_values[count_conf][0][stage], width, left=accum, color='#5CB283AA', linewidth=0.2, edgecolor='grey')
                count_accum = 0
                for j in accum:
                    accum[count_accum] += y_values[count_conf][0][stage][count_accum]
                    count_accum += 1
                count_stages += 1
            # b6
            elif count_stages == 4:
                graph_stages.barh(x + width * count_conf, y_values[count_conf][0][stage], width, left=accum, color='black',linewidth=0.2, edgecolor='grey')
                count_accum = 0
                for j in accum:
                    accum[count_accum] += y_values[count_conf][0][stage][count_accum]
                    count_accum += 1
                count_stages += 1
            # c3
            elif count_stages == 5:
                graph_stages.barh(x + width * count_conf, y_values[count_conf][0][stage], width, left=accum, color='#23949AAA', linewidth=0.2, edgecolor='grey')
                count_accum = 0
                for j in accum:
                    accum[count_accum] += y_values[count_conf][0][stage][count_accum]
                    count_accum += 1
                count_stages += 1
            # c4
            elif count_stages == 6:
                graph_stages.barh(x + width * count_conf, y_values[count_conf][0][stage], width, left=accum, color='#23949A', linewidth=0.2, edgecolor='grey')
                count_accum = 0
                for j in accum:
                    accum[count_accum] += y_values[count_conf][0][stage][count_accum]
                    count_accum += 1
                count_stages += 1
        count_conf += 1

    # TODO: Make more grid lines.
    plt.grid(axis='x', linestyle='dotted', linewidth=0.75)
    plt.xlabel(constants.comp_elect_heat_y_axis_labels['indicators'].replace("#", constants.indicator_with_units[
        'gwp'].replace("#", constants.normalized_indicator_unit['total'])))

    # When user has not given an input for origin_node_id, orginin_node_id = None, thus given the entire building as origin_node_id
    if target_node_type == 'ElementInstance':
        plt.figtext(.5, .93, constants.hotspot_titles_all_building['element'] + " (Total)", fontsize=16, ha='center')
        plt.subplots_adjust(left=0.15, top=0.8)

    elif target_node_type == 'ConstructionInstance':
        plt.figtext(.5, .93, constants.hotspot_titles_all_building['construction'] + " (Total)", fontsize=18, ha='center')
        plt.subplots_adjust(left=0.3, top=0.8)
    elif target_node_type == 'ProductInstance':
        plt.figtext(.5, .93, constants.hotspot_titles_all_building['product'] + " (Total)", fontsize=18, ha='center')
        plt.subplots_adjust(left=0.3, top=0.8)


    textstr = '\n'.join((
        'Sorted by:',
        ' ',
        user_friendly_conf_target_name,
        ' ',
        'Shown in the',
        'following order:',
        ' ',
        user_friendly_conf_target_name,
        user_fiendly_labels[1],
        user_fiendly_labels[2],
        user_fiendly_labels[3],
        user_fiendly_labels[4],
                    ))

    props = dict(boxstyle='square', facecolor='white', alpha=0.5, edgecolor='grey')
    graph_stages.text(1.025, 0.65, textstr, transform=graph_stages.transAxes, fontsize=8, bbox=props)

    textstr_2 = '\n'.join((
        f'Showing only the 10 {target_node_type}\' s',
        'with the highest values for the select indicator'
    ))
    props = dict(boxstyle='square', facecolor='white', alpha=0.5, edgecolor='grey')
    graph_stages.text(-0.35, 0.95, textstr_2, transform=graph_stages.transAxes, fontsize=8, bbox=props)

    # Plot legend with information about stages
    # TODO: Add note saying: 'stage D not included'
    legend_1 = mpl.pyplot.legend(['A1to3', 'B4', 'C3', 'C4'], loc='lower right', bbox_to_anchor=(1.12, 0), borderaxespad=0., title='Stages', prop = {"size": 8})
    legend_1 = graph_stages.get_legend()
    legend_1.legendHandles[0].set_color('#5CB283')
    legend_1.legendHandles[1].set_color('#5CB283AA')
    legend_1.legendHandles[2].set_color('#23949AAA')
    legend_1.legendHandles[3].set_color('#23949A')

    plt.gca().add_artist(legend_1)
    mpl.pyplot.yticks(ticks=x, labels=x_values)
    mpl.pyplot.tick_params(axis='x', labelsize=8)
    mpl.pyplot.tick_params(axis='y', labelsize=8)

    plt.show()

def analysis_target_res(data, conf_target_name, target_node_type, indicator, origin_node_id, origin_find_instance, target_stage):
    """
    Used when the user chooses to plot the stages together or just one stage by itself.

    The target configuration is used to sort the values. The order of the target values is
    then applied to the other configurations.

    :param data: restructured data
    :param conf_target_name: the target conf that values are sorted by
    :param target_node_type: Type of nodes in the configurations that we wish to find and return.
    Valid input arguments: 'ElementInstance', 'ConstructionInstance' and 'ProductInstance'.
    :param indicator: User input, eg. 'GWP'
    :param origin_node_id:The user must tell what parent is to what they want to zoom down on. Eg. the id for a Roof Construction.
    Because the default is None it can be used without input argument, it can make sense
    that it can be None (then it goes from the building)
    :param origin_find_instance:
    :param input_stage:
    :return:
    res_dict (dictionary containing all results),
    x_values (label names for elements, constructions or products),
    y_values (nested listed with nested dict of all values)
    """
    res_dict = {}
    for conf_nr in data:
        if conf_nr == conf_target_name:

            # Generate target_data. Target_data is the data for the target configuration that we wish to based our sorting of values on
            target_data,_ = generate_plot_data(data, conf_target_name, target_node_type, indicator, origin_node_id, origin_find_instance)

            target_data.sort(key=lambda x: x['Sum'], reverse=True)
            res_dict[conf_nr] = target_data[0:10]

        if conf_nr != conf_target_name:
            # Generate the data for the remaining configurations (will be sorted accordingly to sorted values of the target configuration.
            other_data,_ = generate_plot_data(data, conf_nr, target_node_type, indicator, origin_node_id, origin_find_instance)
            res_dict[conf_nr] = other_data

    # Initialize list for sorting the other configurations
    y_values = [[]] # Values for each configuration
    x_values = [] # Names for elements

    # If target conf...
    for x in res_dict[conf_target_name]:
        x_values.append(x['label']) #Terrændæk, ELement navne
        y_values[0].append(x['Sum'])

    # Append the data for the other configurations
    for conf_nr in res_dict:
        if conf_nr != conf_target_name:
            y_values.append([])

            for target_res in res_dict[conf_target_name]:
                # Other_value 0 represent Null (none in JSON)
                other_value = 0
                for other_res in res_dict[conf_nr]:
                    if target_res['id'] == other_res['id']:
                        other_value = other_res['Sum']
                        break
                y_values[-1].append(other_value)
    # Returns variables that are used in the function generate_plot
    return res_dict, x_values, y_values

def generate_plot_target_res(data, conf_target_name, target_node_type, indicator, origin_node_id, origin_find_instance, origin_english_trans, target_stage): #res_dict, x_values, y_values,
    # TODO: Make y-axis names dobbelt line
    target_stage = False
    # Calls the function analysis and gets the needed variables to produce the plot
    res_dict, x_values, y_values = analysis_target_res(data, conf_target_name, target_node_type, indicator, origin_node_id, origin_find_instance, target_stage)

    mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=constants.colors_transparent)
    mpl.rcParams["figure.figsize"] = (8, 7)

    fig, graph_stages = plt.subplots()
    # Each group of results per stage are placed on top of the previous bar
    # TODO: Fix the spines
    graph_stages.spines['top'].set_visible(False)
    graph_stages.spines['right'].set_visible(False)
    graph_stages.spines['bottom'].set_edgecolor('grey')
    graph_stages.spines['left'].set_edgecolor('grey')
    width = 0.1
    x = np.arange(len(x_values))
    fig, graph_stages = plt.subplots()
    extract_labels = []
    for k in res_dict.keys():
        extract_labels.append(k)

    # Conf_0 can be decided to work as a baseline configuraiton?
    # Replace only the first 5 leading zeroes by blanc spaces.
    user_fiendly_labels = [ele.replace('0', '', 5) for ele in extract_labels]
    user_friendly_conf_target_name = conf_target_name.replace('0', '', 5)

    # Enumerate can use two variables height and counter (i)
    # barh automatically flips the x-axis with the y-axis
    for i, height in enumerate(y_values):
        plt.barh(x + width * i, height, width, label=user_fiendly_labels[i], linewidth=2)

    plt.grid(axis='x')
    plt.xlabel(constants.comp_elect_heat_y_axis_labels['indicators'].replace("#", constants.indicator_with_units[
        'gwp'].replace("#", constants.normalized_indicator_unit['total'])))
    # When user has not given an input for origin_node_id, orginin_node_id = None, thus given the entire building as origin_node_id
    if target_node_type == 'ElementInstance':
        plt.figtext(.5, .93, constants.hotspot_titles_all_building['element'] + " (Total)", fontsize=16, ha='center')
        plt.subplots_adjust(left=0.15, top=0.8)

    elif target_node_type == 'ConstructionInstance':
        plt.figtext(.5, .93, constants.hotspot_titles_all_building['construction'] + " (Total)", fontsize=18,
                    ha='center')
        plt.subplots_adjust(left=0.3, top=0.8)
    elif target_node_type == 'ProductInstance':
        plt.figtext(.5, .93, constants.hotspot_titles_all_building['product'] + " (Total)", fontsize=18, ha='center')
        plt.subplots_adjust(left=0.3, top=0.8)

    textstr = '\n'.join((
        'Sorted by:',
        ' ',
        user_friendly_conf_target_name,
        ' ',
        'Shown in the',
        'following order:',
        ' ',
        user_friendly_conf_target_name,
        user_fiendly_labels[1],
        user_fiendly_labels[2],
        user_fiendly_labels[3],
        user_fiendly_labels[4],
    ))

    props = dict(boxstyle='square', facecolor='white', alpha=0.5, edgecolor='grey')
    graph_stages.text(1.025, 0.65, textstr, transform=graph_stages.transAxes, fontsize=8, bbox=props)

    textstr_2 = '\n'.join((
        f'Showing only the 10 {target_node_type}\' s',
        'with the highest values for the select indicator'
    ))
    props = dict(boxstyle='square', facecolor='white', alpha=0.5, edgecolor='grey')
    graph_stages.text(-0.35, 0.95, textstr_2, transform=graph_stages.transAxes, fontsize=8, bbox=props)

    mpl.pyplot.yticks(ticks=x, labels=x_values)
    mpl.pyplot.tick_params(axis='x', labelsize=8)
    mpl.pyplot.tick_params(axis='y', labelsize=8)

    plt.show()

def analysis_target_stage(data, conf_target_name, target_node_type, indicator, origin_node_id, origin_find_instance, target_stage):
    """
    Used when the user chooses to plot the stages together or just one stage by itself.

    The target configuration is used to sort the values. The order of the target values is
    then applied to the other configurations.

    :param data: restructured data
    :param conf_target_name: the target conf that values are sorted by
    :param target_node_type: Type of nodes in the configurations that we wish to find and return.
    Valid input arguments: 'ElementInstance', 'ConstructionInstance' and 'ProductInstance'.
    :param indicator: User input, eg. 'GWP'
    :param origin_node_id:The user must tell what parent is to what they want to zoom down on. Eg. the id for a Roof Construction.
    Because the default is None it can be used without input argument, it can make sense
    that it can be None (then it goes from the building)
    :param origin_find_instance:
    :param input_stage:
    :return:
    res_dict (dictionary containing all results),
    x_values (label names for elements, constructions or products),
    y_values (nested listed with nested dict of all values)
    """
    res_dict = {}
    for conf_nr in data:
        if conf_nr == conf_target_name:

            # Generate target_data. Target_data is the data for the target configuration that we wish to based our sorting of values on
            target_data,_ = generate_plot_data(data, conf_target_name, target_node_type, indicator, origin_node_id, origin_find_instance)

            # Obs stage is hardcoded
            target_data.sort(key=lambda x: x['A1to3'], reverse=True)
            res_dict[conf_nr] = target_data[0:10]

        if conf_nr != conf_target_name:
            # Generate the data for the remaining configurations (will be sorted accordingly to sorted values of the target configuration.
            other_data,_ = generate_plot_data(data, conf_nr, target_node_type, indicator, origin_node_id, origin_find_instance)
            res_dict[conf_nr] = other_data

    # Initialize list for sorting the other configurations
    y_values = [[]] # Values for each configuration
    x_values = [] # Names for elements

    # If target conf...
    for x in res_dict[conf_target_name]:
        x_values.append(x['label']) #Terrændæk, ELement navne
        y_values[0].append(x['A1to3'])

    # Append the data for the other configurations
    for conf_nr in res_dict:
        if conf_nr != conf_target_name:
            y_values.append([])

            for target_res in res_dict[conf_target_name]:
                # Other_value 0 represent Null (none in JSON)
                other_value = 0
                for other_res in res_dict[conf_nr]:
                    if target_res['id'] == other_res['id']:
                        other_value = other_res['A1to3']
                        break
                y_values[-1].append(other_value)
    # Returns variables that are used in the function generate_plot
    return res_dict, x_values, y_values


def generate_plot_target_stage(data, conf_target_name, target_node_type, indicator, origin_node_id, origin_find_instance, origin_english_trans, target_stage): #res_dict, x_values, y_values,
    # TODO: Make y-axis names dobbelt line
    target_stage = False
    # Calls the function analysis and gets the needed variables to produce the plot
    res_dict, x_values, y_values = analysis_target_res(data, conf_target_name, target_node_type, indicator, origin_node_id, origin_find_instance, target_stage)

    mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=constants.colors_transparent)
    mpl.rcParams["figure.figsize"] = (8, 7)

    fig, graph_stages = plt.subplots()
    # Each group of results per stage are placed on top of the previous bar
    # TODO: Fix the spines
    graph_stages.spines['top'].set_visible(False)
    graph_stages.spines['right'].set_visible(False)
    graph_stages.spines['bottom'].set_edgecolor('grey')
    graph_stages.spines['left'].set_edgecolor('grey')
    width = 0.1
    x = np.arange(len(x_values))
    fig, graph_stages = plt.subplots()
    extract_labels = []
    for k in res_dict.keys():
        extract_labels.append(k)

    # Conf_0 can be decided to work as a baseline configuraiton?
    # Replace only the first 5 leading zeroes by blanc spaces.
    user_fiendly_labels = [ele.replace('0', '', 5) for ele in extract_labels]
    user_friendly_conf_target_name = conf_target_name.replace('0', '', 5)

    # Enumerate can use two variables height and counter (i)
    # barh automatically flips the x-axis with the y-axis
    for i, height in enumerate(y_values):
        plt.barh(x + width * i, height, width, label=user_fiendly_labels[i], linewidth=2)

    plt.grid(axis='x')
    plt.xlabel(constants.comp_elect_heat_y_axis_labels['indicators'].replace("#", constants.indicator_with_units[
        'gwp'].replace("#", constants.normalized_indicator_unit['total'])))
    # When user has not given an input for origin_node_id, orginin_node_id = None, thus given the entire building as origin_node_id
    if target_node_type == 'ElementInstance':
        plt.figtext(.5, .93, constants.hotspot_titles_all_building['element'] + " (Total)", fontsize=16, ha='center')
        plt.subplots_adjust(left=0.15, top=0.8)

    elif target_node_type == 'ConstructionInstance':
        plt.figtext(.5, .93, constants.hotspot_titles_all_building['construction'] + " (Total)", fontsize=18,
                    ha='center')
        plt.subplots_adjust(left=0.3, top=0.8)
    elif target_node_type == 'ProductInstance':
        plt.figtext(.5, .93, constants.hotspot_titles_all_building['product'] + " (Total)", fontsize=18, ha='center')
        plt.subplots_adjust(left=0.3, top=0.8)

    textstr = '\n'.join((
        'Sorted by:',
        ' ',
        user_friendly_conf_target_name,
        ' ',
        'Shown in the',
        'following order:',
        ' ',
        user_friendly_conf_target_name,
        user_fiendly_labels[1],
        user_fiendly_labels[2],
        user_fiendly_labels[3],
        user_fiendly_labels[4],
    ))

    props = dict(boxstyle='square', facecolor='white', alpha=0.5, edgecolor='grey')
    graph_stages.text(1.025, 0.65, textstr, transform=graph_stages.transAxes, fontsize=8, bbox=props)

    textstr_2 = '\n'.join((
        f'Showing only the 10 {target_node_type}\' s',
        'with the highest values for the select indicator'
    ))
    props = dict(boxstyle='square', facecolor='white', alpha=0.5, edgecolor='grey')
    graph_stages.text(-0.35, 0.95, textstr_2, transform=graph_stages.transAxes, fontsize=8, bbox=props)

    mpl.pyplot.yticks(ticks=x, labels=x_values)
    mpl.pyplot.tick_params(axis='x', labelsize=8)
    mpl.pyplot.tick_params(axis='y', labelsize=8)

    plt.show()

def user_input(data, conf_target_name, indicator, target_node_type, origin_node_id, stacked_stages, target_stage, target_res, origin_find_instance):
    """
    Choice with branch from the tree diagram - see diagram in GitHub readme.md

    Choose one indicator category.
    # TODO: Create similar hotspots analysis where indicator categories are stacked instead of stages.
    :param w_stages: Boolean
    :return:
    """
    # OK Branch for stacked stages, for the entire building, for the 10 worst instances for the given target_node_type
    if stacked_stages and target_stage is None and target_res is None and origin_node_id is None:

        if target_node_type == 'ElementInstance':
            generate_plot_stacked(data, conf_target_name, target_node_type, indicator,
                                  origin_node_id=None, origin_find_instance=True,
                                  origin_english_trans=None)

        elif target_node_type == 'ConstructionInstance':
            generate_plot_stacked(data, conf_target_name, target_node_type, indicator,
                                  origin_node_id=None, origin_find_instance=True,
                                  origin_english_trans=None)
        elif target_node_type == 'ProductInstance':
            generate_plot_stacked(data, conf_target_name, target_node_type, indicator,
                                  origin_node_id=None, origin_find_instance=True,
                                  origin_english_trans=None)

    # OK Branch for ikke stacked stages, for Sum, for the entire building, for the 10 worst instances for the given target_node_type
    elif stacked_stages is False and target_res == ['Sum'] and target_stage is None and origin_node_id is None:

        if target_node_type == 'ElementInstance':
            generate_plot_target_res(data, conf_target_name, target_node_type, indicator,
                                     origin_node_id=None, origin_find_instance=True,
                                     origin_english_trans=None, target_stage=None)
        elif target_node_type == 'ConstructionInstance':
            generate_plot_target_res(data, conf_target_name, target_node_type, indicator,
                                     origin_node_id=None, origin_find_instance=True,
                                     origin_english_trans=None, target_stage=None)
        elif target_node_type == 'ProductInstance':
            generate_plot_target_res(data, conf_target_name, target_node_type, indicator,
                                     origin_node_id, origin_find_instance=True,
                                     origin_english_trans=None, target_stage=None)

    # OK Branch for ikke stacked stages, for Sum, for the an origin node id, for the 10 worst instances for the given target_node_type
    # Only for ConstructionInstance and ProductInstance
    # TODO: Fix issue realted to model id vs instance id
    elif stacked_stages and target_res == None and target_stage == None and origin_node_id:

        if target_node_type == 'ConstructionInstance':
            generate_plot_stacked(data, conf_target_name, target_node_type, indicator,
                                     origin_node_id=origin_node_id, origin_find_instance=origin_find_instance,
                                     origin_english_trans=None)
        elif target_node_type == 'ElementInstance':
            generate_plot_stacked(data, conf_target_name, target_node_type, indicator,
                                     origin_node_id=origin_node_id, origin_find_instance=origin_find_instance,
                                     origin_english_trans=None)
        elif target_node_type == 'ProductInstance':
            generate_plot_stacked(data, conf_target_name, target_node_type, indicator,
                                     origin_node_id=origin_node_id, origin_find_instance=origin_find_instance,
                                     origin_english_trans=None)

    # OK Branch for ikke stacked stages, for target_stage ['A1to3'], for the entire building, for the 10 worst instances for the given target_node_type
    elif stacked_stages is False and target_res is None and target_stage and origin_node_id is None:

        if target_node_type == 'ElementInstance':
            generate_plot_target_stage(data, conf_target_name, target_node_type, indicator,
                                     origin_node_id=None, origin_find_instance=True,
                                     origin_english_trans=None, target_stage=target_stage)

        elif target_node_type == 'ConstructionInstance':
            generate_plot_target_stage(data, conf_target_name, target_node_type, indicator,
                                     origin_node_id=None, origin_find_instance=True,
                                     origin_english_trans=None, target_stage=target_stage)

        elif target_node_type == 'ProductInstance':
            generate_plot_target_stage(data, conf_target_name, target_node_type, indicator,
                                     origin_node_id, origin_find_instance=True,
                                     origin_english_trans=None, target_stage=target_stage)


    else:
        print('')


def main():
    """
    Generates several types of hotspot analyses for a project containing more than one configuration.
    The user input is given in the function def user_input().
    See GitHub diagram for a full overview of the options the user has.

    TODO: Further develop the scripts (def generate_data) so that they can handle the selection of more than one element.
    This is especially relevant when comparing two projects that do not share the same instance - ids.
    Instance ids are not stable, either assume that model_ids are unique and create a chain of model_ids and implement
    the positional order of the constructions and products in a given project.
    Not implement hyper, super element categories.
    :return: the plot
    """
    data = restructure_data.tree_structure('res/api_saved_res/case2_results_collected.json')
    # If no input stage then use Sum of all stages
    stages = ['A1to3', 'A4', 'A5', 'B4', 'B6', 'C3', 'C4']  # All except D
    stacked_stages = True #False  # True
    target_res = None #['Sum']
    target_stage = None #['A1to3']
    indicator = 'GWP'
    conf_target_name = 'conf_000000'
    origin_find_instance = True
    # TODO: Implement these id's and automatic look up in user interface
    origin_node_id = None # model id '91329025-d117-4a64-a577-58bb1d76d82e' instance id 'a231a6c5-1eba-4e23-b01d-2b4edb58684d'
    origin_english_trans = 'Roof construction'
    target_node_type = 'ProductInstance'
    user_input(data, conf_target_name, indicator, target_node_type, origin_node_id, stacked_stages, target_stage, target_res, origin_find_instance)


if __name__ == '__main__':
    main()