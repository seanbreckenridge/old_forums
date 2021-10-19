# old_forums

Parses posts/achievements from random forums I used in the past. I don't use any of these anymore, but they contain random thoughts I had back then, so parsing them so I have access to them

The bit of lib code here pulls CSS selectors from a config file to detect/parse achievement pages. Used in [HPI](https://github.com/seanbreckenridge/HPI/blob/master/my/old_forums.py)

The forum posts are loaded from JSON files created by `./selenium_scripts`, while forum achievements are parsed from the raw HTML pages (i.e., by right click and `save as`ing a page, so that its possible to update)

## Installation

Requires `python3.6+`

To install with pip, run:

    pip install git+https://github.com/seanbreckenridge/old_forums

### selenium_scripts

Putting these up here as reference. I have so little posts on some of these that didn't have to worry about pagination.

All the posts get pulled out into a common schema:

```
forum_name: str
post_title: str  (name/title of the post)
post_url: str  (url to the post)
post_contents: str  (what I actually said)
dt: epoch datetime
```

Based on code from [`steamscraper`](https://github.com/seanbreckenridge/steamscraper)

As an example; `minecraft_forum.py`

```
python3 ./minecraft_forum.py <username> --to-file ./minecraft_forum.json
Hit enter when the page is ready >
[D 200903 17:18:15 minecraft_forum:49] getting next page...
[D 200903 17:18:24 minecraft_forum:49] getting next page...
[D 200903 17:18:32 minecraft_forum:49] getting next page...
[D 200903 17:18:39 minecraft_forum:49] getting next page...
[D 200903 17:18:46 minecraft_forum:49] getting next page...
[D 200903 17:18:54 minecraft_forum:49] getting next page...
[D 200903 17:19:01 minecraft_forum:49] getting next page...
[D 200903 17:19:08 minecraft_forum:49] getting next page...
[D 200903 17:19:16 minecraft_forum:49] getting next page...
[D 200903 17:19:23 minecraft_forum:49] getting next page...
[D 200903 17:19:30 minecraft_forum:49] getting next page...
[D 200903 17:19:39 minecraft_forum:52] done, writing to file...
```
