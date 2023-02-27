from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

from fake_useragent import UserAgent
import time
import sys
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
ua = UserAgent()
target, proxies = None, []


def play(thread_no, proxy):
    if proxy and ':' in proxy:
        webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
            "httpProxy": proxy,
            "sslProxy": proxy,
            "proxyType": "MANUAL",
        }
    options = Options()
    options.set_preference("general.useragent.override", ua.random)
    options.set_preference("media.volume_scale", "0.0")
    browser = webdriver.Firefox(options=options)
    browser.get("https://rumble.com")
    time.sleep(5)
    browser.get(target)
    play_selector = 'div.bigPlayUI.ctp > div'
    WebDriverWait(browser, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, play_selector)))
    browser.find_element(By.CSS_SELECTOR, play_selector).click()
    delay = 60
    for i in range(delay):
        sys.stdout.write(
            '\r [{}] Waiting for : {} seconds'.format(thread_no, i))
        sys.stdout.flush()
        time.sleep(1)
    browser.close()
    return f'\n Thread no {thread_no} done!'


def test(thread_no, proxy):
    if proxy and ':' in proxy:
        webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
            "httpProxy": proxy,
            "sslProxy": proxy,
            "proxyType": "MANUAL",
        }
    options = Options()
    options.set_preference("general.useragent.override", ua.random)
    options.set_preference("media.volume_scale", "0.0")
    browser = webdriver.Firefox(options=options)
    browser.get("https://whoer.net")
    time.sleep(5)
    delay = 30
    for i in range(delay):
        sys.stdout.write(
            '\r [{}] Waiting for : {} seconds'.format(thread_no, i))
        sys.stdout.flush()
        time.sleep(1)
    browser.close()
    return f'\n Thread no {thread_no} done!'


def cekip(thread_no, proxy):
    PROXY = proxy
    webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
        "httpProxy": PROXY,
        "sslProxy": PROXY,
        "proxyType": "MANUAL",
    }
    browser = webdriver.Firefox()
    browser.get('https://httpbin.org/ip')
    delay = 10
    for i in range(delay):
        sys.stdout.write(
            '\r [{}] Waiting for : {} seconds'.format(thread_no, i))
        sys.stdout.flush()
        time.sleep(1)
    browser.close()
    return f'\n Thread no {thread_no} done!'


def whoer():
    options = webdriver.FirefoxOptions()
    # Define and set the user agent to Chrome 99;
    # The User-Agent Switcher and Manager extension has no config page that we can access as an url and click on it with selenium;
    # Therefore we can injecting the user agent instead
    profile_path = r'C:\Users\looqi\AppData\Roaming\Mozilla\Firefox\Profiles\e3ywktdw.test'
    extension_path = r"C:\Users\looqi\AppData\Roaming\Mozilla\Firefox\Profiles\e3ywktdw.test\extensions\{55f61747-c3d3-4425-97f9-dfc19a0be23c}.xpi"
    # user_agent = ua.random
    # print(user_agent)
    # options.set_preference("general.useragent.override", user_agent)
    # firefox_profile = FirefoxProfile(
    #     'C:/Users/looqi/AppData/Roaming/Mozilla/Firefox/Profiles/g4087t9y.default-release')
    # options.profile = firefox_profile
    # firefox_profile.add_extension(
    #     "C:/Users/looqi/AppData/Roaming/Mozilla/Firefox/Profiles/g4087t9y.default-release/extensions/{55f61747-c3d3-4425-97f9-dfc19a0be23c}.xpi")  # for spoof timezone
    # driver = webdriver.Firefox(
    #     options=options)
    # driver.get('https://www.whoer.net/')
    options = Options()
    useragent = ua.random
    print(useragent)
    options.set_preference("general.useragent.override", useragent)
    options.add_argument("-profile")
    options.add_argument(profile_path)
    options.set_preference("browser.cache.disk.enable", False)
    options.set_preference("browser.cache.memory.enable", False)
    options.set_preference("browser.cache.offline.enable", False)
    options.set_preference("network.http.use-cache", False)
    browser = webdriver.Firefox(options=options)
    browser.delete_all_cookies()
    browser.install_addon(extension_path)
    browser.get("https://ipinfo.io")
    time.sleep(50)
    browser.quit()


def main():
    global target, proxies
    PROX = input('Proxy url : ')
    if (PROX != '' and 'http' in PROX):
        res = requests.get(PROX)
        res = res.text
        proxies = res.splitlines()
        cek = input('Cek proxy? y/n : ')
    else:
        proxies = open('proxies.txt', 'r').readlines()
        cek = 'n'
    if cek.lower() != 'y':
        LINK = input('Link : ')
        target = LINK
    WORKERS = input('Workers : ') or 4
    if len(proxies) < 1:
        print('Proxy tidak boleh kosong!')
        sys.exit('PROXY_EMPTY')

    with ThreadPoolExecutor(max_workers=int(WORKERS)) as executor:
        futures = [executor.submit(cekip if cek.lower(
        ) == 'y' else play, i, p) for i, p in enumerate(proxies)]
        for future in as_completed(futures):
            res = future.result()
            print(res)


if __name__ == '__main__':
    main()
    # whoer()
