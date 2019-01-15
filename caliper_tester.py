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

is_openlrw = False
lrw_server = "http://lti.tools"
lrw_endpoint = f"{lrw_server}/caliper/event?key=python-caliper"

# Get these from your LRW (if necessary)

token = "python-caliper"

if (is_openlrw):
    auth_data = {'username':'a601fd34-9f86-49ad-81dd-2b83dbee522b', 'password':'e4dff262-1583-4974-8d21-bff043db34d5'}
    r = requests.post(f"{lrw_access}", json = auth_data, headers={'X-Requested-With': 'XMLHttpRequest'})
    token = r.json().get('token')

the_config = caliper.HttpOptions(
      host=f"{lrw_endpoint}",
      auth_scheme='Bearer',
      api_key=token)

# Here you build your sensor; it will have one client in its registry,
# with the key 'default'.
the_sensor = caliper.build_sensor_from_config(
        sensor_id = f"{lrw_server}/test_caliper",
        config_options = the_config )

# Here, you will have caliper entity representations of the various
# learning objects and entities in your wider system, and you provide
# them into the constructor for the event that has just happened.
#
# Note that you don't have to pass an action into the constructor because
# the NavigationEvent only supports one action, part of the
# Caliper base profile: caliper.constants.BASE_PROFILE_ACTIONS['NAVIGATED_TO']
#

actor = caliper.entities.Person(id="test")
organization = caliper.entities.Organization(id="test")
edApp = caliper.entities.SoftwareApplication(id="test")
resource = caliper.entities.DigitalResource(id="test")

the_event = caliper.events.NavigationEvent(
        actor = actor,
        edApp = edApp,
        group = organization,
        object = resource,
        eventTime = datetime.now().isoformat(),
        action = "NavigatedTo"
         )

# Once built, you can use your sensor to describe one or more often used
# entities; suppose for example, you'll be sending a number of events
# that all have the same actor

ret = the_sensor.describe(the_event.actor)

print (the_event)
# The return structure from the sensor will be a dictionary of lists: each
# item in the dictionary has a key corresponding to a client key,
# so ret['default'] fetches back the list of URIs of all the @ids of
# the fully described Caliper objects you have sent with that describe call.
#
# Now you can use this list with event sendings to send only the identifiers
# of already-described entities, and not their full forms:
#print(the_sensor.send(the_event, described_objects=ret['default'])

# You can also just send the event in its full form, with all fleshed out
# entities:
print(the_sensor.send(the_event))

print ("Event sent!")
