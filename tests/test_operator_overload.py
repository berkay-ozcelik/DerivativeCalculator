from math_utils import function as f

sin = f.sin
cos = f.cos
ln = f.ln


def main():
    print("##################")
    test_case_0()
    print("##################")
    test_case_1()
    print("##################")
    test_case_2()
    print("##################")
    test_case_3()


"""
    f (x) = 3x + sin(x) + x^2

    f (1) = 4.841471
    f'(1) = 5.540302

    f (7) = 70.65699
    f'(7) = 17.75390

    f (100) = 10299.49
    f'(100) = 203.8623
"""


def test_case_0():
    x = f.Variable()
    function = x * 3 + sin(x) + x ** 2

    value_at = 1
    evaluate_and_print(function, value_at, x)

    value_at = 7
    evaluate_and_print(function, value_at, x)

    value_at = 100
    evaluate_and_print(function, value_at, x)


"""
        f(x) = x^cos(x^2) * x^(x^3) + x^(x^sin(cos(x)))
        f (1)   = 2.00 
        f'(1)   = 2.54

        f (2)   = 164.4206
        f'(2)   = 2292.724

        f (2.5) = 4126043
        f'(2.5) = 98951707
"""


def test_case_1():
    x = f.Variable()
    function = x ** cos(x ** 2) * x ** (x ** 3) + x ** (x ** sin(cos(x)))
    evaluate_and_print(function, at_value=1, respect_to=x)
    evaluate_and_print(function, at_value=2, respect_to=x)
    evaluate_and_print(function, at_value=2.5, respect_to=x)


"""
    f(x) =  sin(x) / cos(x^3 - 3 * x^2 + 3)
    f (1) = 1.557408
    f'(1) = -6.27656

    f (2) = 1.682942
    f'(2) = -0.77021
"""


def test_case_2():
    x = f.Variable()
    function = sin(x) / cos(x ** 3 - (x ** 2) * 3 + 3)
    evaluate_and_print(function, at_value=1, respect_to=x)
    evaluate_and_print(function, at_value=2, respect_to=x)


"""
    f(x) = x^2
    
    f (-8) = 64
    f'(-8) = -16
    
    f (1) = 1
    f'(1) = 2

    f (2) = 4
    f'(2) = 4

"""


def test_case_3():
    x = f.Variable()
    function = x ** 2
    evaluate_and_print(function, -8, x)
    evaluate_and_print(function, 2, x)


def evaluate_and_print(function, at_value, respect_to):
    respect_to.set_value(at_value)
    f_x, f_x_prime = function.evaluate(respect_to=respect_to)
    print("f(%4d) = %20.5f and f'(%4d) = %20.5f" % (at_value, f_x, at_value, f_x_prime))


if __name__ == "__main__":
    main()
