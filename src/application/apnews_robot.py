import logging
import time

from RPA.Browser.Selenium import Selenium

from src.application.common.utils.helpers import Helper
from src.application.common.utils.locators import Locators
from src.application.scraper import Scraper
from src.infrastructure.settings import (FILTER_TO_SELECT, SEARCH_TEXT,
                                         WEBSITE_URL)


class ApNewsRobot:
    def __init__(self) -> None:
        self.browser = Selenium()
        self.run()

    def run(self):
        try:
            self.start()
            Helper.excel_generator(Scraper.fetch_posts(self, postsList=[]))
        except Exception as ex:
            logging.error(f"... ERROR COLLECTING DATA: {ex} ...")
            return None

    def start(self):
        logging.info(f"... OPENING BROWSER - LOCATION: {WEBSITE_URL} ...")
        browser_opts = {
            "arguments": ["--headless", "--disable-gpu", "--window-size=1920,1080"]
        }
        self.browser.open_available_browser(
            WEBSITE_URL, headless=True, options=browser_opts
        )

        self.search()

    def search(self):
        logging.info(f"... SEARCH SENTENCE: {SEARCH_TEXT} ...")
        time.sleep(3)
        self.browser.wait_until_element_is_visible(Locators.SEARCH_BTN)
        self.browser.click_element(Locators.SEARCH_BTN)

        self.browser.wait_until_element_is_visible(Locators.SEARCH_INPUT)
        self.browser.input_text(Locators.SEARCH_INPUT, SEARCH_TEXT)

        self.browser.click_element(Locators.SEARCH_SUBMIT)

        self.sort_posts()

    def sort_posts(self):
        logging.info("... SELECTED SORT: NEWEST ...")
        self.browser.wait_until_element_is_visible(Locators.SORT_SELECT)
        self.browser.click_element_when_visible(Locators.SORT_SELECT)

        self.browser.wait_until_element_is_visible(Locators.SORT_SELECT_NEWEST_OPTION)
        self.browser.click_element_when_visible(Locators.SORT_SELECT_NEWEST_OPTION)

        self.filter()

    def filter(self):
        logging.info(f"... SELECTED FILTER: {FILTER_TO_SELECT} ...")
        time.sleep(2)
        self.browser.click_element_when_visible(Locators.EXPAND_FILTER_BTN)
        self.browser.click_button_when_visible(Locators.CHECK_FILTER)
