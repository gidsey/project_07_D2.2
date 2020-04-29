from project_7.settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
    '.herokuapp.com',
    '127.0.0.1',
]

SECRET_KEY = get_env_variable("SECRET_KEY")