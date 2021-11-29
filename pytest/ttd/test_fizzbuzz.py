from fizzbuzz import fizzBuzz

def test_can_call_fizzBuzz():
    assert fizzBuzz(1)

def test_number_one_stays_as_string_one():
    actual = fizzBuzz(1)
    expected = '1'
    assert actual == expected

def test_number_two_stays_as_string_two():
    actual = fizzBuzz(2)
    expected = '2'
    assert actual == expected

def test_number_three_returns_as_Fizz():
    actual = fizzBuzz(3)
    expected = 'Fizz'
    assert actual == expected

def test_number_five_returns_as_Buzz():
    actual = fizzBuzz(5)
    expected = 'Buzz'
    assert actual == expected

def test_mul_three_returns_as_Fizz():
    actual = [fizzBuzz(12), fizzBuzz(6), fizzBuzz(9)]
    expected = ['Fizz'] *3
    assert actual == expected

def test_mul_five_returns_as_Buzz():
    actual = [fizzBuzz(20), fizzBuzz(10), fizzBuzz(25)]
    expected = ['Buzz'] *3
    assert actual == expected

def test_mul_fifteen_returns_as_FizzBuzz():
    actual = [fizzBuzz(0), fizzBuzz(15), fizzBuzz(30)]
    expected = ['FizzBuzz'] *3
    assert actual == expected
