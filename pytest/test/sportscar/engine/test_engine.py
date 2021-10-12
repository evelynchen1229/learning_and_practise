from pytest import mark

@mark.engine
@mark.smoke

def test_engine_functions_as_expected():
    assert True
