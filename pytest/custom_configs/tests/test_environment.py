from pytest import mark

# to show skip reason when running the test:
# pytest -v -rs read only skip
# read both skip and xfail -rxs
@mark.skip(reason='broken by deploy somenumber')
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

# you expect the test to fail - xfail
# pytest -v -rx read only xfail
@mark.xfail(reason="there is no stage environment set up")
def test_envirnment_is_stage(app_config):
    app_base_url = app_config.base_url
    port = app_config.app_port
    assert port == 808
