from bs4 import BeautifulSoup
import requests

BASE_URL = 'http://dontpad.com'

class DontPad:
    def __init__(self, path):
        self.path = path
        self.url = '/'.join([BASE_URL, path])
        self._session = requests.Session()

    def _update(self):
        response = self._session.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        self._text = soup.textarea.text
        self._last_update = soup.input.value

    def get_text(self):
        self._update()
        return (self._text)

    def get_zip(self, file):
        pass

    def set_text(self, text):
        self._update()
        post_data = {
            'text': text, 
            'lastUpdate': self._last_update
            }
        requests.post(self.url, data=post_data)        

    def append_text(self, text):
        self._update()
        self.set_text(self._text+text)


def main():
    jurandy = DontPad('jurandy')
    print('The current text is:\n' + jurandy.get_text())
    jurandy.set_text('I works!')
    jurandy.append_text('\nAnd it should work for ever and ever.')
    print('The updated text now is:\n' + jurandy.get_text())

if __name__ == '__main__':
    main()

