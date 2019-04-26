```
Title        : (Python) Decorator and Wrapper
Subtitle     : Intermediate Python with Lucid Showcase
IsPublic     : true
IsTop        : false
IsOnList     : true
RankingIndex : 0
```

Sometimes, for the purpose of testing or working in frameworks, we need to add some frequently used but minor features to our functions. Python's **decorators** are perfect for such scenario.


# Showcase

We are going to build a `print_return` decorator which prints **function names**, **arguments** and **return value** to the console in a human readable way. With the help of it, developers can implement and remove such feature quickly when doing tests--without messing up the function body.

The following code demonstrates how to define a `decorator` along with its `wrapper`.

```python
from functools import wraps

# decorator function
def print_return(func):
    """print name, arguments and return value of the decorated func"""

    # wrapper function
    @wraps(func)
    def wrapper(*args, **kwargs):
        # this wrapper return the same value as the decorated func
        result = func(*args, **kwargs)
        # but print content before return
        print(func.__name__ + str(args) + "=" + str(result))
        # return
        return result

    return wrapper
```

Than, we define a function `squared_sum` and implement `@print_return` on it.

```python
@print_return
def squared_sum(a: int, *args) -> int:
    return (a ** 2 + sum((v ** 2) for v in args))
```

And execute it:

```python
result = squared_sum(1, 2, 3)
# print: squared_sum(1, 2, 3)=14
# result would be 14
```
There are a lot detailed explanation about each single syntax of it, but I skip them here since I think it's not that important in this stage. Just imagine that: we are putting **decorated function** as a **argument** of the **decorators** --  execute them and append some extra tasks, such as printing, in the **wrapper**.

![img](https://someones.tw/static/img/postImg/lucid_showcase_04.png)

# Discussion and Conclusion

- First things first, we define a decorator called `print_return`.
- We can apply decorator to functions with `@` character:
```python
@my_decorator
def my_function():
    ...
```
- We can easily apply and remove the decorators, which conforms to the DRY principal: Do Not Repeat Your Self.

# Reference

* David Beazley and Brian K. Jones, Python Cookbook 3rd Edition, Chap.9, O'REILLY, 2014, ISBN 9781449340377
