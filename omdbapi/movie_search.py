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
        print(self.api_keys)

    api_keys: str
    values: dict = field(default_factory=dict)

    def get_movie(self, title, year=None, kind=None, plot=None):
        """
        Get all data movie.
        :param title: movie title to search
        :param year: year the movie was released
        :param kind: movie, series or episode
        :param plot: by default return short plot
        :Example:
        movie.get_movie(title='Interstellar', plot='full')
        """

        # 需要多个key 轮换使用，因为每个key一天只有1000次查询配额
        api_key = self.api_keys[random.randint(0, len(self.api_keys) - 1)]

        url = 'http://www.omdbapi.com/'
        payload = {'t': title, 'y': year, 'type': kind, 'plot': plot, 'r': 'json', 'apikey': api_key}
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
        items = {item.lower(): self.values.get(item.lower(), 'key not found!') for item in args}

        return items


if __name__ == '__main__':
    # 从环境变量读取 APIKEY_OMDB
    import os
    api_keys = os.environ.get('APIKEY_OMDB')
    movie = GetMovie(api_keys=api_keys)
    movie.get_movie(title='Interstellar', year='2014')
    print(movie.values)
    print(movie.get_data('Director', 'Actors'))