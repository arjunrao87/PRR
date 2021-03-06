import logging
import sys
import mailslurp_client
import os 

from airtable import Airtable
from prr.haro.utils.tpa import get_email_content_from_mailslurp, write_to_airtable
from prr.haro.utils.response_generator import parse_email_for_categories, get_stories_from_reporters

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Setup airtable
airtable = Airtable(os.getenv('AIRTABLE_PRR_BASE'), os.getenv('AIRTABLE_HARO'))

# Setup email client
configuration = mailslurp_client.Configuration()
configuration.api_key['x-api-key'] = os.getenv('MAILSLURP_API_KEY')

def convert_haro_email_to_records(email_id: str):
    # Retrieve stories to pitch
    api_response = get_email_content_from_mailslurp(email_id, configuration)
    categories = parse_email_for_categories(api_response)
    stories = get_stories_from_reporters(categories)

    # Write to airtable
    write_to_airtable(airtable, stories)
    logger.info("Completed inserting records into Airtable")
    return "Finished parsing email"
