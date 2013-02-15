import json
import time
import requests
from urllib import urlencode
import hashlib
import re

BASE_URI = 'app.imdb.com'
API_KEY = '2wex6aeu6a8q9e49k7sfvufd6rhh0n'
SHA1_KEY = hashlib.sha1(API_KEY).hexdigest()


class Imdb(object):
    def __init__(self, anonymize=False):
        self.base_uri = BASE_URI
        self.sha1_key = SHA1_KEY

        if anonymize:
            self.base_uri = ('youtubeproxy.org/default.aspx'
                             '?prx=https://{0}').format(self.base_uri)

    def build_url(self, path, params):
        default_params = {'api': 'v1',
                          'appid': 'iphone1_1',
                          'apiPolicy': 'app1_1',
                          'apiKey': self.sha1_key,
                          'locale': 'en_US',
                          'timestamp': int(time.time())}

        query_params = dict(default_params.items() + params.items())
        query_params = urlencode(query_params)
        return 'https://{0}{1}?{2}'.format(self.base_uri, path, query_params)

    def find_movie_by_id(self, imdb_id):
        url = self.build_url('/title/maindetails', {'tconst': imdb_id})
        result = self.get(url)
        movie = Movie(**result['data'])
        return movie

    def find_by_title(self, title):
        default_find_by_title_params = {'json': '1',
                                        'nr': 1,
                                        'tt': 'on',
                                        'q': title}
        query_params = urlencode(default_find_by_title_params)
        results = self.get(('http://www.imdb.com/'
                            'xml/find?{0}').format(query_params))

        keys = ['title_popular',
                'title_exact',
                'title_approx',
                'title_substring']
        movie_results = []

        # Loop through all results and build a list with popular matches first
        for key in keys:
            if key in results:
                for r in results[key]:
                    year = None
                    year_match = re.search(r'(\d{4})', r['title_description'])
                    if year_match:
                        year = year_match.group(0)

                    movie_match = {
                        'title': r['title'],
                        'year': year,
                        'imdb_id': r['id']
                    }
                    movie_results.append(movie_match)

        return movie_results

    def top_250(self):
        url = self.build_url('/chart/top', {})
        result = self.get(url)
        return result['data']['list']['list']

    def popular_shows(self):
        url = self.build_url('/chart/tv', {})
        result = self.get(url)
        return result['data']['list']

    def get(self, url):
        r = requests.get(url, headers={'User-Agent':
                                ('Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_1 '
                                 'like Mac OS X; en-us) AppleWebKit/532.9 '
                                 '(KHTML, like Gecko) Version/4.0.5 '
                                 'Mobile/8B5097d Safari/6531.22.7')})
        return json.loads(r.text)

    @staticmethod
    def find_imdb_id(text):
        imdb_id_match = re.search(r'/tt(\d{2,})', text)
        if not imdb_id_match:
            return False
        else:
            return 'tt{0}'.format(imdb_id_match.group(1))


class Person(object):
    def __init__(self, **kwargs):
        p = kwargs['name']

        self.name = p.get('name')
        self.imdb_id = p.get('nconst')
        self.role = kwargs.get('char')

    def __repr__(self):
        return '<Person: {0} ({1})>'.format(self.name, self.imdb_id)


class Movie(object):
    def __init__(self, **kwargs):
        self.imdb_id = kwargs.get('tconst')
        self.title = kwargs.get('title')
        self.year = int(kwargs.get('year'))
        self.tagline = kwargs.get('tagline')
        self.rating = kwargs.get('rating')
        self.genres = kwargs.get('genres')
        self.votes = kwargs.get('num_votes')
        self.imdb_url = 'http://www.imdb.com/title/{0}/'.format(self.imdb_id)

        self.plot_outline = None
        if 'plot' in kwargs and 'outline' in kwargs['plot']:
            self.plot_outline = kwargs['plot']['outline']

        self.runtime = None
        if 'runtime' in kwargs:
            self.runtime = '{0} min'.format(
                str(int((kwargs['runtime']['time'] / 60))))

        self.poster_url = None
        if 'image' in kwargs and 'url' in kwargs['image']:
            self.poster_url = kwargs['image']['url']

        self.cover_url = None
        if 'image' in kwargs and 'url' in kwargs['image']:
            self.cover_url = '{}_SX214_.jpg'.format(
                                kwargs['image']['url'].replace('.jpg', ''))

        self.release_date = None
        if 'release_date' in kwargs and 'normal' in kwargs['release_date']:
            self.release_date = kwargs['release_date']['normal']

        self.certification = None
        if 'certificate' in kwargs and 'certificate' in kwargs['certificate']:
            self.certification = kwargs['certificate']['certificate']

        self.trailer_img_url = None
        if ('trailer' in kwargs and 'slates' in kwargs['trailer'] and
                kwargs['trailer']['slates']):
            self.trailer_img_url = kwargs['trailer']['slates'][0]['url']

        # Directors
        self.directors = []
        if kwargs.get('directors_summary'):
            for director in kwargs['directors_summary']:
                self.directors.append(Person(**director))

        # Actors
        self.actors = []
        if kwargs.get('cast_summary'):
            for cast in kwargs['cast_summary']:
                self.actors.append(Person(**cast))

        # Writers
        self.writers = []
        if kwargs.get('writers_summary'):
            for writer in kwargs['writers_summary']:
                self.writers.append(Person(**writer))

        # Trailers
        self.trailers = {}
        if 'trailer' in kwargs and 'encodings' in kwargs['trailer']:
            for k, v in kwargs['trailer']['encodings'].items():
                self.trailers[v['format']] = v['url']

    def __repr__(self):
        return '<Movie: {0} ({1}) ({2})>'.format(self.title,
                                                 self.year,
                                                 self.imdb_id)
