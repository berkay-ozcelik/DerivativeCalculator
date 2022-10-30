import math
from abc import abstractmethod


class _PrimitiveFunction:
    @abstractmethod
    def apply(self, parameters: tuple) -> tuple:
        pass


class _SubPrimitiveFunction(_PrimitiveFunction):
    def apply(self, parameters: tuple) -> tuple:
        lhs = parameters[0]
        rhs = parameters[1]
        derivative_lhs = parameters[2]
        derivative_rhs = parameters[3]

        function_result = lhs - rhs
        derivative_result = derivative_lhs - derivative_rhs

        return function_result, derivative_result


class _AddPrimitiveFunction(_PrimitiveFunction):

    def apply(self, parameters: tuple) -> tuple:
        lhs = parameters[0]
        rhs = parameters[1]
        derivative_lhs = parameters[2]
        derivative_rhs = parameters[3]

        function_result = lhs + rhs
        derivative_result = derivative_lhs + derivative_rhs
        return function_result, derivative_result


class _MultPrimitiveFunction(_PrimitiveFunction):
    def apply(self, parameters: tuple) -> tuple:
        lhs = parameters[0]
        rhs = parameters[1]
        derivative_lhs = parameters[2]
        derivative_rhs = parameters[3]

        function_result = lhs * rhs
        derivative_result = derivative_lhs * rhs + derivative_rhs * lhs

        return function_result, derivative_result


class _PowPrimitiveFunction(_PrimitiveFunction):
    def apply(self, parameters: tuple) -> tuple:
        base = parameters[0]
        exponent = parameters[1]
        derivative_base = parameters[2]
        derivative_exponent = parameters[3]

        function_result = base ** exponent
        derivative_result = function_result * (exponent * derivative_base / base + derivative_exponent * math.log(base))
        return function_result, derivative_result


class _SinPrimitiveFunction(_PrimitiveFunction):

    def apply(self, parameters: tuple) -> tuple:
        value = parameters[0]
        derivative_value = parameters[1]

        function_result = math.sin(value)
        derivative_result = math.cos(value) * derivative_value
        return function_result, derivative_result


class _CosPrimitiveFunction(_PrimitiveFunction):

    def apply(self, parameters: tuple) -> tuple:
        value = parameters[0]
        derivative_value = parameters[1]

        function_result = math.cos(value)
        derivative_result = -math.sin(value) * derivative_value

        return function_result, derivative_result


class _TreeNode:
    @abstractmethod
    def evaluate(self, respect_to) -> tuple:
        pass


class _Operator(_TreeNode):
    def evaluate(self, respect_to) -> tuple:
        pass

    __function: _PrimitiveFunction

    def __init__(self, function: _PrimitiveFunction):
        self.__function = function

    def get_function(self) -> _PrimitiveFunction:
        return self.__function


class _DualOperator(_Operator):
    __left_child: _TreeNode
    __right_child: _TreeNode

    def __init__(self, left_child: _TreeNode, function: _PrimitiveFunction, right_child: _TreeNode):
        super().__init__(function)
        self.__left_child = left_child
        self.__right_child = right_child

    def evaluate(self, respect_to) -> tuple:
        value_rhs, derivative_rhs = self.__right_child.evaluate(respect_to)
        value_lhs, derivative_lhs = self.__left_child.evaluate(respect_to)
        args = (value_lhs, value_rhs, derivative_lhs, derivative_rhs)
        return super().get_function().apply(args)


class _SingleOperator(_Operator):
    __child: _TreeNode

    def __init__(self, child: _TreeNode, function: _PrimitiveFunction):
        super().__init__(function)
        self.__child = child

    def evaluate(self, respect_to) -> tuple:
        value, derivative = self.__child.evaluate(respect_to)

        args = (value, derivative)

        return super().get_function().apply(args)


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

    def __str__(self):
        return "Operand"


def add(rhs, lhs) -> _TreeNode:
    rhs, lhs = __get_args(rhs, lhs)
    return _DualOperator(rhs, _AddPrimitiveFunction(), lhs)


def mult(rhs, lhs) -> _TreeNode:
    rhs, lhs = __get_args(rhs, lhs)
    return _DualOperator(rhs, _MultPrimitiveFunction(), lhs)


"""
    f(x) / g(x) = f(x) * g(x) ^ -1
"""

def div(rhs, lhs) -> _TreeNode:
    rhs, lhs = __get_args(rhs, lhs)
    lhs = pow(lhs, -1)
    return mult(lhs, rhs)


def sub(rhs, lhs) -> _TreeNode:
    rhs, lhs = __get_args(rhs, lhs)
    return _DualOperator(rhs, _SubPrimitiveFunction(), lhs)


def pow(base, ex) -> _TreeNode:
    base, ex = __get_args(base, ex)
    return _DualOperator(base, _PowPrimitiveFunction(), ex)


def cos(rad) -> _TreeNode:
    rad = __get_arg(rad)
    return _SingleOperator(rad, _CosPrimitiveFunction())


def sin(rad) -> _TreeNode:
    rad = __get_arg(rad)
    return _SingleOperator(rad, _SinPrimitiveFunction())


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
