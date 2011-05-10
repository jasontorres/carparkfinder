from google.appengine.ext import db
from geo.geomodel import GeoModel

class Location(GeoModel):
  author = db.UserProperty()
  content = db.StringProperty(multiline=True)
  title = db.StringProperty()
  address = db.StringProperty()
  city = db.StringProperty()
  province = db.StringProperty()
  country = db.StringProperty()
  zip_code = db.StringProperty()
  date = db.DateTimeProperty(auto_now_add=True)

  @staticmethod
  def public_attributes():
    return [
      'content', 'title', 'address', 'city', 'province', 'country',
      'zip_code', 'date', 'author', 'location'
    ]

  def _get_latitude(self):
    return self.location.lat if self.location else None

  def _set_latitude(self, lat):
    if not self.location:
      self.location = db.GeoPt()
    self.location.lat = lat

  latitude = property(_get_latitude, _set_latitude)

  def _get_longitude(self):
    return self.location.lon if self.location else None

  def _set_longitude(self, lon):
    if not self.location:
      self.location = db.GeoPt()

    self.location.lon = lon

  longitude = property(_get_longitude, _set_longitude)

  def to_dict(self):
     return dict([(p, unicode(getattr(self, p))) for p in self.public_attributes()])


