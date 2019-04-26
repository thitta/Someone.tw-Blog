```
Title        : (Python) Arguments, Args and Kwargs
Subtitle     : Intermediate Python with Lucid Showcase
IsPublic     : true
IsTop        : false
IsOnList     : true
RankingIndex : 0
```

For most of the beginners, learning how to define and implement basic function is often not hard. However, when it comes to **args and kwargs**, we need to put some extra effort to figure it out. If we can have clear concepts of args and kwargs, we can build more flexible and smart functions in pythonic ways.

# Showcase 1 : Args and Positional Argument

First things first, we are going to define a function called **squared_sum** which squares the input value and add them up.

```python
def squared_sum(a, b):
    return a ** 2 + b ** 2

print(squared_sum(1, 2))  # 5
```

It's fine, but there are a critical problem: what if we want the function can accept flexible quantity of input values instead of sticking to two and only two arguments?

Well, **args** is born for this purpose. we can change the function as follow:
```python
def squared_sum(a, *args):
    result = a ** 2
    for value in args:
        result += value ** 2
    return result

print(squared_sum())  # TypeError, at least one positional argument required
print(squared_sum(3))  # 9 (a=3 and args = [])
print(squared_sum(1, 2, 3))  # 14 (a=1 and args=[2,3])
```

In a word, `*args` will automatically collect all the **positional arguments** that are not explicitly defined by the function and put them in to a **tuple**. You can fetch them in the function body with the variable name `args`.

What exactly is **positional** arguments? We will explain in the next showcase.

# Showcase 2: Kwargs and Keyword Argument

Imagine we have a function which will print student name and birth year like this: 

```python
def print_student_info(name, birth_year, **kwargs):
    print("This is {}.".format(name))
    print("He/she was born in {}.".format(birth_year))

print_student_info("Mike", 1973)
# This is mike.
# He/she was born in 1973.
```

But what if we want the function can accept more flexible number of **keyword arguments** and print them as well? We need the help of **kwargs**. Let's rewrite the function:

```python
def print_student_info(name, birth_year, **kwargs):
    print("This is {}.".format(name))
    print("He/she was born in {}.".format(birth_year))
    for key, value in kwargs.items():
        print("His/her {} is {}.".format(key, value))
```

We can use it as normal, only put the necessary argument:
```python
print_student_info("Mike", 1973)
# This is mike.
# He/she was born in 1973.
```

or we can add as much **keywords arguments** as we want:

```python
print_student_info("John", 1987, gender="male", blood_type="A")
# This is John.
# He/she was born in 1987.
# His/her gender is male.
# His/her blood_type is A.
```

What happens in the last case? First, `John` and `1987` are put into the function as **positional arguments**, which means it provides no variable key name. Than we add two more **keywords arguments** called `gender` and `blood_type`, which is not explicitly required by the function. In the function body, all these arguments will be collected into a dictionary called `kwargs`. In this case ,the kwargs will be

```python
{
    "gender": "male",
    "blood_type": "A"
}
```

You can also arrange all the arguments as **keywords arguments**:

```python
print_student_info(birth_year=1993, name="Lora", gender="female", blood_type="O")
# This is Lora.
# He/she was born in 1993.
# His/her gender is female.
# His/her blood_type is O.
```

In this case, the two predefined and required variable `name` and `birth_year` are passed in **keywords arguments** format -- it means that which variable should be arranged in front no longer matters. The rests of the **keywords arguments** will be captured by the `kwargs`.

# Showcase 3: Let's Wrap It up.

From the previous tow cases, we know:

* `args` collects all none-predefined **positional arguments** into a **tuple**.
* `kwargs` collects all none-predefined *keywords arguments* into a **dictionary**.

Lets wrap it up with a function that requires no argument but accept args and kwargs:
```python
def print_args_and_kwargs(*args, **kwargs):
    print("args={}".format(args))
    print(kwargs)
    
print_args_and_kwargs(23, 183, 76, name="John", gender="male")
```

What we will get is

```
args   = (23, 183, 76)
kwargs = {'name': 'John', 'gender': 'male'}
```

Crystal clear right? In the last case, we are going to combine args and kwargs to create a special kind of argument called **keyword only argument**.

# Showcase4: Extra Credit -- Keyword Only Argument

Imagine we are going to define a function which will generate a file. The function has two argument, the `read_only` controls if the file created should be read-only, the `report_error` controls if the function should report error if the operation fails. The sudo code would look like this:

```python
def create_file(filename: str, read_only: bool, report_error:bool) -> None:
    # do something here
```

And imagine how will we call it:

```python
create_file("readme.md", True, False)
```

Is it satisfying in terms of readability? In my opinion, the first argument might be understandable while the last two (True and False) are not. Under such circumstance, we can apply some tricks that make the last two arguments **Keyword only**:

```python
# We add *args before read_only and report_error
def create_file(filename: str, *args, read_only: bool, report_error: bool) -> None:
    # do something here
    pass
```

If we execute the function as we did in the previous case

```python
create_file("readme.md", True, False) # TypeError
```

It will raise an error since the True and False are all absorbed by the `*args` and no value are provided to `read_only` and `report_error`. Therefore the only way to execute the function would be: 

```python
create_file("readme.md", read_only=True, report_error=False)
```

Since we made `read_only` and `report_error` **keyword only** argument, it looks better!

# Discussion and Conclusion

* `args` and `kwargs` make our function more flexible and smart.
* `args` collects all none predefined **positional arguments** into a **tuple**.
* `kwargs` collects all none predefined **keywords arguments** into a **dictionary**.

# Reference

* David Beazley and Brian K. Jones, Python Cookbook 3rd Edition, Chap.9, O'REILLY, 2014, ISBN 9781449340377






