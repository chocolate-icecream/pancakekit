from pancakekit import Pancake

cake = Pancake()

@cake.topping
def fibonacci(n=5):
    return (fibonacci(n-1) + fibonacci(n-2)) if n >= 2 else n

cake.serve()