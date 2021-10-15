from pytest import mark

@mark.smoke
@mark.ui

def test_can_navigate(chrome_browser):
    chrome_browser.get('https://www.google.co.uk')
    assert True
