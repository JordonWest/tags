import sys
from os.path import join
sys.path.insert(1, sys.path[0])
from config import load_config, app_init
from datetime import datetime
from IPython import embed
from flask import request, redirect, render_template, g

app = app_init(__name__)

from tag import Tag # After app_init(), which sets db for the model

cfg = load_config(join(app.root_path, '../shared/config.yml'))

@app.route('/', methods=['GET'])
def show_tags():

    g.setdefault('image', cfg['awesome_image']) # Flask.g: a way to pass var to a template
    #embed()
    # Note tags=Tag.all() ... another way to pass var to a Jinja2 template
    tags = Tag.all()
    tags_html = '\n'.join(list(map(lambda x: "<a href=\"/tags/%s\">%s</a><br>" % (x.name, x.name), tags)))
    form_html = "<form action=\"/tags\" method=\"POST\"><label>Enter a tag: </label><input name=\"tag-name\"></form>"
    return render_template('index.html', tags=Tag.all())

@app.route('/about', methods=['GET'])
def about():
    return '<h1>The Ultimate Tag Manager</h1><a href=\"/\">Home</a> <a href=\"/about\">About</a><h1>A Uniquely World-Changing Super-Proprietary Way of Managing Tags</h1><p>This is the only website ever designed that has at least one of the properties common to every other website ever designed.</p><p>A highly respected source has said, "I\'d rather use this site than use one of the best sites in the world!"'


@app.route('/tags', methods=['POST'])
def add_tag():
    new_tag = request.form['tag-name']
    tag = Tag.where('tag', new_tag).first()
    if tag is None:
        tag = Tag.create(name=new_tag)

    return redirect('/')

# GET is not the recommended way to implement DELETE, but oh well...
@app.route('/tags/<tag>', methods=['GET'])
def remove_tag(tag):
    tag_to_remove = Tag.where('name', tag).first()
    if tag_to_remove is not None:
        tag_to_remove.delete()

    return redirect('/')
