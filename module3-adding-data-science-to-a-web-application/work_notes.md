# Work Notes

## 11 Nov 2019
Creation of a base flask app was the subject today, it went well but that's mostly
because instructions were clear, almost "copy-and-paste-able"

Unfortunately due to the nature of that it's a little hard to understand exactly what
is going on in the background. It's an intriguing mystery that will hopefully become
clearer as time goes on

Most challenging part of the day: creating a toy dataset. I didn't want to type
everything out in the flask shell (interpreter environment) so I insisted on creating
a .py file (`simplemakeusers.py`... it's older brother `makeusers.py` was a flop)
that would generate the information. It wasn't as simple as creating and running a .py 
from the terminal, as it had to be [run with app context](https://stackoverflow.com/questions/46540664/no-application-found-either-work-inside-a-view-function-or-push-an-application/46541219#46541219). 
There's a more [official way](https://flask.palletsprojects.com/en/1.1.x/cli/#custom-commands) of getting this done that I seek to understand soon.

## 12 Nov 2019

I implemented tweepy and successfully setup the twitter developer account to incorporate
actual use data into the flask app. I also managed to find another, still not ideal,
way of running a .py code in the flask shell to avoid typing everything out each time.
Instead of running with context, I just write the script (ex. myscript.py) then use
python's exec function: `exec(open('./mscripy.py').read())`

Today was also a bit slow and I"m still not so sure what is going on with much of the
inner workings of flask.

I ran into several issues throughout mostly all due to very tiny syntax errors:
- in one instance, I stored the user as a class user, but the name of the user was an
attribute, but I set it as the class. My peers pointed it out so I fixed it and was
able to move on (Error was an Interface error - likely caused by an unsupported type
(i.e. non-string)
- The other instance was very silly and not caught by the interpreter. The number of
tweets being returned was 1-5. All I needed to do was specify `count=200` instead of
`counts=200`. even after fixing this, the number of tweets returned are around
20-30. Presumably this is now just returning the first page of the user's twitter account

## 13 Nov 2019
Successfully implemented predictions and a comparator for multiple users loaded into
the database. I also created distinct HTML forms based on the event of adding a user
or comparing two users with a prediction

The most interesting and challenging part were one in the same: formatting the html code
based on the data (selections, users uploaded, etc.). Though I haven't done any CSS
styling, I spent a lot of time thinking about the logic of the code and all the
app decorators that are controlling what is posted and what is requested. Jinja calls
for creating HTML with python also feel complex to me at the moment, especially the html
pages which inherit from the base/home file
