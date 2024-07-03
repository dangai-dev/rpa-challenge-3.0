from src.infrastructure.settings import FILTER_TO_SELECT


class Locators:
    # SEARCH_BTN = (
    #     '//button[@data-element="search-button"]'
    # )
    # SEARCH_INPUT = '//input[@data-element="search-form-input"]'
    # SEARCH_SUBMIT = '//button[@data-element="search-submit-button"]'
    # SORT_SELECT = '//select[@class="select-input"]'
    # SORT_SELECT_NEWEST_OPTION = '//option[@value="1"]'
    # EXPAND_FILTER_TOPICS_BTN = '//button[@data-toggle-trigger="see-all"]'
    # CHECK_FILTER = f'//span[normalize-space(text())="{FILTER_TO_SELECT}"]/preceding-sibling::input[@type="checkbox"]'
    # POSTS_DIV = '//div[@class="promo-wrapper"]'
    # POST_TITLE = '//div[@class="promo-content"]//div[@class="promo-title-container"]//h3[@class="promo-title"]//a[@class="link"]'
    # POST_DESCRIPTION = '//div[@class="promo-content"]//p[@class="promo-description"]'
    # POST_DATE = '//div[@class="promo-content"]//p[@class="promo-timestamp"]'
    # POST_IMG = 'image'
    # POST_IMG = '//div[@class="promo-media"]//a[@class="link promo-placeholder"][1]//img[@class="image"]'
    
    SEARCH_BTN = (
        '//*[@id="Page-header-trending-zephr"]/div[2]/div[3]/bsp-search-overlay/button'
    )
    SEARCH_INPUT = '//*[@id="Page-header-trending-zephr"]/div[2]/div[3]/bsp-search-overlay/div/form/label/input'
    SEARCH_SUBMIT = '//*[@id="Page-header-trending-zephr"]/div[2]/div[3]/bsp-search-overlay/div/form/button'
    SORT_SELECT = '//select[@name="s"]'
    SORT_SELECT_NEWEST_OPTION = '//option[@value="3"]'
    EXPAND_FILTER_BTN = '//div[contains(@class, "SearchFilter-heading")]'
    CHECK_FILTER = f'//span[normalize-space(text())="{FILTER_TO_SELECT}"]/preceding-sibling::input[@type="checkbox"]'
    POSTS_DIV = 'class:PagePromo'
    POST_TITLE = '//div[@class="PagePromo"]//div[@class="PagePromo-content"]//bsp-custom-headline[@custom-headline="div"]//div[@class="PagePromo-title"][1]//span[@class="PagePromoContentIcons-text"]'
    POST_DESCRIPTION = '//div[@class="PagePromo"]//div[@class="PagePromo-content"]//div[@class="PagePromo-description"][1]//span[@class="PagePromoContentIcons-text"]'
    POST_DATE = '//div[@class="PagePromo"]//div[@class="PagePromo-content"]//div[@class="PagePromo-byline"][1]//div[@class="PagePromo-date"][1]//span[@data-date=""]//span[@class="Timestamp-template"]'
    POST_IMG = '//div[@class="PagePromo-media"][1][1]//img[@class="Image"]'