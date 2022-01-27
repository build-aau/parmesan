import json
import os
import shutil
import copy
import collect_json

def load_json_file(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def dump_json_file(json_file, data):
    """
    Find path and create folder (using recursion) if not already there
    :param json_file:
    :param data:
    :return:
    """
    folder_path = os.path.split(json_file)[0]
    os.makedirs(folder_path, exist_ok=True)
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent = 4, ensure_ascii=False)

def save_configuration(case_data, conf_name):
    """
    Function for saving the generated configurations.

    # Organised as a follows for each configuration generated:
    # parent-folder containing not modified files and a modified element.json

    :param element_data:
    :param output_path:
    :param conf_name:
    :return:
    """

    new_case_path = os.path.join('conf', f'{conf_name}.json')
    dump_json_file(new_case_path, case_data)

def configurations_count(input_data):
    """
    # Function that determines the number of configurations
    based on a predefined methods of pairing sets into configurations.
    Example: The number of replacements for one set defines the number of possible combinations.

    Determines the number of configurations to generate.

    Requires that the length of the list of replacements be the same for all sets.
    Count is chosen to be defined based on the first set's replacements we encounter.

    :param input_data:
    :return:
    """
    count_replacements = len(input_data[0]['replacements'])
    for set_data in input_data:
        count_replacement_check = len(set_data['replacements'])
        assert count_replacement_check == count_replacements, 'Inconsistent number of replacements'
    return count_replacements

def configurations_generator(output_path):
    """
    ABOUT:

    Main function that generates a number of configurations
    based on the number of ids in the list replacements for a set in the file input_configurations.json

    Target is the node in a set that we want to replace to generate new configurations

    Target is a choose edge "EdgeToConstruction" id
    Replacement is a construction node id that is replace for the target edge.

    IMPORTANT:

    Needs case data in json format structured as describe in LCAbyg JSON guide as an input.
    Replacement ids must all be in one file names "input_configurations.json".

    :param output_path:
    :return:
    """
    output_count = 0

    # Load the files with the replacement ids
    input_data = load_json_file('data/input/input_configurations_case2.json')

    # Select the case data to generate the configurations from
    # None because no output variable
    original_case_data = collect_json.collect_json(['data/input/case2'], None)
    count_conf_generator = configurations_count(input_data)

    # Counts the number of configurations to generate
    for i in range(0, count_conf_generator):
        # Creates a clone of the case_data for each configuration of the original_case_data
        # This is done everywhere there is a reference
        case_data = copy.deepcopy(original_case_data)

        for set_data in input_data:
            target = set_data['target']

            for obj in case_data:

                if 'Edge' in obj:

                    edge_type = list(obj['Edge'][0].keys())[0]
                    if edge_type == 'ElementToConstruction':
                        edge_id_con = obj['Edge'][0][edge_type]['id']
                        if edge_id_con == target:

                            replacement = set_data['replacements'][i]
                            amount_replacement = set_data['amount_replacements'][i]
                            # Lifespan is always none for constructions
                            lifespan_replacement = set_data['lifespan_replacements'][i]

                            if replacement is not None:
                                # Replace original id with replacement id
                                obj['Edge'][2] = replacement

                            if amount_replacement is not None:
                                obj['Edge'][0]['ElementToConstruction']['amount'] = amount_replacement

                            # Lifespan is always none for constructions
                            if lifespan_replacement is not None:
                                obj['Edge'][0]['ElementToConstruction']['lifespan'] = lifespan_replacement



                    if edge_type == 'ConstructionToProduct':
                        edge_id_prod = obj['Edge'][0][edge_type]['id']

                        if edge_id_prod == target:

                            replacement = set_data['replacements'][i]
                            amount_replacement = set_data['amount_replacements'][i]
                            lifespan_replacement = set_data['lifespan_replacements'][i]

                            if replacement is not None:
                                # Replace original id with replacement id
                                obj['Edge'][2] = replacement

                            if amount_replacement is not None:
                                obj['Edge'][0]['ConstructionToProduct']['amount'] = amount_replacement

                            if lifespan_replacement is not None:
                                obj['Edge'][0]['ConstructionToProduct']['lifespan'] = lifespan_replacement


        save_configuration(case_data, f'conf_{output_count:06d}')
        output_count += 1

'''
if __name__ == '__main__':
    main()
'''



