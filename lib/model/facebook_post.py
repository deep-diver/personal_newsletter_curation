from __future__ import annotations

from datetime import datetime, timezone
import pytz
import markdown2 
from typing import Dict, List

class FacebookPost(object):
    """
    글(Post)를 나타냅니다.
    """

    id          : str
    message     : str
    numbers     : Dict[str, int] # reaction, comment, share
    link        : str
    front_image : str
    created_time: datetime
    author      : str

    @staticmethod
    def convert_message(message_json) -> str:
        result = message_json.get("message", "")
        
        if result.strip() == "":
            print(message_json)
            if attachments := message_json.get("attachments"):
                for attachment in attachments.get("data"):
                    description = attachment.get("description", "")
                    if description != "": 
                        result = description
                        break
        
        if result == "":
            return None

        return result

    @staticmethod
    def get_time(message_json, tz) -> datetime:
        utc_time = datetime.strptime(message_json.get("created_time"), "%Y-%m-%dT%H:%M:%S%z")
        tz_converted_time = FacebookPost.convert_timezone_from_utc_to(utc_time, tz)
        return tz_converted_time.strftime("%Y-%m-%d %H:%M")

    @staticmethod
    def convert_timezone_from_utc_to(utc_time, tz) -> str:
        return utc_time.replace(tzinfo=timezone.utc).astimezone(tz=pytz.timezone(tz))

    @classmethod
    def from_json(cls, message_json: dict) -> FacebookPost:
        post = FacebookPost()

        post.created_time   = FacebookPost.get_time(message_json, "Asia/Seoul")

        if message := FacebookPost.convert_message(message_json):
            post.message = message
        else:
            return None 

        post.id             = message_json.get("id")
        post.link           = message_json.get("permalink_url")

        post.numbers = {}
        post.numbers["reaction"]    = message_json.get("reactions").get("summary").get("total_count")
        post.numbers["share"]       = message_json.get("shares").get("count") if "shares" in message_json else 0
        post.numbers["comment"]     = message_json.get("comments").get("summary").get("total_count")

        post.attachments = []
        if attachments := message_json.get("attachments"):
            for attachment in attachments.get("data"):
                if image := attachment.get("media").get("image"):
                    post.attachments.append(image.get("src"))

        post.front_image = post.attachments[0] if len(post.attachments) > 0 else "https://github.com/deep-diver/fb-group-post-fetcher/blob/master/static/images/no-image.png?raw=true"

        return post

    def __repr__(self) -> str:
        return f"FB_POST(message={self.message}, link={self.link}, author={self.author})"
