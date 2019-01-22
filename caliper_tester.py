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
import requests, json, sys

from datetime import datetime

# Configuration is for OpenLRW, obtain bearer token

# For OPENLRW
#lrw_server = "http://localhost:9966"
#lrw_access = f"{lrw_server}/api/auth/login"
#lrw_endpoint = f"{lrw_server}/api/caliper"

# For Unizin
#lrw_server = "https://umich.caliper.dev.cloud.unizin.org"
#lrw_access = ""
#lrw_endpoint = f"{lrw_server}"
#token = ""

is_openlrw = False

lrw_server = "http://lti.tools"
# Not needed for test server
lrw_access = ""
lrw_endpoint = f"{lrw_server}/caliper/event?key=python-caliper"
token = "python-caliper"

# This is needed to get a token from the access point
if (is_openlrw):
    auth_data = {'username':'a601fd34-9f86-49ad-81dd-2b83dbee522b', 'password':'e4dff262-1583-4974-8d21-bff043db34d5'}
    r = requests.post(f"{lrw_access}", json = auth_data, headers={'X-Requested-With': 'XMLHttpRequest'})
    token = r.json().get('token')

the_config = caliper.HttpOptions(
      host=f"{lrw_endpoint}",
      auth_scheme='Bearer',
      api_key=token, 
      debug=False)

# Here you build your sensor; it will have one client in its registry,
# with the key 'default'.
the_sensor = caliper.build_sensor_from_config(
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

print (dir(the_event))
# The return structure from the sensor will be a dictionary of lists: each
# item in the dictionary has a key corresponding to a client key,
# so ret['default'] fetches back the list of URIs of all the @ids of
# the fully described Caliper objects you have sent with that describe call.
#
# Now you can use this list with event sendings to send only the identifiers
# of already-described entities, and not their full forms:
#print(the_sensor.send(the_event, described_objects=ret['default'])

# You can also just send the event in iten full form, with all fleshed out
# entities:
print(the_sensor.send(the_event))

for k, client in the_sensor.client_registry.items():
        for debug in client.debug:
                print ("Client {0} last status {1} {2} ".format(client.apiKey, debug.status_code, debug.text))