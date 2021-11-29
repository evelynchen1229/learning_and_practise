"""
can I call fizzbuzz
get '1' when I pass in 1
get '2' when I pass in 2
get 'Fizz' when I pass in 3
get 'Buzz' when I pass in 5
get 'Fizz' when I pass in 6 (multiple of 3)
get 'Buzz' when I pass in 10 (multiple of 5)
get 'FizzBuzz' when I pass in 15 (multiple of 3 or 5)

"""

def fizzBuzz(value):
    if value % 15  == 0:
        return 'FizzBuzz'
    elif value % 3 == 0:
        return 'Fizz'
    elif value % 5 == 0:
        return 'Buzz'
    return str(value)
