from __future__ import with_statement
import sys
sys.path.insert(0, 'libs')
import os
import io
import cgi
import jinja2
import urllib
import urllib2
import webapp2
from models import *
from lib.allegro_api import allegro_api
from lib.nokaut_api import nokaut_api
from google.appengine.api import files
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.api import images


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])


def counter(items):
    """Function for getting 3 most popular products"""
    all_items = []
    tmp = []
    for i in items:
        if i in tmp:
            pass
        else:
            all_items.append((items.count(i), i))
            tmp.append(i)
    all_items = sorted(all_items)
    all_items.reverse()
    return [item for item in all_items[:3]]


class HTMLRequestHandler(webapp2.RequestHandler):
    """Class for get template"""
    def __init__(self, *args, **kwargs):
        webapp2.RequestHandler.__init__(self, *args, **kwargs)

    def render_template(self, template_file, template_values=None):
        """ Function for render template"""
        template = JINJA_ENVIRONMENT.get_template(template_file)
        self.response.write(template.render(template_values))


class History(HTMLRequestHandler):
    """View for history"""
    def post(self):
        """Post function"""
        name = users.get_current_user()
        history = Searched.all().filter('author', name).order("-date")
        my_history = [[his.content, his.date, his.url] for his in history]
        template_values = {"my_history": my_history}

        self.render_template(
            'templates/history.html', template_values=template_values)


class MainPage(HTMLRequestHandler):
    """Main view"""
    def get_most_popular(self, item_counter):
        items = []
        for i in item_counter:
            items.append(Searched.all().filter('content', i[1]).fetch(1)[0])

        item_imgs = [o.blob_allegro for o in items]
        imgs = [images.get_serving_url(blob) for blob in item_imgs]
        img_mini = ["".join([img, "=s100"]) for img in imgs]
        urls = [o.url for o in items]
        return zip(imgs, img_mini, urls)

    def get(self):
        """Get function"""
        if users.get_current_user():
            user_name = users.get_current_user().nickname()
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            user_name = "anonymous"
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        items = Searched.all().order("-date")
        all_items = [item.content for item in items]
        item_counter = counter(all_items)

        template_values = {
            "item_counter": self.get_most_popular(item_counter),
            'url': url,
            'url_linktext': url_linktext,
            'value_urllib': urllib.urlencode({'user_name': user_name}),
            'value_form2': cgi.escape(user_name),
            'upload_url': blobstore.create_upload_url('/upload'),
            'searched': Searched.all()
        }

        self.render_template(
            'templates/index.html', template_values=template_values)


def make_blob_key(image_url):
    """Function for make blob key for picture"""
    file_name = files.blobstore.create(mime_type='application/octet-stream')
    response_url = urllib2.urlopen(image_url)
    image_file = io.BytesIO(response_url.read())
    binary_img = image_file.read()

    with files.open(file_name, 'a') as file:
        file.write(binary_img)

    files.finalize(file_name)
    blob_key = files.blobstore.get_blob_key(file_name)
    return blob_key


class Results(HTMLRequestHandler):
    """Result view"""
    def post(self):
        """Post function"""
        user_name = users.get_current_user() and users.get_current_user()\
            .nickname() or 'anonymous'
        sended = Searched(parent=user_key(user_name))

        if users.get_current_user():
            sended.author = users.get_current_user()

        keyword = cgi.escape(self.request.get('keyword'))
        keyword = keyword.split()[0]

        allegro_price = allegro_api(keyword)[0]
        nokaut_price = nokaut_api(
            keyword, 'a8839b1180ea00fa1cf7c6b74ca01bb5')[0]
        allegro_url = allegro_api(keyword)[1]
        nokaut_url = nokaut_api(
            keyword, 'a8839b1180ea00fa1cf7c6b74ca01bb5')[1]
        allegro_image_url = allegro_api(keyword)[2]
        nokaut_image_url = nokaut_api(
            keyword, 'a8839b1180ea00fa1cf7c6b74ca01bb5')[2]

        if allegro_price < nokaut_price:
            url = allegro_url
        else:
            url = nokaut_url

        blob_key_allegro = make_blob_key(allegro_image_url)
        blob_key_nokaut = make_blob_key(nokaut_image_url)
        img_nokaut = images.get_serving_url(blob_key_nokaut)
        img_allegro = images.get_serving_url(blob_key_allegro)
        img_mini_allegro = "".join([img_allegro, "=s100"])
        img_mini_nokaut = "".join([img_nokaut, "=s100"])

        sended.blob_allegro = blob_key_allegro
        sended.blob_nokaut = blob_key_nokaut
        sended.url = url
        sended.content = keyword
        sended.put()

        template_values = {
            "allegro_url": allegro_url,
            "allegro_price": allegro_price,
            "nokaut_url": nokaut_url,
            "nokaut_price": nokaut_price,
            "prod_name": cgi.escape(self.request.get('content')),
            "img_nokaut": img_nokaut,
            "img_allegro": img_allegro,
            "img_mini_allegro": img_mini_allegro,
            "img_mini_nokaut": img_mini_nokaut
        }
        self.render_template(
            'templates/resoult.html', template_values=template_values
        )
