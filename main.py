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
import logging
import os
import webapp2
import jinja2
import google.appengine.api.mail as mail
from google.appengine.ext import ndb
from datetime import datetime

JINJA_ENVIRONMENT = jinja2.Environment(
      loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
      extensions=['jinja2.ext.autoescape'],
      autoescape=True)

"""
Blog writing how-to:

1. Write a html file with content which extends abstract-blog.html.
2. Write a html file with content to be used as a blerd.
3. Add a BlogPost to blogPosts with the appropriate args.

"""

class BlogPost:
  def __init__(self, title, blerbPath, articleId, articlePath, imagePath=None):
    self.title = title
    self.blerbPath = blerbPath
    self.articleId = articleId
    self.articlePath = articlePath
    self.imagePath = imagePath

blogPosts = [
  BlogPost("Origin Story", "b01-originstory-blerb.html", "origin_story", "b01-originstory.html"),
  BlogPost("What is Say Penis?", "b00-what-blerb.html", "wtf", "b00-what.html")]

def findBlog(articleId):
  for blog in blogPosts:
    if blog.articleId == articleId:
      return blog
  return None

class AlphaRequest(ndb.Model):
  email = ndb.StringProperty()
  request_time = ndb.DateTimeProperty()

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

class AlphaTestHandler(webapp2.RequestHandler):
  def get(self):
    template = JINJA_ENVIRONMENT.get_template('alpha-test.html')
    self.response.write(template.render({"success":False}))
  
  def post(self):
    template = JINJA_ENVIRONMENT.get_template('alpha-test.html')
    email = self.request.get('email')
    try:
      mail.check_email_valid(email, 'email')
      alphaRequest = AlphaRequest(id=email)
      alphaRequest.email = email
      alphaRequest.request_time = datetime.now()
      alphaRequest.put()
      self.response.write(template.render({"success":True, "email":email}))
    except:
      self.response.write(template.render({"success":False, "email":email}))

class BlogHandler(webapp2.RequestHandler):
  def get(self, url):
    blog = findBlog(url)
    template = JINJA_ENVIRONMENT.get_template('no_blog.html')
    if blog:
      template = JINJA_ENVIRONMENT.get_template(blog.articlePath)
    self.response.write(template.render({}))

class BaseBlogHandler(webapp2.RequestHandler):
  def get(self):
    template = JINJA_ENVIRONMENT.get_template('blog_base.html')
    self.response.write(template.render({"blogs":blogPosts}))

class CareerHandler(webapp2.RequestHandler):
  def get(self):
    template = JINJA_ENVIRONMENT.get_template('careers.html')
    self.response.write(template.render({}))   

class FourOhFourHandler(webapp2.RequestHandler):
  def get(self, url):
    template = JINJA_ENVIRONMENT.get_template('four_oh_four.html')
    self.response.write(template.render({"error_message":"Doesn't look like \
      there's anything here."}))
  def post(self, url):
    template = JINJA_ENVIRONMENT.get_template('four_oh_four.html')
    self.response.write(template.render({"error_message":"Doesn't look like \
      there's anything here."}))   

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/l/([a-z|0-9]{6})', ListenHandler),
    ('/l/(.*)', InvalidShareHandler),
    ('/blog', BaseBlogHandler),
    ('/blog/(.*)', BlogHandler),
    ('/careers', CareerHandler),
    ('/alpha', AlphaTestHandler),
    ('/(.*)', FourOhFourHandler)
], debug=True)
