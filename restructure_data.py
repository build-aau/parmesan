import json
# Please note: "conf_id" represents the "conf_key" in the output dictionary from the API
def create_children(node_id, nodes, edges_from):
    """
    Creates children of nodes
    :param node_id:
    :param nodes:
    :param edges_from:
    :return:
    """
    target_node = nodes[node_id]

    if node_id in edges_from:
        for child_id in edges_from[node_id]:
            if 'children' not in target_node:
                target_node['children'] = dict()

            target_node['children'][child_id] = nodes[child_id]

            create_children(child_id, nodes, edges_from)

def tree_structure(data_path):
    """
    Converts the data from list structure to tree structure

    :param data_path: relative path of where the data organized as list structure is located
    :return:
    """
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for conf, conf_data in data.items():
        nodes = dict()
        edges_from = dict()  # key = from node, list of nodes to

        bld_node = None

        model = conf_data['output']['model']

        for node in model:
            assert node['id'] not in nodes
            nodes[node['id']] = node

            if node['node_type'] == 'Building':
                bld_node = node

            edge_from = node['parent']
            edge_to = node['id']
            if edge_from is not None:
                if edge_from not in edges_from:
                    edges_from[edge_from] = list()

                edges_from[edge_from].append(edge_to)

        assert bld_node is not None

        create_children(bld_node['id'], nodes, edges_from)
    return data


def find_building(data, conf_id):
    for node in data[conf_id]['output']['model']:
        if node['node_type'] == 'Building':
            return node
    raise Exception('No building found')

def find_node_from_node_instance_id(data, conf_id, node_id): # fra instans id
    """
    USAGE: Hotspots_tree_2plots.py script, to allow for the user to select a node to investigate further.

    :param data: The restructured data.
    :param conf_id: Configuration id, example: conf_000000.json (the first keys in the dictionary containing all output from the API.)
    :param node_id: Id if the node 'ElementInstance' in the output file from the API. For other types of instances model_id should be used.
    # TODO: Add list of all types of instances that used node_id
    :return:
    """
    for node in data[conf_id]['output']['model']:
        if node['id'] == node_id:
            return node
    raise Exception(f'No node for the given node id is found {node_id}')

def find_node_from_node_model_id(data, conf_id, node_model_id): # fra model id
    """
    USAGE: Hotspots_tree_2plots.py script, to allow for the user to select a node to investigate further..

    :param data: The restructured data.
    :param conf_id: Configuration id, example: conf_000000.json (the first keys in the dictionary containing all output from the API.)
    :param node_model_id:  Used for the other types of instances model_id.
    # TODO: Add list of all types of instances that used node_model_id
    :return:
    """
    for node in data[conf_id]['output']['model']:
        if node['model_id'] == node_model_id:
            return node
    raise Exception(f'No node for the given node model id is found {node_model_id}')


def find_children_of_type(parent_node, child_type):
    children_nodes = []
    for child_id, child in parent_node['children'].items():
        if child['node_type'] == child_type:
            children_nodes.append(child)
    return children_nodes

def find_one_child_of_type(parent_node, child_type):
    only_child = find_children_of_type(parent_node, child_type)
    assert len(only_child) == 1
    return only_child[0]


def find_children_in_list(parent_node_list, child_type):
    """
    Find children in a list.

    :param parent_node_list:
    :param child_type: = white_list
    :return:
    """
    children_nodes = []
    for parent_node in parent_node_list:

        children_list = find_children_of_type(parent_node, child_type)
        children_nodes.extend(children_list)
    return children_nodes


def find_all_children_of_type(target_node, child_type, save_data, allowed_cat):
    """
    Recursive function

    :param target_node:
    :param child_type:
    :param save_data:
    :param allowed_cat: filter by white-list
    :return:
    """
    if target_node['node_type'] == child_type:
        save_data.append(target_node)
    if target_node['node_type'] == 'ElementCategoryInstance' and target_node['model_id'] not in allowed_cat:
        return
    if 'children' in target_node:
        for _, child in target_node['children'].items():
            find_all_children_of_type(child, child_type, save_data, allowed_cat)


def find_all_children_of_type_with_children(target_node, child_type, save_data):
    """
    About: Recursive function that filters the target_nodes from which do not have children
    allowed category is built into "and 'children' in target_node"

    Usage: For one configuration

    :param target_node: Starting point
    :param child_type: Where you specify which type of node you want out (filter)
    :param save_data: Input, output is used as the output list you dump to. The list must be empty when you call it the first time. This is the selected data you want to save
    :return:
    """

    if target_node['node_type'] == child_type and 'children' in target_node:
        save_data.append(target_node)

        # Runs through all children of a given target node
    if 'children' in target_node:
        for _, child in target_node['children'].items():
            # Jumps down on a child and takes its new starting point in it
            find_all_children_of_type_with_children(child, child_type, save_data)
            # Hereafter is target_node = 'children'



def find_ancestor_of_type(target_id, conf_data, ancestor_target_node_type):
    """
    Recursive function to find ancestor of type, not efficient function

    :param target_id:
    :param conf_data:
    :param ancestor_target_node_type:
    :return:
    """
    target_node = None # svarer til ikke fundet nogen
    for node in conf_data['output']['model']:
        if node['id'] == target_id:
            target_node = node
            break
    assert target_node is not None

    if target_node['node_type'] == ancestor_target_node_type:
        return target_node
    else:
        # target_node['parent'] # arget node when we call ourselves again
        # if not found, it jumped a steps backwards into the tree data structure
        return find_ancestor_of_type(target_node['parent'], conf_data, ancestor_target_node_type)

# TODO: Go backwards an find all ancestors? See def below
'''
def find_ancestor_backwards_tree(target_id, conf_data, ancestor_target_node_type):
    """
    Recursive function to find the hierarchy of ancestor of type,
    Work in progress - not efficient operation

    :param target_id:
    :param conf_data:
    :param ancestor_target_node_type:
    :return:
    """
    target_node = None 
    for node in conf_data['output']['model']:
        if node['id'] == target_id:
            target_node = node
            break
    assert target_node is not None

    if target_node['node_type'] == ancestor_target_node_type:
        return target_node
    else:
        # Target node when we call ourselves again
        # target_node['parent']
        # If not found, it jumped a notch backwards into the tree
        # return find_ancestor_of_type(target_node['parent'], conf_data, ancestor_target_node_type)
        # save_data
'''
