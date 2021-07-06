# Work Notes for TwitOff App

## Monday, September 16, 2019
### What went well (in the context of working on the assignment) today?
Flask app is up and running. I created a module for loading data into the database.

### What was particularly interesting or surprising about the topic(s) today?
Fitting all the pieces together and acutally getting them to work is nice.

### What was the most challenging part of the work today, and why?
Python syntax: why the dot with `from .app import create_app`?
Bash syntax: what is the colon in `FLASK_APP=twitoff:APP`?
The different build patterns available for packages in general and Flask apps in particular can be confusing.
I would like to know the correct way to get a module to load and run while within the flask shell.

## Tuesday, September 17, 2019
### What went well (in the context of working on the assignment) today?
I obtained authentication keys obtained and they work.

### What was particularly interesting or surprising about the topic(s) today?
I am both surprised Twitter allows access to their data via an api, and I am also surprised at the number of hoops one is required to jump through to get that access.

### What was the most challenging part of the work today, and why?
Keeping the directory and file structure organized according to convention and requirements is often a stumbling block.

## Wednesday, September 18, 2019
### What went well (in the context of working on the assignment) today?
Today has been a struggle. My code breaks in ways that are not covered in the video.

### What was particularly interesting or surprising about the topic(s) today?
My head is a bit muddled, so I am not sure what to put here.

### What was the most challenging part of the work today, and why?
Getting a sense of what is happening behind the scenes and why with Flask, SQLAlchemy, etc., is difficult. Also, getting into debug mode was working and now it is not.

## Thursday, September 19, 2019
### What went well (in the context of working on the assignment) today?
The app is deployed to Heroku.

### What was particularly interesting or surprising about the topic(s) today?
I'm wondering how much of the trouble people have on Windows is because Windows makes things difficult, and how much is because instructors are on Macs. I am on Linux, so it is similar enough to Mac for me to follow the lesson pretty closely.

### What was the most challenging part of the work today, and why?
There are still bugs in my app. When I add a user, the user and their tweets get added, but sometimes an erro message from Heroku is displayed as well.
