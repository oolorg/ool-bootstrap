import os
import sys

sys.path.append('/usr/lib/ool-test')
sys.path.append('/usr/lib/ool-test/bootstrap')
sys.path.append('/usr/lib/ool-test/bootstrap/web')
sys.path.append('/usr/lib/ool-test/bootstrap/web/cgi-bin')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
