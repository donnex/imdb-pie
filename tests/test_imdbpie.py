from nose.tools import assert_false, assert_true, assert_equal
from imdbpie import Imdb, Movie


class TestImdb(object):
    @classmethod
    def setup_class(cls):
        cls.imdb = Imdb()

    def test_search(self):
        results = self.imdb.find_by_title('batman')
        assert_true(len(results) > 150)

    def test_popular_movie_first(self):
        results = self.imdb.find_by_title('batman')
        assert_equal(results[0]['imdb_id'], 'tt0096895')

    def test_search_with_spaces(self):
        results = self.imdb.find_by_title('the truman show')
        assert_true(len(results) > 1)

    def test_search_with_no_match(self):
        results = self.imdb.find_by_title('asdasasdasdasdadas')
        assert_true(len(results) == 0)

    def test_search_for_id(self):
        results = self.imdb.find_movie_by_id('tt0382932')
        assert_true(isinstance(results, Movie))

    def test_top250(self):
        movies = self.imdb.top_250()
        assert_equal(len(movies), 250)

    def test_popular_shows(self):
        shows = self.imdb.popular_shows()
        assert_equal(len(shows), 50)

    def test_find_imdb_id_from_string(self):
        assert_equal(Imdb.find_imdb_id('asd www.imdb.com/title/tt0499549/ asdad'), 'tt0499549')
        assert_equal(Imdb.find_imdb_id('tt0499549'), 'tt0499549')
        assert_equal(Imdb.find_imdb_id('text tt0499549 text'), 'tt0499549')
        assert_false(self.imdb.find_imdb_id('asd'))


class TestMovie(object):
    @classmethod
    def setup_class(cls):
        cls.imdb = Imdb()

    def test_movie_attributes(self):
        movie = self.imdb.find_movie_by_id('tt0382932')
        assert_equal(movie.title, 'Ratatouille')
        assert_equal(movie.imdb_id, 'tt0382932')
        assert_equal(movie.tagline, 'Dinner is served... Summer 2007')
        assert_equal(movie.plot_outline, 'With dreams of becoming a chef, a culinary genius in the form of a rat, makes an unusual alliance with a young kitchen worker at a famed restaurant.')
        assert_equal(movie.runtime, '111 min')
        assert_equal(movie.year, 2007)
        assert_equal(movie.rating, 8)
        assert_true(len(movie.genres) > 1)
        assert_equal(movie.imdb_url, 'http://www.imdb.com/title/tt0382932/')
        assert_true('.jpg' in movie.poster_url)
        assert_true('.jpg' in movie.cover_url)
        assert_equal(movie.release_date, '2007-06-29')
        assert_equal(movie.certification, 'G')
        assert_true(movie.votes > 20000)
        assert_true(len(movie.directors) > 0)
        assert_true(len(movie.actors) > 0)
        assert_true(len(movie.writers) > 0)

    def test_movie_trailer_img_url(self):
        movie = self.imdb.find_movie_by_id('tt1210166')
        assert_true('http://ia.media-imdb.com/images/' in
                                                    movie.trailer_img_url)


class TestPerson(object):
    @classmethod
    def setup_class(cls):
        cls.imdb = Imdb()

    def test_person_attributes(self):
        movie = self.imdb.find_movie_by_id('tt0382932')
        assert_equal(movie.actors[0].name, 'Brad Garrett')
        assert_equal(movie.actors[0].role, 'Gusteau')
        assert_equal(movie.directors[0].name, 'Brad Bird')
        assert_equal(movie.directors[0].role, None)
        assert_equal(movie.writers[0].name, 'Brad Bird')
        assert_equal(movie.writers[0].role, None)
