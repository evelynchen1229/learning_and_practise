from pytest import mark

@mark.engine
@mark.smoke
@mark.ui

def test_engine_functions_as_expected():
    assert True

def test_can_navigate_to_youtube(chrome_browser):
    chrome_browser.get('https://www.youtube.com')
    assert True

