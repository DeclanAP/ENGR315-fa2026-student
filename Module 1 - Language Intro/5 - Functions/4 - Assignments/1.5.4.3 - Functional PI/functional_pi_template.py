import math


def my_pi(target_error):
    """
    Implementation of Gauss–Legendre algorithm to approximate PI from https://en.wikipedia.org/wiki/Gauss%E2%80%93Legendre_algorithm

    :param target_error: Desired error for PI estimation
    :return: Approximation of PI to specified error bound
    """

    ### YOUR CODE HERE ###
    
    # modify these lines to correct set the variable values
    a = 1
    b = 1/math.sqrt(2)
    t = 0.25
    p = 1

    NewA: float
    NewB: float
    Newt: float
    Newp: float

    for i in range(1, 10):
        NewA = (a+b)/2
        NewB = math.sqrt(a*b)
        Newp = 2*p
        Newt = t - p*(NewA - a)**2

        a = NewA
        b = NewB
        p = Newp
        t = Newt

        print("Loop Iteration: ", i)

        pi_estimate = ((a+b)**2)/(4*t)

    return pi_estimate




desired_error = 1E-10

approximation = my_pi(desired_error)

print("Solution returned PI=", approximation)

error = abs(math.pi - approximation)

if error < abs(desired_error):
    print("Solution is acceptable")
else:
    print("Solution is not acceptable")
