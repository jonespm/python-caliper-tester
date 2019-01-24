# -*- coding: future_fstrings -*-

"""
 For this to work you need to first install the package at
  https://github.com/IMSGlobal/caliper-python
 This can either use for testing 
  - OpenLRW 
  - http://lti.tools/caliper/event?key=python-caliper 
"""

from __future__ import unicode_literals
import caliper
import requests, json, sys, os, logging

from datetime import datetime
from dotenv import load_dotenv

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()

# Add this path first so it picks up the newest changes without having to rebuild
this_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, this_dir + "/..")
load_dotenv(dotenv_path=this_dir + "/.env")

# Configuration is for OpenLRW, obtain bearer token

lrw_type = os.getenv('LRW_TYPE',"").lower()
token = os.getenv('TOKEN',"")
lrw_server = os.getenv('LRW_SERVER', "")

lrw_access = ""

if lrw_type == 'unizin':
    lrw_endpoint = f"{lrw_server}"
elif lrw_type == 'ltitools':
    lrw_endpoint = f"{lrw_server}/caliper/event?key={token}"
elif lrw_type == 'openlrw':
    lrw_access = f"{lrw_server}/api/auth/login"
    lrw_endpoint = f"{lrw_server}/api/caliper"
    auth_data = {'username':'a601fd34-9f86-49ad-81dd-2b83dbee522b', 'password':'e4dff262-1583-4974-8d21-bff043db34d5'}
    r = requests.post(f"{lrw_access}", json = auth_data, headers={'X-Requested-With': 'XMLHttpRequest'})
    token = r.json().get('token')
else:
    sys.exit(f"LRW Type {lrw_type} not supported")

the_config = caliper.HttpOptions(
    host=f"{lrw_endpoint}",
    auth_scheme='Bearer',
    api_key=token, 
    debug=True)

# Here you build your sensor; it will have one client in its registry,
# with the key 'default'.
the_sensor = caliper.build_simple_sensor(
        sensor_id = f"runestone",
        config_options = the_config )

actor = caliper.entities.Person(id="test")
organization = caliper.entities.Organization(id="test")
edApp = caliper.entities.SoftwareApplication(id="runestone")
resource = caliper.entities.DigitalResource(id="test")

now = datetime.utcnow()
event_time = now.strftime('%Y-%m-%dT%H:%M:%S') + now.strftime('.%f')[:4] + 'Z'
the_event = caliper.events.ViewEvent(
        actor = actor,
        edApp = edApp,
        group = organization,
        object = resource,
        eventTime = event_time,
        # This is optional since it only supports one action but we'll pass it anyway
        action = "Viewed"
         )

# Once built, you can use your sensor to describe one or more often used
# entities; suppose for example, you'll be sending a number of events
# that all have the same actor

logger.info(dir(the_event))
logger.info(the_sensor.send(the_event))

logger.info (the_sensor.status_code)
logger.info (the_sensor.debug)