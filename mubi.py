import requests
from bs4 import BeautifulSoup
from time import sleep

from utils import EmptyCatalogueException

class MUBI:

    def __init__(self, cookie):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 Vivaldi/2.2.1388.37'
        })
        self.session.cookies.update(cookie)

    def _parse(self, htmlresponse):
        soup = BeautifulSoup(htmlresponse, 'html.parser')
        ls = soup.find_all('h2', class_='full-width-tile__title')
        if not ls:
            raise EmptyCatalogueException('Empty Catalogue')
        movies_list = [soup.find('h2', class_='showing-page-hero-tile__title').string]
        director_list = []
        year = []
        for h2 in ls:
            movies_list.append(h2.string)
        
        ls = soup.find_all('h3', class_='now-showing-tile-director-year')
        for h3 in ls:
            span = h3.find_all('span', itemprop='name')
            director_list.append(span[0].string)

        ls = soup.find_all('span', class_='now-showing-tile-director-year__year-country')
        for span in ls:
            year.append(span.string.split()[-1])

        return movies_list, director_list, year

    def get_movies(self):
        url = 'https://mubi.com/showing'
        movies_list = []        
        for _ in range(5):
            try:
                r = self.session.get(url)
                movies_list, director_list, year = self._parse(r.text)
            except EmptyCatalogueException:
                sleep(1)
            else:
                return movies_list, director_list, year
        else:
            return [], [], []

if __name__ == "__main__":
    import json
    with open('credentials.json') as f:
        data = json.load(f)

    mubi = MUBI(data['MUBI'])
    movie_list, director_list, year = mubi.get_movies()
    for i in zip(movie_list,director_list, year):
        print(i)