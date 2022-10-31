from math_utils import function as f

sin = f.sin
cos = f.cos
ln = f.ln


def evaluate_and_print(function, at_value, respect_to):
    respect_to.set_value(at_value)
    f_x, f_x_prime = function.evaluate(respect_to=respect_to)
    print("f(%4d) = %20.5f and f'(%4d) = %20.5f" % (at_value, f_x, at_value, f_x_prime))


"""
    f (x) = sin(ln(cos(x)))
    f (1) = -0.57747
    f'(1) = -1.27149
    
    f (100) = -0.14759
    f'(100) =  0.580783
"""


def test_case_0():
    x = f.Variable()
    function = sin(ln(cos(x)))
    evaluate_and_print(function, 1, x)
    evaluate_and_print(function, 100, x)


"""
    f (x) = (x / ln(x)) ^ (1/2)
    f (2) = 1.698644
    f'(2) = -0.18800

    f (45.3) = 3.446658
    f'(45.3) = 0.028066
"""


def test_case_1():
    x = f.Variable()
    function = (x / ln(x)) ** (1 / 2)
    evaluate_and_print(function, 2, x)
    evaluate_and_print(function, 45.3, x)


"""
    f (x) = ln(ln(ln(x ^ 2)))
    f (2) = -1.11891
    f'(2) = 2.208426

    f (45.3) = 0.708845
    f'(45.3) = 0.002849
"""


def test_case_2():
    x = f.Variable()
    function = ln(ln(ln(x ** 2)))
    evaluate_and_print(function, 2, x)
    evaluate_and_print(function, 45.3, x)


def main():
    test_case_0()
    print("############")
    test_case_1()
    print("############")
    test_case_2()


if __name__ == "__main__":
    main()
