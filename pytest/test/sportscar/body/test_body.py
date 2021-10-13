from selenium import webdriver
from pytest import mark

@mark.smoke
@mark.ui

def test_can_navigate():
    browser = webdriver.Chrome()
    browser.get('https://www.google.co.uk')
    assert True
