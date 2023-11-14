__version__ = '0.7.0'

import re
from dataclasses import dataclass, field
import random

import requests


class GetMovieException(Exception):
    """GetMovie Exception"""


@dataclass
class GetMovie:
    """
    instantiate the class, passing api key.

    :param api_keys: ombdapi keys

    :Example:
    movie = GetMovie(api_key='your api key')
    """
    def __post_init__(self):
        if not isinstance(self.api_keys, str):
            raise GetMovieException('API key must be string!')
        self.api_keys = self.api_keys.split(',')
        # print(self.api_keys)

    api_keys: str
    values: dict = field(default_factory=dict)

    def get_movie(self, title, year=None, kind='movie', plot=None, season=None, episode=None):
        """
        Get all data movie.
        :param title: movie title to search
        :param year: year the movie was released
        :param kind: movie, series or episode
        :param plot: by default return short plot
        :param season: season number, optional
        :param episode: episode number, optional if season is provided
        :Example:
        movie.get_movie(title='Interstellar', plot='full')
        """

        # 需要多个key 轮换使用，因为每个key一天只有1000次查询配额
        api_key = self.api_keys[random.randint(0, len(self.api_keys) - 1)]

        url = 'http://www.omdbapi.com/'
        # if title is imdbid like tt\d{7,8}, then use i=imdbid
        if re.match(r'^tt\d{7,8}$', title):
            payload = {'i': title,  'r': 'json', 'apikey': api_key}
        else:
            payload = {'t': title, 'type': kind, 'r': 'json', 'apikey': api_key}
        if year:
            payload['y'] = year
        if plot:
            payload['plot'] = plot  # full, short
        if season:
            payload['Season'] = season
            if episode:
                payload['Episode'] = episode
        print(payload)
        result = requests.get(url, params=payload).json()

        if result.pop('Response') == 'False':
            raise GetMovieException(result['Error'])

        self.values.clear()
        for key, value in result.items():
            key = key.lower()
            setattr(self, key, value)
            self.values[key] = value

        return self.values

    def get_data(self, *args):
        """
        Get values passing keys as parameter.

        :param *args: items data key

        :Example:
        movie.get_data('Director', 'Actors')
        """
        items = {item.lower(): self.values.get(item.lower(), f'key:{item} not found!') for item in args}

        return items

