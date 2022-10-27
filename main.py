from math_utils import function as f

mult = f.mult
sub = f.sub
add = f.add
pow = f.pow
sin = f.sin
cos = f.cos


def main():
    x = f.Variable()
    """
        f(x) = 3x + sin(x) + x^2
    """
    function = add(mult(3, x), add(sin(x), pow(x, 2)))
    for i in range(1, 11):
        x.set_value(i)
        f_x, f_x_prime = function.evaluate(respect_to=x)
        print("f(%2d) = %8.3f and f'(%2d) = %8.3f" % (i, f_x, i, f_x_prime))

if __name__ == "__main__":
    main()
