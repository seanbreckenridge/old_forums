import json
import time
from typing import Optional

import click
from logzero import logger
from selenium import webdriver
from bs4 import BeautifulSoup as soup

MINECRAFT_FORUM_BASE = "https://www.minecraftforum.net"
MINECRAFT_FORUM_PAGE = "https://www.minecraftforum.net/members/{}/posts"
FORUM_NAME = "Minecraft Forum"


def _parse_post(post_el):
    try:
        epoch: int = int(post_el.find("abbr")["data-epoch"])
        post_data: str = post_el.find(class_="post-activity").find_all("a")[-1]
        post_title: str = post_data.text.strip()
        post_url: str = post_data["href"]
        post_contents: str = post_el.find(class_="post-content").text.strip()
    except Exception as e:
        logger.exception(e)
    return {
        "date": epoch,
        "post_title": post_title,
        "post_url": post_url,
        "contents": post_contents,
        "forum_name": FORUM_NAME,
    }


def scrape_forum_data(username, driver):

    driver.get(MINECRAFT_FORUM_PAGE.format(username))
    click.secho("Hit enter when the page is ready > ", nl=False, fg="green")
    input()

    parsed_posts = []

    while True:

        time.sleep(5)

        page_soup = soup(driver.page_source, "html.parser")
        posts = page_soup.find(class_="comment-listing").find_all(class_="comment")
        parsed_posts.extend(list(map(_parse_post, posts)))
        next_page_button = page_soup.find(class_="b-pagination-item-next")
        if next_page_button is not None:
            logger.debug("getting next page...")
            driver.get(MINECRAFT_FORUM_BASE + next_page_button.find("a")["href"])
        else:
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
