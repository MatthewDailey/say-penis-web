#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
      loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
      extensions=['jinja2.ext.autoescape'],
      autoescape=True)

class MainHandler(webapp2.RequestHandler):
  def get(self):
    template = JINJA_ENVIRONMENT.get_template('index.html')
    self.response.write(template.render({}))


class ListenHandler(webapp2.RequestHandler):
  def get(self, shareId):
    template = JINJA_ENVIRONMENT.get_template('listen.html')
    self.response.write(template.render({'code':shareId}))

class InvalidShareHandler(webapp2.RequestHandler):
  def get(self, url):
    template = JINJA_ENVIRONMENT.get_template('four_oh_four.html')
    self.response.write(template.render({"error_message":"The code '" + url +\
       "' is not a valid penis code. Once you have a valid penis code, enter \
       it in the android app to listen."}))


class FourOhFourHandler(webapp2.RequestHandler):
  def get(self, url):
    template = JINJA_ENVIRONMENT.get_template('four_oh_four.html')
    self.response.write(template.render({"error_message":"Doesn't look like \
      there's anything here."}))

      

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/l/([a-z|0-9]{6})', ListenHandler),
    ('/l/(.*)', InvalidShareHandler),
    ('/(.*)', FourOhFourHandler)
], debug=True)
