# Third party APIs 

import bs4
import logging
import sys

from bs4 import BeautifulSoup

# Logging
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def parse_email_for_categories(api_response):
    soup = BeautifulSoup(api_response, 'lxml')
    soup.find_all('h4')
    blocks = soup.find_all('h4')

    categories = {}
    for block in blocks:
        all_tags = []
        for tag in block.next_siblings:
            if tag.name == "h4":
                break
            else:
                all_tags.append(tag)
        categories[block.text] = all_tags
    return categories

def get_stories_from_reporters(categories):
    stories = []
    story = None
    final_category = None
    for category in categories:
        if "***" not in category:
            final_category = category
            for each_block in categories[category]:
                if isinstance(each_block, bs4.element.NavigableString):
                    if "Summary" in each_block.string:
                        summary = each_block.string.split("Summary: ")[1]
                        if story is not None:
                            story["category"] = category
                            stories.append(story)
                            story = None
                        story = {"summary": summary}
                    if "Media Outlet" in each_block.string:
                        media_outlet = each_block.string.split("Media Outlet: ")[1]
                        story["media_outlet"] = media_outlet   
                    if "Deadline" in each_block.string:
                        deadline = each_block.string.split("Deadline: ")[1].split("-")
                        deadline_date = deadline[1]
                        deadline_time = deadline[0]
                        story["deadline_date"] = deadline_date
                        story["deadline_time"] = deadline_time
                    if "12051 Indian Creek Ct., Beltsville, MD 20705, USA" in each_block.string:
                        break
                if isinstance(each_block, bs4.element.Tag):
                    if each_block.name == 'p':
                        if "Name: " in each_block.text:
                            story["name"] = each_block.text.split("Name: ")[1] 
                        if "Query specifics:" in each_block.text:
                            story["query_specifics"] = each_block.text.split("Query specifics: ")[1] 
                        if "Query:" in each_block.text:
                            story["query"] = each_block.text.split("Query: ")[1] 
                        if "Requirements" in each_block.text:
                            story["requirements"] = each_block.text.split("Requirements: ")[1]
                    if each_block.name == 'a':
                        if "target" in each_block.attrs:
                            story["email"] = each_block.attrs['href']
    story["category"] = final_category
    if story is not None:
        stories.append(story)
    return stories