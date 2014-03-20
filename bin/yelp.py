#!/usr/bin/env python
#
# Copyright 2011-2014 Splunk, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


# python yelp.py __EXECUTE__ 'location="New York"'

import sys
import time
from splunklib.searchcommands import \
    dispatch, GeneratingCommand, Configuration, Option, validators

import requests
import oauth2
import json
import urllib

@Configuration(retainsevents=False)
class YelpCommand(GeneratingCommand):
    location = Option(
        doc='''
        **Syntax:** **location=***<location>*
        **Description:** Location to search for businesses''',
        require=True)

    term = Option(
        doc='''
        **Syntax:** **term=***<term>*
        **Description:** Type of business''',
        require=False)

    category = Option(
        doc='''
        **Syntax:** **category=***<category>*
        **Description:** Delimitted list of categories''',
        require=False)

    sort = Option(
        doc='''
        **Syntax:** **sort=***<sort>*
        **Description:** Sort mode: 0=Best matched (default), 1=Distance, 2=Highest Rated''',
        require=False, validate=validators.Integer(), default=1)

    limit = Option(
        doc='''
        **Syntax:** **limit=***<limit>*
        **Description:** Number of records to return''',
        require=False, validate=validators.Integer())

    offset = Option(
        doc='''
        **Syntax:** **offset=***<offset>*
        **Description:** Offset the list of returned business results by this amount''',
        require=False, validate=validators.Integer())

    def generate(self):
        config = self.get_configuration()
        url = self.get_yelp_signed_url(
            config['consumer-key'],
            config['consumer-secret'],
            config['token'],
            config['token-secret'])
        
        response = requests.get(url)
        
        if response.status_code != 200:
            print response.text
            return
        
        result = response.json()
        
        timestamp = time.time()
        for result in results["businesses"]:
            yield self.getEvent(result, timestamp)

    def getEvent(self, result, timestamp):
        event = {"_time": timestamp, "name": result["name"], "rating":result["rating"], 
            "address": " ".join(result["location"]["address"]), 
            "city": result["location"]["city"], "state": result["location"]["state_code"], 
            "zip": result["location"]["postal_code"], "neighborhoods": "", "url": result["url"]}

        if "neighborhoods" in result["location"]:
            event["neighborhoods"] = ", ".join(result["location"]["neighborhoods"])

        event["_raw"] = json.dumps(result)

        return event

    def get_configuration(self):
        config_file = open('./config.json')
        return json.load(config_file)

    def get_yelp_signed_url(self, consumer_key, consumer_secret, token,
                       token_secret):
        url_params = {}

        url_params['location'] = self.location

        if self.category is not None:
            url_params['category_filter'] = self.category
        
        if self.term is not None:
            url_params['term'] = self.term

        if self.limit is not None:
            url_params['limit'] = self.limit

        if self.offset is not None:
            url_params['offset'] = self.offset

        """Returns response for API request."""
        # Unsigned URL
        encoded_params = ''
        if url_params:
            encoded_params = urllib.urlencode(url_params)
        url = 'http://api.yelp.com/v2/search?%s' % (encoded_params)

        # Sign the URL
        consumer = oauth2.Consumer(consumer_key, consumer_secret)
        oauth_request = oauth2.Request('GET', url, {})
        oauth_request.update({'oauth_nonce': oauth2.generate_nonce(),
                              'oauth_timestamp': oauth2.generate_timestamp(),
                              'oauth_token': token,
                              'oauth_consumer_key': consumer_key})

        token = oauth2.Token(token, token_secret)
        oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer,
                                   token)
        signed_url = oauth_request.to_url()
        return signed_url


dispatch(YelpCommand, sys.argv, sys.stdin, sys.stdout, __name__)
