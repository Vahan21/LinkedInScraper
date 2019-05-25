from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from common.element_xpaths import *
import time
import pandas as pd
import os
import random

driver = None
actions = None
sleep_time = None
max_pages = None
wait_time = None
query_url = None
filter_by_companies = None
filter_by_geography = None
linkedin_username = None
linkedin_password = None
successful_init = True


def init_variables_with_input():
    def to_int(var):
        try:
            return int(var)
        except Exception:
            print('Error. Invalid input, should be an ineger number')
            global successful_init
            successful_init = False
            print(var)

    global sleep_time, query_url, filter_by_companies, filter_by_geography, \
        max_pages, linkedin_username, linkedin_password, wait_time

    linkedin_username = input('Please input linkedin username: ')
    linkedin_password = input('Please input linkedin password: ')

    query_url = input('Please input the query url : ')

    sleep_time = input('Please input the time to sleep between actions in seconds (2 or more recommended): ')
    sleep_time = abs(to_int(sleep_time))

    if not successful_init:
        return

    max_pages = input('Please input the number of pages to traverse: ')
    max_pages = abs(to_int(max_pages))

    wait_time = 30


def wait_for_elem(xpath=None, elem=None, is_list=False):
    if is_list:
        WebDriverWait(driver, wait_time).until(ec.visibility_of_all_elements_located((By.XPATH, xpath)))
    elif elem is not None:
        WebDriverWait(driver, wait_time).until(ec.invisibility_of_element(elem))
    elif xpath is not None:
        WebDriverWait(driver, wait_time).until(ec.visibility_of_element_located((By.XPATH, xpath)))


def click_elem(elem, xpath):
    wait_for_elem(xpath)
    sleep_for_var_length()
    elem.click()


def find_elem(xpath, is_list=False, for_bing=False):
    wait_for_elem(xpath=xpath, is_list=is_list)
    sleep_for_var_length(for_bing=for_bing)
    if is_list:
        return driver.find_elements_by_xpath(xpath)
    return driver.find_element_by_xpath(xpath)


def send_keys_to_elem(elem, text, press_enter=True, for_bing=False):
    sleep_for_var_length(for_bing=for_bing)
    elem.send_keys(text)
    if press_enter:
        time.sleep(1)
        elem.send_keys(Keys.RETURN)


def sleep_for_var_length(for_bing=False):
    if for_bing:
        rand_sleep_time = random.randint(1, 10) / 10
    else:
        rand_sleep_time = sleep_time * random.randint(1, 10) / 10 + 0.8

    time.sleep(rand_sleep_time)


def in_page(xpath):
    try:
        wait_for_elem(xpath)
        sleep_for_var_length()
        driver.find_element_by_xpath(xpath)
        return True
    except NoSuchElementException:
        return False


def sign_in():
    username_field = driver.find_element_by_xpath(username_xpath)
    username_field.send_keys(linkedin_username)

    password_field = driver.find_element_by_xpath(password_xpath)
    password_field.send_keys(linkedin_password)

    sign_in_field = driver.find_element_by_xpath(sign_in_xpath)
    click_elem(sign_in_field, xpath=sign_in_xpath)

    assert in_page(search_input_xpath)


def make_search():
    wait_for_elem(search_input_xpath)
    driver.get(query_url)


def find_sub_elements(parent, child_xpath):
    try:
        return parent.find_element_by_xpath(f'.{child_xpath}')
    except:
        return 'N/A'


def scroll_down():
    for _ in range(2):
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        sleep_for_var_length()


def get_text(elem):
    try:
        return elem.text
    except Exception:
        return 'N/A'


