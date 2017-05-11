from flask import Flask
from flask import render_template
from flask import request
import json
import requests
import urllib.parse
import urllib.request


app = Flask(__name__)


blog_posts = [{'title': "Finding Their Party: Using Clustering to Find Patterns in Data",
               'address':
               "http://robinsonbrain.blogspot.com/2017/04/finding-their-party-using-voting-to.html",
               'date': '4/27/2017',
               'description': 'Using voting data from Utah\'s House of Representatives, I describe'\
               'how the K-Means algorithm work. Complete with cool, interactive visualizations of'\
               'the algorithm during each step, as well as a cute dog picture. Links to code are'\
               'provided.'},
              {'title': "Who's Utah's 'Yes Man?': Data Insights into Utah's House of "\
               "Representatives 2017",
               'address':
               "http://robinsonbrain.blogspot.com/2017/02/grouping-members-of-utahs-house-of.html",
               'date': '2/19/2017',
               'description': 'Ever curious about who votes like your representative in Utah\'s '\
               'House of Representatives? I collect and analyze voting data to find out '\
               'interesting patterns in the data.'}
             ]

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

@app.route("/")
def home():
    """
    Right now this is sparse, because I don't need a lot. In the future, this will be more
    interesting.
    """
    return render_template("blog_home.html")


if __name__ == '__main__':
    app.run(port=5000, debug=True)
