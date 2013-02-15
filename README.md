# ImdbPie

Python IMDB client using the IMDB json web service made available for their iOS app.

## How To Use

### Create an instance of ImdbPie

    imdb = Imdb()
    imdb = Imdb(anonymize=True}) # to proxy requests

### Search for a movie by title

    imdb.find_by_title('The Dark Knight') => [{'year': u'2008', 'imdb_id': u'tt0468569', 'title': u'The Dark Knight'}, {'year': u'2012', 'imdb_id': u'tt1345836', 'title': u'The Dark Knight Rises'}, ...}]

### Find a movie by its imdb_id

    movie = imdb.find_movie_by_id('tt0468569')

    movie.title => 'The Dark Knight'
    movie.rating => 8.1
    movie.certification => 'PG-13'
    movie.votes => 895890
    movie.cover_url => 'http://ia.media-imdb.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1__SX214_.jpg'

### Find a movie trailer poster

    movie = imdb.find_movie_by_id('tt1210166')
    movie.trailer_img_url => 'http://ia.media-imdb.com/images/M/MV5BODM1NDMxMTI3M15BMl5BanBnXkFtZTcwMDAzODY1Ng@@._V1_.jpg'

### Find the top 250 movies ever

    imdb.top_250() => [{'title': 'The Shawshank Redemption', 'year': '1994', 'type': 'feature', 'rating': 9.3,...}, ...]


### Get the current popular shows

    imdb.popular_shows() => [{'title' : 'Glee', 'year' : '2009', 'imdb_id' => 'tt1327801'}, {'title' : 'Dexter', ...}]

## Requirements

    1. Python 2.7
    2. Python requests module - http://python-requests.org

## Tests

    Tests in tests dir, requires nosetests - https://nose.readthedocs.org/en/latest/
