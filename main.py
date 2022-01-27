import configurations_generator
import sbi_web_api
import os
import json

CONFIGURATIONS_PATH = 'conf'

def main():
    """
    STEPS:

    1. collect_json.collect_json
    2. generate_configurations.generate_configurations
    3. sbi_web_api.send_job
    Send the data to the LCAbyg Web API and save the output in a folder named "api_live_res".
    Thee output contains all results computed b the LCAbyg engine.
    To store output without overwriting copy the output data and place in the folder "api_saved_res"
    4. Use another script to analyse the output_data further. (They have their own main).

    IMPORTANT:

    The API requires login-information. Contact BUILD for more info.
    Please be kind to the server by not overloading it with jobs.

    :return:
    """
    selected_results_dict = dict()
    configurations_generator.configurations_generator(CONFIGURATIONS_PATH)
    # Return in order not to spam the LCAbyg web API server:
    #return

    for conf in os.listdir(CONFIGURATIONS_PATH):

        conf_path = os.path.join(CONFIGURATIONS_PATH, conf)
        input_api_path = conf_path
        # User input: upload case data in json format
        case_name = 'case2'
        correct_conf_name = os.path.splitext(conf)[0]


        output_api_path = os.path.join('res/api_live_res', f'results_{conf}')

        # Function calling LCAbyg API using login and password
        if 'SWAPI_USERNAME' in os.environ and 'SWAPI_PASSWORD' in os.environ:
            username = os.environ['SWAPI_USERNAME']
            password = os.environ['SWAPI_PASSWORD']
        else:
            raise Exception('Supply a SBI Web API username and password via the env variables SWAPI_USERNAME and SWAPI_PASSWORD')
        print(input_api_path)
        print(output_api_path)
        sbi_web_api.send_job(input_api_path, output_api_path, username, password)


        with open(output_api_path, 'r', encoding='utf-8') as f:
            json_list_output = json.load(f)

        # Remember to update if we save it in a new folder
        with open(input_api_path, 'r', encoding='utf-8') as f:
            json_list_input = json.load(f)
        selected_results_dict[correct_conf_name] = {'output': json_list_output, 'input': json_list_input}

    dict_res_path = os.path.join('res/api_live_res', f'{case_name}_results_collected.json')

    # Auto-closes the json file
    with open(dict_res_path, 'w', encoding='utf-8') as f:
        json.dump(selected_results_dict, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    main()
