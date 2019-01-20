import requests
import json
from bs4 import BeautifulSoup
from time import sleep

class Letterboxd:

    def __init__(self, userinfo):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 Vivaldi/2.2.1388.37'
        })
        self._log_in(userinfo)

    def _log_in(self, userinfo):
        url = 'https://letterboxd.com/'
        self.session.get(url)
        self.session.cookies.update(self.session.cookies.get_dict())
        data = {
            '__csrf': self.session.cookies.get_dict().get('com.xk72.webparts.csrf'),
            'username': userinfo['username'],
            'password': userinfo['password']
        }
        self.session.post('https://letterboxd.com/user/login.do', data=data)
        self.session.cookies.update(self.session.cookies.get_dict())
    
    def add_movies_to_playlist(self, playlist_link, movie_list, director_list, year):
        # fetch playlist data
        response = self.session.get(playlist_link)
        self.session.cookies.update(self.session.cookies.get_dict())
        soup = BeautifulSoup(response.text, 'html.parser')
        list_id = soup.find('input', attrs={'name': 'filmListId'}).get('value')
        list_name = soup.find('input', attrs={'name': 'name'}).get('value')
        list_desc = soup.find('textarea', attrs={'name': 'notes'}).string
        list_public = 'true' if soup.find('input', attrs={'name': 'publicList'}).get('checked') == 'checked' else 'false'

        formdata = {
            '__csrf': self.session.cookies.get_dict().get('com.xk72.webparts.csrf'),
            'filmListId': list_id,
            'name': list_name,
            'tags': '',
            'notes': list_desc,
            'entries': json.dumps([])
        }
        self.session.cookies.update(self.session.cookies.get_dict())
        self.session.post('https://letterboxd.com/s/save-list', data=formdata)

        formdata.update({'publicList': list_public})

        entries = []

        for movie in zip(movie_list, director_list, year):
            params = {
                'q': movie[0],
                'limit': '100'
            }
            r = self.session.get('https://letterboxd.com/s/autocompletefilm', params=params)
            js = r.json()
            if not js['result']:
                continue
            ranked = []
            counter = 0
            for data in js['data']:
                counter += 1
                point = 2
                if data['directors'] and data['directors'][0]['name'] == movie[1]:
                    point -= 1
                if 'releaseYear' in data and data['releaseYear'] == movie[2]:
                    point -= 1
                if point == 0:
                    self.session.get(f"https://letterboxd.com/ajax/film:{data['id']}/filmlistentry")
                    entries.append({"filmId": str(data['id'])})
                    break
                else:
                    ranked.append((data['id'], point, counter))
            else:
                ranked.sort(key=lambda x: (x[1], x[2]))
                self.session.get(f"https://letterboxd.com/ajax/film:{ranked[0][0]}/filmlistentry")
                entries.append({"filmId": str(ranked[0][0])})

        formdata['entries'] = json.dumps(entries)
        self.session.cookies.update(self.session.cookies.get_dict())
        self.session.post('https://letterboxd.com/s/save-list', data=formdata)

if __name__ == "__main__":
    import json
    with open('credentials.json') as f:
        data = json.load(f)

    ltxd = Letterboxd(data['Letterboxd'])