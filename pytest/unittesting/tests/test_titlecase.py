from titlecase import title_case

def test_title_capitalised_as_expected():
    initial = 'this is a test'
    expected = 'This Is a Test'
    actual = title_case(initial)
    assert expected == actual
