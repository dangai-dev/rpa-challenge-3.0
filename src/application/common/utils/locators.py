from src.infrastructure.settings import FILTER_TO_SELECT


class Locators:
    SEARCH_BTN = '//bsp-search-overlay[@class="SearchOverlay"]//button[@class="SearchOverlay-search-button"]'
    SEARCH_INPUT = '//*[@id="Page-header-trending-zephr"]/div[2]/div[3]/bsp-search-overlay/div/form/label/input'
    SEARCH_SUBMIT = '//*[@id="Page-header-trending-zephr"]/div[2]/div[3]/bsp-search-overlay/div/form/button'
    SORT_SELECT = '//select[@name="s"]'
    SORT_SELECT_NEWEST_OPTION = '//option[@value="3"]'
    EXPAND_FILTER_BTN = '//div[contains(@class, "SearchFilter-heading")]'
    CHECK_FILTER = f'//span[normalize-space(text())="{FILTER_TO_SELECT}"]/preceding-sibling::input[@type="checkbox"]'
    POSTS_DIV = '//div[@class="SearchResultsModule-results"]//bsp-list-loadmore[@class="PageListStandardD"]//div[@class="PageList-items-item"]//div[@class="PagePromo"]'
    POST_TEXT = "PagePromoContentIcons-text"
    POST_DATE = "Timestamp-template"
    POST_DATE_NOW = "Timestamp-template-now"
    POST_IMG = "Image"
    NEXT_PAGE_BTN = "class:Pagination-nextPage"
