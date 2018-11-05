from bs4 import BeautifulSoup
import requests
import os.path
import tempfile
import time

BASE_URL = 'http://dontpad.com'

class DontPad:
    def __init__(self, path):
        self.path = path if path.endswith('/') else path+'/'
        self.url = '/'.join([BASE_URL, self.path])
        self._session = requests.Session()

    def _update(self):
        response = self._session.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        self._text = soup.textarea.text
        self._last_update = soup.input.value

    def get_text(self):
        self._update()
        return (self._text)

    def get_zip(self, folder=''):
        if not folder or not os.path.exists(folder):
            folder = tempfile.gettempdir()
        zip_path = self.path[:-1]+'.zip'
        zip_url = self.url[:-1]+'.zip'
        zip_fname = os.path.basename(zip_path)
        response = self._session.get(zip_url)
        destiny = os.path.join(folder, zip_fname)
        with open(destiny, 'bw') as zip_file:
            zip_file.write(response.content)
        return destiny

    def set_text(self, text, append=False):
        self._update()
        post_data = {
            'text': self._text+text if append else text, 
            'lastUpdate': self._last_update
            }
        requests.post(self.url, data=post_data)        

    def append_text(self, text):
        self.set_text(self._text+text, append=True)

    def get_subfolders(self):
        return []


def test():
    jurandy = DontPad('jurandy')
    print('The current text is:\n' + jurandy.get_text())
    time.sleep(1)
    jurandy.set_text('It works!')
    time.sleep(1)
    jurandy.append_text('\nAnd it should work while dontpad uses the same form fields.')
    time.sleep(1)
    print('The updated text now is:\n' + jurandy.get_text())

if __name__ == '__main__':
    test()

