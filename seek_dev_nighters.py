import requests
from pytz import timezone
from datetime import datetime


def load_attempts():
    devman_api = requests.get('https://devman.org/api/challenges/solution_attempts/?page=1')
    devman_content = devman_api.json()
    pages = int(devman_content['number_of_pages'])
    for page in range(1, pages+1):
        devman_api = requests.get('https://devman.org/api/challenges/solution_attempts/?page={}'.format(page))
        devman_content = devman_api.json()
        for list_users in devman_content['records']:
            yield {
            'username': list_users['username'],
            'timestamp': list_users['timestamp'],
            'timezone': list_users['timezone']
        }


def get_midnighters(user_info):
    tz = user_info['timezone']
    if user_info['timestamp'] is not None:
        server_time = datetime.fromtimestamp(user_info['timestamp'])
        client_time = timezone(tz).fromutc(server_time)
        if client_time.hour < 5:
            return True


if __name__ == '__main__':
    list_users = load_attempts()
    set_midnighters = set()
    for user_info in list_users:
        if get_midnighters(user_info):
            set_midnighters.add(user_info['username'])
    for user in set_midnighters:
        print(user)
