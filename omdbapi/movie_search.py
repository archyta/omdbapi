from . import GetMovie

if __name__ == '__main__':
    # 从环境变量读取 APIKEY_OMDB
    import os
    api_keys = os.environ.get('APIKEY_OMDB')
    movie = GetMovie(api_keys=api_keys)
    movie.get_movie(title='Interstellar', year='2014')
    print(movie.values)
    print(movie.get_data('Director', 'Actors'))