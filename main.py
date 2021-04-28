import os
import asyncio
import aiohttp
import argparse

from static.constants import BASE_URL, TAIL_URL
from static.constants import FIRST_WORDS, SUB_FIRST_WORDS, TOP_K
from lib.token_refresh import *
from lib.parsing import *
from lib.email_utility import *
import yaml 

def fetch_dummy_posts():
    research_posts, tutorial_posts, tooling_posts, others_posts = get_dummy_posts()
    # print(research_posts)
    sendmail(research_posts, tutorial_posts, tooling_posts, others_posts, "Weekly My Personal Newsletter")

def get_dummy_posts():
    research_posts = []
    tutorial_posts = []
    tooling_posts = []
    others_posts = []

    messages = []
    links = []
    categories = []
    authors = []

    with open('dummy.yaml') as f:
        docs = yaml.load_all(f, Loader=yaml.FullLoader)

        for doc in docs:
            for k, v in doc.items():
                if k == "messages":
                    messages = v
                elif k == "links":
                    links = v
                elif k == "authors":
                    authors = v
                elif k == "categories":
                    categories = v

    for i in range(len(categories)):
        post = FacebookPost()
        post.message = messages[i][:SUB_FIRST_WORDS] + " ..."
        post.link = links[i]
        post.author = authors[i]

        if categories[i] == "research":
            research_posts.append(post)
        elif categories[i] == "tutorial":
            tutorial_posts.append(post)
        elif categories[i] == "tooling":
            tooling_posts.append(post)
        elif categories[i] == "others":
            others_posts.append(post)

    return research_posts, tutorial_posts, tooling_posts, others_posts


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='Please specify the range of dates and the number of posts to be collected')
    # parser.add_argument('--since', required=True, type=str, help='dates in YYYY-MM-DD') 
    # parser.add_argument('--until', required=True, type=str, help='dates in YYYY-MM-DD')
    # parser.add_argument('--email-title', required=True, type=str, help='title for the email')
    # parser.add_argument('--limit', required=False, type=int, default=300, help='number of posts to scrap')
    # parser.add_argument('--weight-reactions', required=False, type=float, default=1.0, help='from 0 to 1')
    # parser.add_argument('--weight-shares', required=False, type=float, default=1.0, help='from 0 to 1')
    # parser.add_argument('--weight-comments', required=False, type=float, default=1.0, help='from 0 to 1')
    # args = parser.parse_args()

    # access_token = update_token()
    load_dotenv()
    fetch_dummy_posts()

    # URL = f"{BASE_URL}&limit={args.limit}&since={args.since}&until={args.until}&{TAIL_URL}&access_token={access_token}"

    # asyncio.run(fetch_posts(URL, 
    #                         args.weight_reactions, 
    #                         args.weight_shares, 
    #                         args.weight_comments,
    #                         args.email_title,
    #                         args.since,
    #                         args.until))



