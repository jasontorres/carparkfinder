#!/usr/bin/env python

import os
import cgi
import logging
import datetime

from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import util 
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from django.utils import simplejson

import models
from geo import geotypes

from geo.geomodel import GeoModel


from models import Location

class MainHandler(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()

    if user:
      
      path = os.path.join(os.path.dirname(__file__), 'index.html')
      self.response.out.write(template.render(path, {}))

    else:
        self.redirect(users.create_login_url(self.request.uri))

class LocationHandler(webapp.RequestHandler):
  def post(self):

    location = Location()

    logging.info(self.request.get('data'))

    data = simplejson.loads(self.request.get('data'))

    logging.info(data)

    if users.get_current_user():
      location.author = users.get_current_user()
      location.title = data['title']
      location.address = data['address']
      location.city =  data['city']
      location.state =  data['region']
      location.location= data['lat'] + "," + data['lng']
      #location.location = "14.584892,121.05747"
      location.put()

      self.response.out.write('OK')

  def get(self):
    _lng = cgi.escape(self.request.get('lng'))
    _lat = cgi.escape(self.request.get('lat'))
    _distance = 5

    center = geotypes.Point(float('14.550102'),
        float('121.056186'))

    #14.553803,121.050244

    #results = Location.proximity_fetch(Location.all(), center, max_results=10, max_distance=100000000)
  
    results = Location.all()

    public_attrs = Location.public_attributes()

    results_obj = [r.to_dict() for r in results]

    self.response.out.write(simplejson.dumps({
      'status': 'success',
      'results': results_obj
    }))


def main():
  application = webapp.WSGIApplication([('/', MainHandler), ('/locations', LocationHandler)],
                                       debug=True)
  util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
