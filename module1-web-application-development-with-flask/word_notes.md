1. `pipenv` helps in managing our environment. It helps in having a reproducible and deployable environment. Specifically, we can tell if the environment has all all the dependencies we need and can ignore, so that deploying locally and on heroku becomes easier. 
2. `Pipfile` and `Pipfile.lock` helps in specifying whats in our environment so that it can be reproduced and deployed effectively.
3. __name__ is the internal string, that Python populates directly. If the file name is `hello.py`, __name__ will be directly replaced by `hello.py`
4. Decorators `(@)` modify functions. It adds context to the function. By definition, "a decorator is a function that takes another function and extends the behavior of the latter function without explicitly modifying it"
5. "By having `app.route` as decorator, the function `hello` is registered for the route `/` so that when that route is requested, `hello` is called and its result `“Hello world”` is returned back to the client (be it web browser, curl, etc)."
6. To run the environment from terminal on MacOS:  `FLASK_APP=hello.py flask run`
7. Having a folder with __init__.py defines that the folder is a package.
8. To run the package from the terminal: `FLASK_APP=twitoff:APP flask run` ......Here, before the colon is the package name and after the colon is the object created inside the __init__.py file.
9. While importing from various files, be aware of Circular Import: If A import B and B imports A, system may not know what to import first. So caution used be used in these circumstances.
10. `.config` is a python dictionary.
11. `'///'` makes a relative path.
12. `app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'` .... Its telling SQL Alchemy to use sqlite database, `///` shows the path of the specific database to use (db.sqlite3 in this instance).
13. Since, `.gitignore` ignores db file by default so that it will not be checked in. Database file should not be checked into github, for space and privacy reasons.
14. Syntax to re-create DB: 
- `DB.drop_all()`
- `DB.create_all()`


* What went well (in the context of working on the assignment) today?

Ans: Re-created the example from the class after watching the lecture video.

* What was particularly interesting or surprising about the topic(s) today?

Ans: The topic taught today was new for me and learnt a lot about Flask, decorators, how to create relationship between users and tweets, even though they are in different classes, etc.

* What was the most challenging part of the work today, and why?

Ans: Nothing I can think of.
