"""
Backend code for robinsonbrain.com
"""
from flask import Flask
from flask import render_template, request, redirect, url_for
from config import blog_posts, datasets
from random import choice
import json
import os
import platform
import requests
import steam_finder
import urllib.parse
import urllib.request


app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for('error_page'))

@app.route("/kmeans_vis", methods=['POST', 'GET'])
def kmeans_vis():

    # Get the dataset

    return render_template("kmeans_vis.html",
                           datasets=datasets,
                           cluster_range=[i for i in range(3, 20)])

@app.route("/error")
def error_page():
    return render_template('page_not_found.html'), 404

@app.route("/about")
def about():
    """
    This shouldn't need much modification here, just leads to the about me page.
    """
    return render_template("about.html")


@app.route("/contact")
def contact():
    """
    Leads to the contact me page
    """
    return render_template("contact.html")


@app.route("/posts")
def posts():
    """
    This will have all my posts. This should be dynamic so as I increase the amount
    of posts, they will be on multiple pages.
    """
    return render_template("posts.html",
                           blog_posts=blog_posts)


@app.route("/helpmesteam", methods=['POST', 'GET'])
def help_me_decide():
    steamid = request.args.get('steamid')
    number_of_suggestions = request.args.get('suggestions')
    if steamid and number_of_suggestions:
        if int(number_of_suggestions) > 9 or int(number_of_suggestions) < 1:
            number_of_suggestions = "9"
        games = steam_finder.get_random_game(steamid, int(number_of_suggestions))
    else:
        games = {}
    return render_template("helpmesteam.html",
                           games=games)


@app.route("/post/<post_id>")
def blog_post(post_id):
    """
    Returns the specified blog post that we are interested in reading.
    """
    if platform.system() == 'Linux':
        path = os.path.abspath(os.path.join("DataBlog", "static", "posts", "{}.html".format(post_id)
                                           ))
    else:
        path = os.path.abspath(os.path.join("static", "posts", "{}.html".format(post_id)))
    try:
        html = open(path, encoding="utf-8").read()
    except FileNotFoundError:
        return redirect(url_for('error_page'))
    return render_template("default_post.html",
                           content=html)


@app.route("/")
def home():
    """
    Right now this is sparse, because I don't need a lot. In the future, this will be more
    interesting.
    """
    return render_template("blog_home.html")


if __name__ == '__main__':
    app.run(port=5000, debug=True)
