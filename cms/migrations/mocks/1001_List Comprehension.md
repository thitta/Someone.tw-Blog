```
Title        : (Python) List Comprehension
Subtitle     : Intermediate Python with Lucid Showcase
IsPublic     : true
IsTop        : false
IsOnList     : true
RankingIndex : 0
```

**List comprehension** provides a concise way to create a sub list from an existent one -- without using nested for loop which could take multiple lines. We can basically regard list comprehension as a **syntactic sugar**, while it is very widely used and can make life much more easier.

# Showcase 1: List Comprehension vs For Loop

Assume we get a list of student's basic information like this.

```Python
students = [
    {"id": 1, "name": "Tom", "gender": "M", "height":180.1},
    {"id": 2, "name": "Jen", "gender": "F", "height":153.5},
    {"id": 3, "name": "Bob", "gender": "M", "height":168.9},
    {"id": 4, "name": "Ann", "gender": "F", "height":170.1},
    {"id": 5, "name": "Tom", "gender": "M", "height":172.3},
]
```

What should we do if we want to extract all values of `name` into a list.

With the help of **List comprehension**, it only takes one line:

```Python
names = [student["name"] for student in students]
```

Life is exactly that easy! Of course we can achieve the same result with for loop, but it would take few more lines and is not that readable.

```Python
names = []
for student in students:
    names.append(student["name"])
```

What if we need all the names of the female students?

Just append **if clause** after **for**.
```Python
names = [v["name"] for v in students if v["gender"]=="F"]
```

Be aware that in this case, we use **v**, which means "value", to represent each single student that is looped over. There are some other common naming convention such like v, val, item, e, ele, element, etc. Just choose the one that is most comfortable for you and your team.

Again, we can still achieve the same result with for loop, but it becomes more verbose than the previous case since we have to write another nested **if**.

```Python
names = []
for v in students:
    if v["gender"] == "F":
        names.append(v["names"])
```

You can also manipulate the value when creating a new list. For example, round the student's height.

```Python
rounded_height = [round(v) for v in students]
```

# Showcase 2: More Than List

In fact, the comprehension clause returns a Python **generator** object, which can not only be used to generate a list.

For example, in the list of student, we found there are two students named Tom. But what if I'm only interested in listing unique names?

We can use Python's *set* to solve this problem:

```Python
unique_names = set(v["name"] for v in names)
```

In the same pattern you can also use list comprehension to generate tuples.

```Python
unique_names = tuple(v["name"] for v in names)
# or
unique_names = (v["name"] for v in names)
```

# Showcase 3: Ternary Assignment

If you are not familiar with **Ternary Assignment**. Let's have a quick review of it:

```Python
my_math_score = 82
my_science_score = 53

my_math_pass = True if my_math_score >= 60 else False
my_science_pass = True if my_science_score >= 60 else False

print(my_math_pass)  # True
print(my_science_pass)  # False
```

We can apply this skill to list comprehension. In this case, we have a list of dict which contains student's name and score, we are required to count how many students have pass the exam.

```Python
test_scores = [{"name": "tom", "score": 50},
               {"name": "tom", "score": 66},
               {"name": "tom", "score": 92},
               {"name": "tom", "score": 87}]          
```

We can do it in a single and elegant line:

```Python
pass_count = [True if v["score"] >= 60 else False for v in test_scores].count(True)
print(pass_count)  # 3
```

or use for loop:

```Python
pass_count = 0
for v in test_scores:
    if v["score"] >= 60:
        pass_count += 1
print(pass_count)  # 3
```

# Showcase 4: No Good Case

## Nested and Over Nested

List comprehension creates a list, by which we can nest into another list comprehension. However, I personally don't recommend nest for more than one layer since it could be hard to read.

```Python
# nested
result = [i for i in [j for j in my_list]]

# over nested
result = [i for i in [j for j in [k for k in my_list]]]
```

## Use For Loop Instead when Executing Something

If you are going to execute commands toward a list of things and not interested in the list generated, **use for loop instead of list comprehension** even though it could take few more lines. Hide execution code in list comprehension increase the difficulty for debug. 

In the following sudo case, we have a list of url and we are going save the HTTP GET result of them....

```Python
urls = []
result = []

# Do
for url in urls:
    result.append(HTTP.GET(url))

# DO NOT...though it still works
[result.append(HTTP.GET(url) for url in urls)]
```

# Discussion and Conclusion

- List comprehension is concise and powerful.
- List comprehension can also be used to create tuple and set.
- We can apply **if clause** and **ternary assignment** in list comprehension.
- Do not over nested list comprehension. Or use list comprehension when executing commands.