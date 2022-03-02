from dataclasses import dataclass
from datetime import datetime
from typing import TextIO, NamedTuple, List, Iterator, Optional

import dateparser
from bs4 import BeautifulSoup, Tag
from autotui.fileio import namedtuple_sequence_load


# As generic of an approach as I can manage without site specific code
# For example of usage of this, see https://github.com/seanbreckenridge/HPI/blob/master/my/old_forums.py


class AchievementSelector(NamedTuple):
    """
    to avoid specifying CSS selectors for each site individually in code here,
    this loads a configuration file (a list of JSON objects) which specify how to detect
    and which CSS selectors to use to extract the information out of the HTML
    page. A path to that file is specified with the OLD_FORUMS_SELECTORS
    environment variable

    As an example of the file passed to load_from_blob, if you had just the one achievement page:
    [
        {
            "detector": "a[href*=\"somesite.com\"]",
            "site": "somesite.com",
            "achievement_container": "div.achievement",
            "achieved_filter": ".active",
            "achievement_name": "h2.title",
            "achievement_desc": ".description",
            "achievement_earned_at": ".date",
            "achievement_attribute": "data-title"
        }
    ]
    """

    detector: str  # some CSS selector which should only appear on this page, to detect which HTML file we're using
    site: str  # name of the site, to attach to achievements
    achievement_container: str  # CSS selector of an earned achievement div/container
    achieved_filter: str  # CSS selector which should be present in the container if you've earned it
    achievement_name: str  # CSS selector of the name element in the container
    achievement_desc: str  # CSS selector of the description of the achievement in the container
    achievement_earned_at: str  # CSS selector for when this was earned
    # often exact dates are specified as data or attributes on HTML elements
    # if this is 'text', just uses the text of the date element
    achievement_attribute: str

    @classmethod
    def load_from_blob(cls, fp: TextIO) -> List["AchievementSelector"]:
        """
        Given a file-like object, loads to this NamedTuple structure
        """
        return namedtuple_sequence_load(fp, to=cls)

    @staticmethod
    def match_selector(
        soup: BeautifulSoup, selectors: List["AchievementSelector"]
    ) -> "AchievementSelector":
        for s in selectors:
            if soup.select(s.detector):
                return s
        raise RuntimeError(f"For {soup} Couldn't match any detectors using {selectors}")


# make all timestamps naive, so they're comparable
# dateparser will include TZs if they're included and
# won't if they're not, so this normalizes that
def _remove_tz(dt: Optional[datetime]) -> datetime:
    assert dt is not None
    return datetime.fromtimestamp(dt.timestamp())


def select_one_assert(tag: Tag, selector: str) -> Tag:
    val = tag.select_one(selector)
    assert val is not None, f"{tag} {selector}"
    return val


@dataclass
class Achievement:
    site: str
    name: str
    description: str
    earned_at: datetime

    @staticmethod
    def parse_using_selectors(
        html_fp: TextIO, selectors: List[AchievementSelector]
    ) -> Iterator["Achievement"]:
        soup = BeautifulSoup(html_fp.read(), "html.parser")
        sel = AchievementSelector.match_selector(soup, selectors)
        for c in [
            c
            for c in soup.select(sel.achievement_container)
            if c.select(sel.achieved_filter)
        ]:
            date_el = select_one_assert(c, sel.achievement_earned_at)
            date_unparsed_text = (
                date_el.text
                if sel.achievement_attribute == "text"
                else date_el.get(sel.achievement_attribute, "")
            )
            assert isinstance(date_unparsed_text, str)
            yield Achievement(
                site=sel.site,
                name=select_one_assert(c, sel.achievement_name).text.strip(),
                description=select_one_assert(c, sel.achievement_desc).text.strip(),
                earned_at=_remove_tz(dateparser.parse(date_unparsed_text.strip())),
            )
