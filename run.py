from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

target = None


def play(thread_no, proxy):
    PROXY = proxy
    webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
        "httpProxy": PROXY,
        "sslProxy": PROXY,
        "proxyType": "MANUAL",
    }
    browser = webdriver.Firefox()
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


def main():
    global target
    cek = input('Cek proxy? y/n : ')
    if cek.lower() != 'y':
        LINK = input('Link : ')
        target = LINK
    WORKERS = input('Workers : ') or 4
    proxies = open('proxies.txt', 'r').readlines()
    if len(proxies) < 1:
        print('Proxy tidak boleh kosong!')
        sys.exit('PROXY_EMPTY')

    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        futures = [executor.submit(cekip if cek.lower(
        ) == 'y' else play, i, p) for i, p in enumerate(proxies)]
        for future in as_completed(futures):
            res = future.result()
            print(res)


if __name__ == '__main__':
    main()
