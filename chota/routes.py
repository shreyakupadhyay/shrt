from chota import app, db
from flask import render_template, redirect, request, flash, jsonify
import string
import random
import re
import httplib2
from urlparse import urlparse
import json


class Url(db.Model):
    """
    Class for creating models via SQLAlchemy
    """
    __tablename__ = "Url"
    id = db.Column('url_id', db.Integer, primary_key=True)
    random_code = db.Column(db.String(80), unique=True)
    url = db.Column(db.String(120), unique=False)

    def __init__(self, random_code, url):
        self.random_code = random_code
        self.url = url

    def __repr__(self):
        return '<url %r>' % self.url


def _protocol(url):
    """
    Checks if http:// is present before Url
    """
    parsed = urlparse(url)
    if parsed.scheme == "":
        return "http://"+url
    else:
        return url


def _is_valid_url(url):
    """
    Validates the URL input
    """
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?'
        r'|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if regex.search(url):
        return True
    return False


def _url_exists(url):
    """
    Get the headers of a web resource to check if it exists
    """
    h = httplib2.Http()
    try:
        resp = h.request(url, 'HEAD')
        if resp[0].status == 200:
            return True
    except (httplib2.RelativeURIError, httplib2.ServerNotFoundError):
        return False


def _random_string():
    """
    Generates a random code for adding to short url
    """
    length = 6
    rv = ""
    for i in range(length):
        rv += random.choice(string.ascii_lowercase)
    return rv


def _shorten_url(url):
    """
    Functions returns short url
    """
    url = _protocol(url.strip())
    if _url_exists(url):
        long_url = Url.query.filter_by(url=url).first()
        #Checks if someone has already shortened the same url
        if long_url is None:
            random_code = _random_string()
            short_url = Url(random_code, url)
            db.session.add(short_url)
            db.session.commit()
            return "http://chota-tk.herokuapp.com/" + random_code
        else:
            #If the url is present in the db, it returns the already created
            #short url
            return "http://chota-tk.herokuapp.com/" + long_url.random_code
    else:
        return False


def _expand_url(code):
    """
    Returns expanded url
    """
    long_url = Url.query.filter_by(random_code=code).first()
    #Checks if the short url is valid
    if long_url is None:
        return False
    else:
        return long_url.url


@app.route('/', methods=["GET"])
def main():
    return render_template('index.html')


@app.route('/', methods=["POST"])
def api():
    data = None
    if request.json:
        data = request.json
    else:
        return jsonify(success=False, message='Please provide JSON Data')

    try:
        data = json.loads(request.data)
    except ValueError:
        return jsonify(success=False, message='Could not parse json.')

    long_url = data.get('long_url')
    long_url = _protocol(long_url)
    short_url = _shorten_url(long_url)
    return jsonify(success=True, short_url=short_url)


@app.route('/form', methods=["POST"])
def form():
    url = request.form['url']
    short_url = _shorten_url(url)
    if not short_url:
        flash("invalid url, try again")
        return render_template("index.html")
    else:
        return render_template('shortened.html', url=short_url)


@app.errorhandler(404)
def handle_error():
    """
    404 error handler function
    """
    return render_template("404.html")


@app.route('/<string:handler>', methods=["GET"])
def handle_url(handler=None):
    """
    Function to return short url's to original url
    """
    long_url = _expand_url(handler)
    if not long_url:
        return redirect('/', code=302)
    else:
        return redirect(long_url, code=302)
