"""Configuration of the app."""

import os


class Configuration(object):
    APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
    DEBUG = True
    SECRET_KEY = 'this is a really bad key' # todo: better key
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/data.db' % APPLICATION_DIR
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # unnecessary and memory hog
