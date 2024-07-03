import logging, time

from RPA.Browser.Selenium import Selenium, By

from src.application.common.models.post import Post
from src.application.common.utils.helpers import Helper
from src.application.common.utils.locators import Locators
from src.infrastructure.settings import SEARCH_TEXT


class Scraper:
    def __init__(self) -> None:
        self.browser = Selenium()

    def fetch_posts(self):
        logging.info("...FETCHING POSTS...")
        postsList: list[Post] = []
        self.browser.wait_until_element_is_visible(Locators.POSTS_DIV)
        time.sleep(4)
        posts = self.browser.get_webelements(Locators.POSTS_DIV)
        for post in posts:
            title = post.find_element(By.XPATH, Locators.POST_TITLE).text
            description = post.find_element(By.XPATH, Locators.POST_DESCRIPTION).text
            date = Helper.convert_to_datetime(post.find_element(By.XPATH, Locators.POST_DATE).text)
            search_text_total = Helper.search_text(
                SEARCH_TEXT, title, description
            )
            has_money = Helper.has_money(title, description)
            image = Helper.get_image(post, title)
            item = Post(
                title=title,
                description=description,
                date=date,
                search_text_total=search_text_total,
                image=image,
                has_money=has_money
            )
            postsList.append(item)
            
        return postsList
