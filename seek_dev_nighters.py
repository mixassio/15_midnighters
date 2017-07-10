import requests
from pytz import timezone
from datetime import datetime

END_NIGHT = 5  # night is over in 5:00


def load_attempts():
    page = 1
    while True:
        payload = {'page': page}
        url = 'https://devman.org/api/challenges/solution_attempts/'
        response = requests.get(url, params=payload)
        if not response.ok:
            break
        users = response.json()
        for list_users in users['records']:
            yield {
                'username': list_users['username'],
                'timestamp': list_users['timestamp'],
                'timezone': list_users['timezone']
            }
        page += 1


def check_midnighters(user_info):
    tz = user_info['timezone']
    if user_info['timestamp'] is not None:
        server_time = datetime.fromtimestamp(user_info['timestamp'])
        client_time = timezone(tz).fromutc(server_time)
        if client_time.hour < END_NIGHT:
            return True


def print_midnighters(list_users):
    midnighters = {}
    for user_info in list_users:
        if check_midnighters(user_info):
            midnighters[user_info['username']] = True
    for user in midnighters.keys():
        print(user)


if __name__ == '__main__':
    list_users = load_attempts()
    print_midnighters(list_users)
