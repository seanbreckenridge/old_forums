"""
Only have the one page, so not gonna implement pagination
"""

import json
from typing import Optional

import click
from logzero import logger
from selenium import webdriver
from bs4 import BeautifulSoup as soup

FORUM_NAME = "Hypixel"
HYPIXEL_FORUM = "https://hypixel.net/members/{}/#recent-content"
HYPIXEL_BASE = "https://hypixel.net"


def _parse_post(post_el):
    try:
        epoch: int = int(post_el.find(class_="u-dt")["data-time"])
        post_data: str = post_el.find(class_="contentRow-title").find("a")
        post_title: str = post_data.text.strip()
        post_url: str = HYPIXEL_BASE + post_data["href"]
        post_contents: str = post_el.find(
            class_="contentRow-snippet"
        ).text.strip()  # not the whole thing, but good enough
    except Exception as e:
        logger.exception(e)
        raise e
    return {
        "dt": epoch,
        "post_title": post_title,
        "post_url": post_url,
        "post_contents": post_contents,
        "forum_name": FORUM_NAME,
    }


def scrape_forum_data(username, driver):
    driver.get(HYPIXEL_FORUM.format(username))
    click.secho("Hit enter when the page is ready > ", nl=False, fg="green")
    input()

    page_soup = soup(driver.page_source, "html.parser")
    parsed_posts = list(
        map(_parse_post, page_soup.find_all(class_="js-inlineModContainer"))
    )
    logger.debug("done, writing to file...")
    return parsed_posts


@click.command()
@click.argument("FORUM_USERNAME")
@click.option(
    "--to-file",
    type=click.Path(),
    required=True,
    help="File to store parsed JSON to",
)
@click.option(
    "--chromedriver-path",
    type=click.Path(exists=True),
    required=False,
    help="Location of the chromedriver",
)
def main(forum_username: str, to_file: str, chromedriver_path: Optional[str]):
    cpath = "chromedriver" if chromedriver_path is None else chromedriver_path
    driver = webdriver.Chrome(executable_path=cpath)

    logger.warning(
        "The FORUM_USERNAME should look forumname.98493, go to 'Postings' and copy the ID from there"
    )
    try:
        forum_data = scrape_forum_data(forum_username, driver)
    except Exception as e:
        logger.exception(e)
    finally:
        driver.quit()

    with open(to_file, "w") as to_f:
        json.dump(forum_data, to_f)


if __name__ == "__main__":
    main()
