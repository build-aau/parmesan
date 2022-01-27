import json
import matplotlib.pyplot as plt

def main():
    """
    Simple plot that compares the total impact of several configurations.
    The indicator, and year can be modified in line 20.

    :return:
    """

    print('loading...')

    with open('res/api_live_res/case2_results_collected.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    res_dict = {} # dict()
    for conf in data:
        for node in data[conf]['output']['model']:
            if node['node_type'] == 'Building':
                id_building = node['id']
                res = data[conf]['output']['results'][id_building]['Sum']['9999']['GWP']

                print(res)
                res_dict[conf] = res
                break

    names = list(res_dict.keys())
    values = list(res_dict.values())
    plt.bar(range(len(res_dict)), values, tick_label=names)
    plt.title('Sum_GWP for configurations')
    plt.ylabel('Sum_GWP [kg CO2-eq]')
    plt.show()

if __name__ == '__main__':
    main()