def get_data_from_linkedin_search_results():
    results = []
    try:
        while True:
            time.sleep(5)
            scroll_down()
            search_results_raw = find_elem(sr_results_raw_xpath, is_list=True)
            for i, sr in enumerate(search_results_raw):

                company = find_sub_elements(sr, sr_companies_xpath)
                location = find_sub_elements(sr, sr_locations_xpath)
                user_name = find_sub_elements(sr, sr_names_xpath)
                job_title = find_sub_elements(sr, sr_job_titles_xpath)
                profile_url = find_sub_elements(sr, sr_profile_urls_xpath)

                try:
                    company = company.text.split('\n')[0]
                except Exception:
                    pass

                try:
                    profile_url = profile_url.get_attribute('href')
                except Exception:
                    pass

                location = get_text(location)
                user_name = get_text(user_name)
                job_title = get_text(job_title)

                results.append((company, location, user_name, job_title, profile_url))
                print(f'iteration {i}')

            current_page = find_elem(current_page_xpath).text
            print(f'curr page: {int(current_page)}')
            sleep_for_var_length()
            next_btn_elem = find_elem(xpath=next_btn_xpath, is_list=False)

            is_next_active = next_btn_elem.is_enabled()

            if int(current_page) >= max_pages or not is_next_active:
                break
            click_elem(next_btn_elem, xpath=next_btn_xpath)
            sleep_for_var_length()
    except:
        return results
    print('Success !')
    print('Scraping results', results)
    return results


def search_in_bing(text):
    search_input = find_elem(bing_search_input)
    sleep_for_var_length(for_bing=True)
    send_keys_to_elem(search_input, Keys.CONTROL + 'a', press_enter=False, for_bing=True)
    send_keys_to_elem(search_input, Keys.DELETE, press_enter=False, for_bing=True)
    send_keys_to_elem(search_input, text, press_enter=True, for_bing=True)


def visit_linkedin():
    sleep_for_var_length()
    driver.get(linkedin_url)
    sign_in()
    make_search()
    return get_data_from_linkedin_search_results()


def visit_bing(linkedin_results):
    global results_df

    data = []
    driver.get(bing_url)

    if len(linkedin_results) < 1:
        print('Error did not get any results from linkedin to save.')
        return

    counter = 0
    for company_name, location, user_name, job_title, profile_url in linkedin_results:
        try:
            if location == 'N/A':
                location = ''

            if company_name != 'N/A':
                search_text = str(company_name) + ' ' + str(location)
                search_in_bing(search_text)

                print(f'opening page for {search_text}')
                company_page_url_elem = find_elem(bing_sr_page_url_xpath, is_list=False, for_bing=True)

                company_desc = find_elem(bing_sr_desc_xpath, for_bing=True).text
                page_url = company_page_url_elem.get_attribute('href')
                bing_query_url = driver.current_url
            else:
                bing_query_url = 'N/A'
                page_url = 'N/A'
                company_desc = 'N/A'

            city, country = extract_city_country(location)

            data.append((user_name, job_title, company_name, profile_url, city, country,
                         bing_query_url, page_url, company_desc))

            results_df = pd.DataFrame(columns=['Name', 'Job Title', 'Company Name',
                                               'Profile URL', 'City', 'Country',
                                               'Bing Search Query URL', 'Bing 1st Result Website',
                                               'Bing 1st result text'],
                                      data=data)
            counter += 1
            if counter % 10 == 0:
                save_to_excel(results_df)
        except:
            continue
    save_to_excel(results_df)


def save_to_excel(df):
    writer = pd.ExcelWriter('linkedin_data.xlsx', engine='xlsxwriter', options={'strings_to_urls': False})
    df.to_excel(writer)
    writer.close()
    print('Saved file successfully')


def extract_city_country(location):
    try:
        city, country = location.split(', ')
    except ValueError:
        city = 'N/A'
        country = location
    return city, country


def main():
    init_variables_with_input()
    if not successful_init:
        return

    global driver, actions
    executable_path = os.path.join(os.getcwd(), 'chromedriver')
    driver = webdriver.Chrome(executable_path=executable_path)
    driver.maximize_window()
    actions = ActionChains(driver)

    results = visit_linkedin()

    visit_bing(results)
    driver.close()


linkedin_url = 'https://www.linkedin.com/sales/?trk=d_sales2_nav_home'
bing_url = 'https://www.bing.com/search?q=search&qs=n&form=QBLH&sp=-1&pq=search&sc=8-6&sk=&cvid' \
           '=8850AA98E98C4C09BEFDA136B07242F2'

if __name__ == '__main__':
    try:
        main()
    except:
        print('=====================================================================')
        print('Some error occured: perhaps an issue with internet connection or input given at the start.')
        print('=====================================================================')
