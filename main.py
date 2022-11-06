from flask import Flask, render_template, url_for
from data import queries
import math
from dotenv import load_dotenv

load_dotenv()
app = Flask('codecool_series')

LIMIT = 15
SHOWN_PAGE_NUMBERS = 5


@app.route('/')
def index():
    genres = queries.get_show_genres()
    genres_names = queries.get_genres_names()
    shows = queries.get_shows()
    return render_template('index.html', shows=shows, genres=genres,
                           genres_names=genres_names)


@app.route('/shows/<show_id>')
def show_show(show_id):
    show = queries.get_show_by_id(show_id)
    actors = queries.get_show_actors(show_id)
    seasons = queries.get_seasons_by_show_id(show_id)
    video_id = show["trailer"].split("=")[1]
    return render_template('single_show.html', show=show, actors=actors, video_id=video_id,
                           seasons=seasons)


@app.route('/shows/most-rated')
def most_rated_shows():
    page_number = 1
    all_shows = queries.get_shows()
    all_pages = count_pages(all_shows)
    shown_pages_start, shown_pages_end = get_shown_pages(page_number, all_pages)
    genres = queries.get_show_genres()
    genres_names = queries.get_genres_names()
    shows = queries.get_shows_ordered_by('rating', "DESC", LIMIT, 0)
    return render_template('index.html', shows=shows, genres=genres,
                           genres_names=genres_names, all_shows=all_shows,
                           page_number=page_number, shown_pages_end=shown_pages_end,
                           shown_pages_start=shown_pages_start)


@app.route('/shows/most-rated/<page_number>')
def most_rated_shows_by_page_number(page_number: int):
    page_number = int(page_number)
    all_shows = queries.get_shows()
    all_pages = count_pages(all_shows)
    shown_pages_start, shown_pages_end = get_shown_pages(page_number, all_pages)
    offset = LIMIT * (page_number - 1)
    genres = queries.get_show_genres()
    genres_names = queries.get_genres_names()
    shows = queries.get_shows_ordered_by('rating', "DESC", LIMIT, offset)
    return render_template('index.html', shows=shows, genres=genres,
                           genres_names=genres_names, shown_pages_start=shown_pages_start,
                           page_number=page_number, shown_pages_end=shown_pages_end)


def count_pages(data):
    all_pages = math.ceil(len(data) / 15)
    return all_pages


def get_shown_pages(page_number, all_pages):
    shown_pages_start = int(page_number - ((SHOWN_PAGE_NUMBERS - 1) / 2))
    shown_pages_end = int(page_number + ((SHOWN_PAGE_NUMBERS - 1) / 2))
    if shown_pages_start < 1:
        shown_pages_start = 1
        shown_pages_end = SHOWN_PAGE_NUMBERS
    elif shown_pages_end > all_pages:
        shown_pages_start = all_pages - SHOWN_PAGE_NUMBERS + 1
        shown_pages_end = all_pages
    return shown_pages_start, shown_pages_end


@app.route('/design')
def design():
    return render_template('design.html')


def main():
    app.run(debug=False)


if __name__ == '__main__':
    main()
