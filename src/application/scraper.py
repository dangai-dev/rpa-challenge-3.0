import logging
import time
from datetime import date, datetime

from dateutil.relativedelta import relativedelta
from RPA.Browser.Selenium import By, Selenium

from src.application.common.models.post import Post
from src.application.common.utils.helpers import Helper
from src.application.common.utils.locators import Locators
from src.infrastructure.settings import MONTHS_TO_SEARCH, SEARCH_TEXT


class Scraper:
    def __init__(self) -> None:
        self.browser = Selenium()

    def fetch_posts(self, postsList=list[Post]):
        try:
            logging.info("... FETCHING POSTS ...")
            self.browser.wait_until_element_is_visible(Locators.POSTS_DIV)
            time.sleep(4)
            posts = self.browser.get_webelements(Locators.POSTS_DIV)
            last_post_date = datetime.now()
            months_to_search = 1 if int(MONTHS_TO_SEARCH) == 0 else MONTHS_TO_SEARCH
            search_until_date = datetime.now() - relativedelta(
                months=int(months_to_search)
            )
            for post in posts:
                if len(postsList) > 0:
                    last_post_date = datetime.strptime(
                        postsList[-1].date, "%Y-%m-%d"
                    ).date()
                    if last_post_date.month < search_until_date.month:
                        logging.warning(
                            f"... A DATA QUEBROU AQUI: {last_post_date.month} < {search_until_date.month}..."
                        )
                        break

                post_text = post.find_elements(By.CLASS_NAME, Locators.POST_TEXT)
                title = post_text[0].text
                description = post_text[1].text
                date_post = Scraper.get_date(post)
                date = (
                    Helper.convert_to_datetime(date_post)
                    if date_post != ""
                    else date_post
                )
                search_text_total = Helper.search_text(SEARCH_TEXT, title, description)
                has_money = Helper.has_money(title, description)
                image = Helper.get_image(post, title)
                obj = Post(
                    title=title,
                    description=description,
                    date=date,
                    search_text_total=search_text_total,
                    image=image,
                    has_money=has_money,
                )
                postsList.append(obj)

            if last_post_date.month > search_until_date.month:
                self.browser.click_element_when_visible(Locators.NEXT_PAGE_BTN)
                pagination = self.browser.get_location().split("p=")[-1]
                logging.info(f"... PAGE: {pagination} ...")
                time.sleep(3)
                Scraper.fetch_posts(self, postsList)
            else:
                postsList.pop()

            return postsList

        except:
            logging.error(" ... ERROR FETCHING POSTS ...")

    def get_date(post) -> str:
        post_date = post.find_elements(By.CLASS_NAME, Locators.POST_DATE)
        post_date_now = post.find_elements(By.CLASS_NAME, Locators.POST_DATE_NOW)
        if len(post_date) > 0 or len(post_date_now) > 0:
            post_date = post_date if len(post_date) > 0 else post_date_now
            post_date = post_date[-1].text
        else:
            post_date = ""

        return post_date
