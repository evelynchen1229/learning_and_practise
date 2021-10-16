def test_environment_is_qa(app_config):
    app_base_url = app_config.base_url
    port = app_config.app_port
    assert app_base_url == 'https://myqa-env.com'
    assert port == 80

def test_envirnment_is_dev(app_config):
    app_base_url = app_config.base_url
    port = app_config.app_port
    assert app_base_url == 'https://mydev-env.com'
    assert port == 8080
