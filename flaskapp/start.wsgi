import os, sys

PROJECT_DIR = '/groups/w209dv22sec6g1/flaskapp'

activate_this = '/groups/w209dv22sec6g1/flaskapp/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

sys.path.append(PROJECT_DIR)

from flaskapp import app as application
