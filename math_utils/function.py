import math
from abc import abstractmethod


class _Function:
    @abstractmethod
    def apply(self, parameters: tuple) -> tuple:
        pass


class _SubFunction(_Function):
    def apply(self, parameters: tuple) -> tuple:
        lhs = parameters[0]
        rhs = parameters[1]
        derivative_lhs = parameters[2]
        derivative_rhs = parameters[3]

        function_result = lhs - rhs
        derivative_result = derivative_lhs - derivative_rhs

        return function_result, derivative_result


class _AddFunction(_Function):

    def apply(self, parameters: tuple) -> tuple:
        lhs = parameters[0]
        rhs = parameters[1]
        derivative_lhs = parameters[2]
        derivative_rhs = parameters[3]

        function_result = lhs + rhs
        derivative_result = derivative_lhs + derivative_rhs
        return function_result, derivative_result


class _MultFunction(_Function):
    def apply(self, parameters: tuple) -> tuple:
        lhs = parameters[0]
        rhs = parameters[1]
        derivative_lhs = parameters[2]
        derivative_rhs = parameters[3]

        function_result = lhs * rhs
        derivative_result = derivative_lhs * rhs + derivative_rhs * lhs

        return function_result, derivative_result


class _PowFunction(_Function):
    def apply(self, parameters: tuple) -> tuple:
        base = parameters[0]
        exponent = parameters[1]
        derivative_base = parameters[2]
        derivative_exponent = parameters[3]

        function_result = base ** exponent
        negative = base < 0
        base = abs(base)
        derivative_result = function_result * (
                exponent * derivative_base / base + derivative_exponent * math.log(base))
        if negative:
            return function_result, -derivative_result

        return function_result, derivative_result


class _SinFunction(_Function):

    def apply(self, parameters: tuple) -> tuple:
        value = parameters[0]
        derivative_value = parameters[1]

        function_result = math.sin(value)
        derivative_result = math.cos(value) * derivative_value
        return function_result, derivative_result


class _CosFunction(_Function):

    def apply(self, parameters: tuple) -> tuple:
        value = parameters[0]
        derivative_value = parameters[1]

        function_result = math.cos(value)
        derivative_result = -math.sin(value) * derivative_value

        return function_result, derivative_result


class _LnFunction(_Function):
    def apply(self, parameters: tuple) -> tuple:
        value = parameters[0]
        derivative_value = parameters[1]

        function_result = math.log(value)
        derivative_result = derivative_value / value
        return function_result, derivative_result


class _TreeNode:
    @abstractmethod
    def evaluate(self, respect_to) -> tuple:
        pass

    def __init__(self, function: _Function):
        self.__function = function

    def get_function(self) -> _Function:
        return self.__function

    @abstractmethod
    def __add__(self, other):
        pass

    @abstractmethod
    def __sub__(self, other):
        pass

    @abstractmethod
    def __mul__(self, other):
        pass

    @abstractmethod
    def __truediv__(self, other):
        pass

    @abstractmethod
    def __pow__(self, power):
        pass


class _Operator(_TreeNode):
    def evaluate(self, respect_to) -> tuple:
        pass

    __function: _Function


class _DualOperator(_Operator):
    __left_child: _TreeNode
    __right_child: _TreeNode

    def __init__(self, left_child: _TreeNode, function: _Function, right_child: _TreeNode):
        super().__init__(function)
        self.__left_child = left_child
        self.__right_child = right_child

    def evaluate(self, respect_to) -> tuple:
        value_rhs, derivative_rhs = self.__right_child.evaluate(respect_to)
        value_lhs, derivative_lhs = self.__left_child.evaluate(respect_to)
        args = (value_lhs, value_rhs, derivative_lhs, derivative_rhs)
        return super().get_function().apply(args)

    def __add__(self, other):
        return add(self, other)

    def __sub__(self, other):
        return sub(self, other)

    def __mul__(self, other):
        return mult(self, other)

    def __truediv__(self, other):
        return div(self, other)

    def __pow__(self, power):
        return pow(self, power)


class _SingleOperator(_Operator):
    __child: _TreeNode

    def __init__(self, child: _TreeNode, function: _Function):
        super().__init__(function)
        self.__child = child

    def evaluate(self, respect_to) -> tuple:
        value, derivative = self.__child.evaluate(respect_to)

        args = (value, derivative)

        return super().get_function().apply(args)

    def __add__(self, other):
        return add(self, other)

    def __sub__(self, other):
        return sub(self, other)

    def __mul__(self, other):
        return mult(self, other)

    def __truediv__(self, other):
        return div(self, other)

    def __pow__(self, power):
        return pow(self, power)


class Variable(_TreeNode):
    __value: float

    def __init__(self, value=0.0):
        self.__value = value

    def evaluate(self, respect_to) -> tuple:
        if respect_to == self:
            return self.get_value(), 1
        else:
            return self.get_value(), 0

    def get_value(self) -> float:
        return self.__value

    def set_value(self, value: float):
        self.__value = value

    def __add__(self, other):
        return add(self, other)

    def __sub__(self, other):
        return sub(self, other)

    def __mul__(self, other):
        return mult(self, other)

    def __truediv__(self, other):
        return div(self, other)

    def __pow__(self, power):
        return pow(self, power)

    def __str__(self):
        return "(" + str(self.__value) + ")"


def add(rhs, lhs) -> _TreeNode:
    rhs, lhs = __get_args(rhs, lhs)
    return _DualOperator(rhs, _AddFunction(), lhs)


def mult(rhs, lhs) -> _TreeNode:
    rhs, lhs = __get_args(rhs, lhs)
    return _DualOperator(rhs, _MultFunction(), lhs)


"""
    f(x) / g(x) = f(x) * g(x) ^ -1
"""


def div(rhs, lhs) -> _TreeNode:
    rhs, lhs = __get_args(rhs, lhs)
    lhs = pow(lhs, -1)
    return mult(lhs, rhs)


def sub(rhs, lhs) -> _TreeNode:
    rhs, lhs = __get_args(rhs, lhs)
    return _DualOperator(rhs, _SubFunction(), lhs)


def pow(base, ex) -> _TreeNode:
    base, ex = __get_args(base, ex)
    return _DualOperator(base, _PowFunction(), ex)


def cos(rad) -> _TreeNode:
    rad = __get_arg(rad)
    return _SingleOperator(rad, _CosFunction())


def sin(rad) -> _TreeNode:
    rad = __get_arg(rad)
    return _SingleOperator(rad, _SinFunction())


def ln(var) -> _TreeNode:
    var = __get_arg(var)
    return _SingleOperator(var, _LnFunction())


def __get_arg(arg0):
    if isinstance(arg0, float) or isinstance(arg0, int):
        arg0 = Variable(arg0)
    if not isinstance(arg0, _TreeNode):
        raise Exception("Invalid argument exception.")
    return arg0


def __get_args(arg0, arg1):
    if isinstance(arg1, float) or isinstance(arg1, int):
        arg1 = Variable(arg1)
    if isinstance(arg0, float) or isinstance(arg0, int):
        arg0 = Variable(arg0)

    if not (isinstance(arg0, _TreeNode) and isinstance(arg1, _TreeNode)):
        raise Exception("Invalid argument exception.")

    return arg0, arg1
