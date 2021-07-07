- What went well (in the context of working on the assignment) today?

Had no issues running flask shell, and creting `db.sqlite3` using REPL, was able to add tweets to user model, and make it persists.

- What was particularly interesting or surprising about the topic(s) today?

It's interesting to see how SQLAlchemy works, its versatile irrespective of any specific RDBMS - it let's you work locally on light-weight database at first than move on to powerful PostgreSQL database for production, or final app iteration.  

- What was the most challenging part of the work today, and why?

The most challening was to steer clear of **circular imports** which are notorious to debug. Another was forgeting to commit the database model.
