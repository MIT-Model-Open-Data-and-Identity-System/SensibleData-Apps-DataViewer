import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ROOT_DIR = '/home/arks/sensibledtu_DEVEL/SensibleData-Apps-DataViewer/data_viewer/'
ROOT_URL = '/devel/apps/data_viewer/'
BASE_URL = "https://54.229.13.160/"
APPLICATION_URL = BASE_URL[:-1] + ROOT_URL
SENSIBLE_PREFIX = '/sensible/'
SENSIBLE_URL = APPLICATION_URL[:-1] + SENSIBLE_PREFIX

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
		'NAME': ROOT_DIR+'SECURE_data.db',                      # Or path to database file if using sqlite3.
	}
}

#import uuid, hashlib
#str(hashlib.sha256(str(uuid.uuid4())).hexdigest())
SECRET_KEY = 'fdskljk3o990e8f9kjfdslkjgkskgfk394ikrkjwe'
