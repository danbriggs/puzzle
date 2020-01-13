from sympy import divisor_count

def averager(f):
    """Given f:Z×Z->R, averager(f):R×R->R is defined as the
    weighted average of f at each of the four neighboring lattice points."""
    def av_fun(x,y):
        a=int(x)
        b=int(y)
        fracx = x-a
        fracy = y-b
        upfracx = a+1-x
        upfracy = b+1-y
        lowerleft=upfracx*upfracy*f(a,b)
        lowerright=fracx*upfracy*f(a+1,b)
        upperleft=upfracx*fracy*f(a,b+1)
        upperright=fracx*fracy*f(a+1,b+1)
        return lowerleft+lowerright+upperleft+upperright
    return av_fun

def tester():
    my_fun = lambda x,y: divisor_count(x)*divisor_count(y)
    my_fun2 = averager(my_fun)
    print(my_fun(49,80))
    print(my_fun(50,80))
    print(my_fun(49,81))
    print(my_fun(50,81))    
    print(my_fun2(49.1,80.05))
