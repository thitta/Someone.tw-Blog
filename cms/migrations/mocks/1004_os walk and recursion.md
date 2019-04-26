```
Title        : (Python) OS walk and Recursion
Subtitle     : Intermediate Python with Lucid Showcase
IsPublic     : true
IsTop        : false
IsOnList     : true
RankingIndex : 0
```

Processing files is one of the most common tasks we have to handle. Python's `os` module provides a series of tools for such tasks. Sometimes, we have to go through a whole directory tree -- `os.walk()` is a perfect tool for such purpose. However, its mechanism might appear a little bit confounding at first, so we are going to spend some time to discuss it.

# Showcase 1

Assume we have a directory tree as the image below presents. We want to extract all the file paths of `.png`. 

![dir_tree](https://someones.tw/static/img/postImg/lucid_showcase_02.png)

In this case, we are going to build a function that find all the file paths with designated **extension name** in a directory. The function expects two argument, the first one is `dir_path` and the second one is `ext_name`, such like `.png`.

```python
import os

def find_extension(dir_path, ext_name):
    result = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if os.path.splitext(file)[1] == ext_name:
                result.append(os.path.join(root, file))
    return result
```    

We can execute the function and get the result:

```python
print(find_extension("/dir_1", ext_name=".png"))
# .../dir_1/1.png
# .../dir_2/2.png
# .../dir_3/5.png
# .../dir_4/4.png
```

What does `os.walK()` exactly do? Simply put, it recursively visit each directory under our target directory path, recording the following info of it in a 3-tuple:`(root_path, directory_names, file_names)`. In the end, return a **generator** object, which you can basically regard it as a list like this

```
[
    (".../dir_1", ["dir_2", "dir_3"], ["1.png"]), # 1
    (".../dir_1/dir_2", [], ["2.png", "3.txt"]),  # 2
    (".../dir_1/dir_3", ["dir_4"], ["5.png"]),    # 3
    (".../dir_1/dir_3/dir_4", [], ["4.png"])      # 4
]
```

The image below demonstrates how `os.walk()` visits each directory and records info:

![dir_tree](https://someones.tw/static/img/postImg/lucid_showcase_03.png)

Here we can go back to review our `find_extension()` again. Once we can understand how `os.walk()` works, the function becomes understandable: we go through the directories, examining extension name of files; if the extension name is equivalent to what we expect, than join it with root path, append into result and finally return.

# Showcase 2: Build Our Walk Function with Recursion

Sometimes, the environment we are working on probably don't equip tools such like `os.walk()`. For example, when we are using `paramiko`, one of Python's sftp module, to process the file system of the remote server, it only provides tools like `listdir()`. In this case, we are going to demonstrate how to build our own `walk function` with the concept of `recursion`.

```python
import os

def my_walk(init_dirpath):
    result = []

    # recursive function
    def do_recursion(root):
        root = root
        dirs = []
        files = []
        # list directory content and separate files and dirs
        for basename in os.listdir(root):
            if os.path.splitext(basename)[1] == "":
                # skip hidden file (start with .)
                if basename[0] == ".":
                    continue
                # append dirs
                dirs.append(basename)
            else:
                # append files
                files.append(basename)
            # record result of this round
            result.append((root, files, dirs))
        # put sub-dirs (if any) into recursion
        for dir in dirs:
            do_recursion(os.path.join(root=dir))

    # init recursion
    do_recursion(init_dirpath)
    # recursion finish and return
    return result
```

* First, `my_walk` function define a local function `do_recursion` in its body.
* This function will visit a directory, list files and sub-directories of it, than.....
* If the recursive function finds and records any sub-directories, visit it by calling the function itself, we name this process **recursion**.
* The whole process initiates at the `init_dirpath` we set and return the list of records once all the recursions are finished.

# Discussion and Conclusion

* `os.walk()` can help us go through a directory tree.
* In each single round, `os.walk()` generate a 3-tuple record `(root, dirs, files)`.
* We can build our own walk function with the concept of **recursion**.
* The codes presented above can be highly curtailed by [list comprehension](https://someone-blog.appspot.com/post/679/(Python)-List-Comprehension), try it if you are interested.
