import json
import requests


class Notifier:

    ENDPOINT = 'https://api.pushbullet.com/v2/pushes'

    def __init__(self):
        self.__token = 'o.sp3pA6LfFHgeFZlVKSjrNviwnevqAVXX'

    def send_notification(self, title, body):
        content = {"type": "note", "title": title, "body": body}

        response = requests.post(Notifier.ENDPOINT, data=json.dumps(content),
                                 headers={'Access-Token': self.__token,
                                          'Content-Type': 'application/json'})

        if response.status_code != 200:
            print('Oops...Something went wrong...')
        else:
            print('Success! Notification sent!')
