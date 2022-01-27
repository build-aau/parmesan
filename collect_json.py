import json
import os

def collect_json(json_paths, json_dump_path):
    """
    Create a collected json file from a folder with json files
    Using os.walk to find all main and sub folders.

    This script runs in API-main, for each of the configurations.

    :param json_paths: List of paths to be wrapped (paths to folders)
    :param json_dump_path: Path to save the collected json. If no output path use the keyword "None".
    :return:
    """

    output = []
    # Save the paths in a list
    for json_path in json_paths:

        # Root = path to a folder
        # File = the files in a given folder
        # os.walk gives a long list of tuples some contain root, dirs, files that come for each folder
        for root, dirs, files in os.walk(json_path):
            for name in files:
                # Return full path and folder name
                target = os.path.join(root, name)
                # Assumed that the json folder is correct
                if os.path.splitext(target)[1].lower() == '.json':

                    with open(target, 'r', encoding='utf-8') as f:
                        json_list = json.load(f)
                        # Assuming this is true
                    output.extend(json_list)

    # Optional: Save list a file

    if json_dump_path is not None:

        with open(json_dump_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent = 4, ensure_ascii=False)

    return output