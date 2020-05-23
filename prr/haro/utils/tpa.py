# Third party APIs 
import logging
import json
import sys 
import mailslurp_client
import os

from mailslurp_client.rest import ApiException

# Logging
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def get_email_content_from_mailslurp(email_id, configuration):
    with mailslurp_client.ApiClient(configuration) as api_client:
        api_instance = mailslurp_client.EmailControllerApi(api_client)
        decode = False
        api_response = None
        try:
            api_response = api_instance.get_email_html(email_id, decode=decode)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling EmailControllerApi->get_email_html: %s\n" % e)
            raise ValueError("Unable to retrieve email content")

def write_to_airtable(airtable, records):
    for record in records:
        try:
            airtable.insert(record)
        except:
            logging.error("Unable to write record - " + json.dumps(record))

