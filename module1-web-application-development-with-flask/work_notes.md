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
