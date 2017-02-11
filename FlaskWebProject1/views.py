"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from FlaskWebProject1 import app
import ocr
import xml.etree.ElementTree as ET

@app.route('/')
def root():
    """Renders the root page."""
    return render_template(
        'index.html',
        title='SilverTongue',
        year=datetime.now().year,
    )

@app.route('/home')
def home():
    """Renders the home page."""
    wordList = ocr.getForeignWords()
    top = ET.Element("div")
    print(ET.tostring(top))
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
        words=ET.tostring(top),
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Meet the Team',
        year=datetime.now().year,
        message=''
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message=''
    )

@app.route('/tryit')
def tryit():
    """Renders the try it page."""
    return render_template(
        'tryit.html',
        title='Learn',
        year=datetime.now().year,
    )
@app.route('/results')
def results():
    import silvertongue
    """Renders the Results page."""
    return render_template(
        'results.html',
        title='Results',
        year=datetime.now().year,
    )
