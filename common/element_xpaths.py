sign_in_xpath = '//button[@class="btn__primary--large from__button--floating"]'
username_xpath = '//input[@id="username"]'
password_xpath = '//input[@id="password"]'

search_input_xpath = '//input[@id="global-nav-typeahead-input"]'
search_btn_xpath = '//button[text()="Search"]'

geography_div_xpath = '//div[@id="ember54"]'
geography_input_xpath = '//input[@id="ember53-typeahead-region"]'
filtered_geography_inputs_xpath = '//*[@class="button--unstyled link-without-visited-state t-14 font-weight-400 cursor-pointer search-filter-typeahead__suggestion-item-value text-align-left"]'

company_div_xpath = '//div[@id="ember66"]'
company_input_xpath = '//input[@id="ember65-typeahead"]'

sr_results_raw_xpath = '//li[@class="pv5 ph2 search-results__result-item"]'
sr_locations_xpath = '//li[@class="result-lockup__misc-item"]'
sr_companies_xpath = '//*[@class="result-lockup__position-company"]'
sr_names_xpath = '//*[@class="result-lockup__name"]'
sr_job_titles_xpath = '//*[@class="Sans-14px-black-75%-bold"]'
sr_profile_urls_xpath = '//a[@class="ember-view" and ancestor-or-self::*[@class="result-lockup__name"]]'

next_btn_xpath = '//button[@class="search-results__pagination-next-button"]'
current_page_xpath = '//li[contains(@aria-label,"Current page")]'

# Bing
bing_search_input = '//input[@id="sb_form_q"]'

bing_sr_desc_xpath = '//*[@id="b_results"]/li[1]//p'
bing_sr_page_url_xpath = '//div[@class="b_title"]//a'
