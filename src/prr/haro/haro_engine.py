import logging
import sys
import mailslurp_client
import os 

from utils.tpa import get_email_content_from_mailslurp, write_to_airtable
from utils.response_generator import parse_email_for_categories, get_stories_from_reporters
from airtable import Airtable

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Setup airtable
PRR_BASE_ID="app26blbVX3rcmY5p"
HARO_TABLE="leads"
airtable = Airtable(PRR_BASE_ID, HARO_TABLE)

# Setup email client
configuration = mailslurp_client.Configuration()
configuration.api_key['x-api-key'] = os.getenv('MAILSLURP_API_KEY')

def convert_haro_email_to_records():
    # Retrieve stories to pitch
    email_id= '67fd1c5b-53ab-4840-804d-95ab2d8df5a1'
    api_response = get_email_content_from_mailslurp(email_id, configuration)
    categories = parse_email_for_categories(api_response)
    stories = get_stories_from_reporters(categories)

    # Write to airtable
    tpa.write_to_airtable(airtable, stories)
    logger.info("Completed inserting records into Airtable")
