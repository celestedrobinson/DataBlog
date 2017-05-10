from flask import Flask
from flask import render_template
from flask import request
import json
import requests
import urllib.parse
import urllib.request


app = Flask(__name__)

@app.route("/about")
def about():
    """
    This shouldn't need much modification here, just leads to the about me page.
    """
    return render_template("about.html")


@app.contact("/contact")
def contact():
    """
    Leads to the contact me page
    """
    return render_template("contact.html")


@app.route("/posts")
def posts():
    """
    This will have all my posts. Right now I haven't added any. Expect to see some interesting
    content soon.
    """
    return render_template("posts.html")

@app.route("/")
def home():
    """
    Right now this is sparse, because I don't need a lot. In the future, this will be more
    interesting.
    """
    return render_template("blog_home.html")


if __name__ == '__main__':
    app.run(port=5000, debug=True)