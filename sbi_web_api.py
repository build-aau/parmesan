import requests
import json
import base64
import time
import random


DIRECTORY_URL = 'https://swa-dir-a.buildsrv.dk'


def get_a_job_server(target, user_type):
    res = requests.get(DIRECTORY_URL).json()

    assert res['version'] == 1

    alternatives = list()
    for srv in res['job_queues']:
        if target in srv['supported_targets'] and user_type in srv['allowed_users']:
            alternatives.append(srv)

    assert len(alternatives) > 0
    return random.choice(alternatives)['url']


def ping(job_queue_url):
    res = requests.get(f'{job_queue_url}/v1/ping').text
    assert res == 'pong'
    return res


def login(job_queue_url, username, password):
    data = {
        'username': username,
        'password': password,
    }
    json_data = json.dumps(data)
    res = requests.post(f'{job_queue_url}/v1/login', json_data)
    data = json.loads(res.text)
    return data


def new_job(job_queue_url, token, job_data):
    auth_headers = {
        'Session': token,
    }
    res = requests.post(f'{job_queue_url}/v1/jobs', json=job_data, headers=auth_headers)
    data = json.loads(res.text)
    return data


def job_status(job_queue_url, token, job_id):
    auth_headers = {
        'Session': token,
    }
    res = requests.get(f'{job_queue_url}/v1/jobs/{job_id}', headers=auth_headers)
    return res.json()


def job_delete(job_queue_url, token, job_id):
    auth_headers = {
        'Session': token,
    }
    res = requests.get(f'{job_queue_url}/v1/jobs/{job_id}', headers=auth_headers)
    return res.json()


def get_job_output(job_queue_url, token, job_id):
    auth_headers = {
        'Session': token,
    }
    res = requests.get(f'{job_queue_url}/v1/jobs/{job_id}/output', headers=auth_headers)
    return res.json()


def send_job(input_path, output_path, username, password):
    """

    :param input_path:
    :param output_path:
    :param username: Contact BUILD, Aalborg University
    :param password: Contact BUILD, Aalborg University
    :return:
    """
    print('Preparing conf_data:')
    with open(input_path, 'r', encoding='utf-8') as f:
        input_json = f.read()
    target = 'lcabyg5_calc'
    user_group = 'Test'
    job_data = {
        'priority': 0,
        'job_target': target,
        'job_target_min_ver': '',
        'job_target_max_ver': '',
        'job_arguments': '',
        'input_blob': base64.standard_b64encode(input_json.encode('utf-8')).decode('utf-8'),
    }
    print()

    print('Finding a server:')
    job_queue_url = get_a_job_server(target, user_group)
    print(f'job_queue_url = {job_queue_url}')
    print()

    print('Sending ping:')
    res_ping = ping(job_queue_url)
    print(f'res_ping = {res_ping}')
    print()

    print('Logging in:')
    token = login(job_queue_url, username, password)
    print(f'token = {token}')
    print()

    print('Submitting a new job:')
    job_id = new_job(job_queue_url, token, job_data)
    print(f'job_id = {job_id}')
    print()

    print('Waiting for the job to finish:')
    done = False
    while not done:
        status = job_status(job_queue_url, token, job_id)
        print(f'status = {status["status"]}')
        done = (status['status'] == 'Ready') or (status['status'] == 'Failed')
        time.sleep(1)
    print()

    print('Download the results:')
    job_output_raw = get_job_output(job_queue_url, token, job_id)
    job_output = base64.b64decode(job_output_raw).decode('utf-8')
    print()

    print('Saving the results to disk:')
    data = json.loads(job_output)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print()

    print('Done')


#def main():
def sbi_web_api():
    username = 'YOUR USERNAME'
    password = 'PASSWORD'

    input_json = 'example_project.json'
    output_json = 'output.json'

    send_job(input_json, output_json, username, password)


#if __name__ == '__main__':
    #main()
