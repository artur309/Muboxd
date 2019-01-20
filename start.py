import json

from mubi import MUBI
from letterboxd import Letterboxd

if __name__ == "__main__":
    with open('credentials.json') as f:
        data = json.load(f)
    mubi = MUBI(data['MUBI'])
    movie_list, director_list, year = mubi.get_movies()
    ltxd = Letterboxd(data['Letterboxd'])
    ltxd.add_movies_to_playlist(data['playlist'], movie_list, director_list, year)