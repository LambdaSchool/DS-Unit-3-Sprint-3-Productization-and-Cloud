# DS-Unit-3-Sprint-3-Productization-and-Cloud
Building a real deployed full-stack application, backed by Data Science
--------------------

*Note* - assignments this week are all steps in a larger week-long project. They
are to be worked on in a repo you make with your own account, as instructed in
the first day. You should still fork this repo, and open a PR where you add a
`work_notes.md` file that includes a link to your project repo. You should then
update `work_notes.md` each day with the following:

- What went well (in the context of working on the assignment) today?
- What was particularly interesting or surprising about the topic(s) today?
- What was the most challenging part of the work today, and why?

Project link: https://github.com/DanielMartinAlarcon/TwitOff

## Monday Mar 4
- What went well (in the context of working on the assignment) today?
    - Got all the parts to work, including Jinja templates that render variables and for loops.
- What was particularly interesting or surprising about the topic(s) today?
    - It was neat to actually see all the parts that go into minimal web development. This feels really useful.
- What was the most challenging part of the work today, and why?
    - Knowing which parts of the documentation (Jinja, Flask-SQLalchemy, etc) are actually important for the task at hand.

## Tuesday Mar 5
- What went well (in the context of working on the assignment) today?
    - I managed a complete re-setting of the environments in which I was developing this app, and connected to the APIs for Basilica and Twitter.  I got a lot more familiar with the Flask workflow.
- What was particularly interesting or surprising about the topic(s) today?
    - It's a beauty to see Basilica create embeddings for new lists of tweets, neatly placing them in tweetspace.
- What was the most challenging part of the work today, and why?
    - Something about my environments prevented Python Decouple from working, and it took a couple of hours to sort that out. 

## Wednesday Mar 6
- What went well (in the context of working on the assignment) today?
    - The tweets load, the models predict, and all the parts work together.

- What was particularly interesting or surprising about the topic(s) today?
    - Seeing more complex functions running on a web application. Also, learning to use the python debugger.
- What was the most challenging part of the work today, and why?
    - Keeping track of which applications are in control of which parts of our own app, so that I can look up the proper documentation.


## Thursday Mar 7
- What went well (in the context of working on the assignment) today?
    - IT DEPLOYED.  Also, everything about Heroku is starting to fit together.  It's really neat to see an app out in the real world.

- What was particularly interesting or surprising about the topic(s) today?
    - How many people were saved by the simple instruction of resetting their databases.

- What was the most challenging part of the work today, and why?
    - Error messages in Heroku are only useful some of the time. I still don't quite know how I managed to find my bug in the end.