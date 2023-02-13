from datetime import datetime
from typing import NamedTuple


# represents one post on a forum entry
# loaded using https://github.com/seanbreckenridge/autotui
class Post(NamedTuple):
    dt: datetime
    post_title: str
    post_url: str
    post_contents: str
    forum_name: str
