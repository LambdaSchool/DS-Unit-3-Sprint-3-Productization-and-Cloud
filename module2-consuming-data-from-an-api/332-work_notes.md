# 332 Assignment

Tuesday | 2019-11-12

## Tobias Reaper

### Repositories

- [DS-Unit-3-Sprint-3-Productization-and-Cloud](https://github.com/tobias-fyi/DS-Unit-3-Sprint-3-Productization-and-Cloud)
- [My Twitoff Repo: `deftwit`](https://github.com/tobias-fyi/deftwit)

## Questions

- What went well (in the context of working on the assignment) today?

First, I actually got my Twitter developer account on time. I thought I may have to make due for today until it was approved. Second, I was able to connect to the API with relative ease.

- What was particularly interesting or surprising about the topic(s) today?

Probably the most interesting thing for me today was learning how to use the API, and the most surprising thing was how easy it was to access a large amount of data on any Twitter users with a public account. I was also very interested in the Basilica embedding, though I didn't have much time to look into that.

- What was the most challenging part of the work today, and why?

The most challenging part of today was debugging the app. I had everything set up such that I knew it should've been working perfectly, with a list of tweets displaying based off of the user's handle, which was passed into the url. I looked around and became very confused when the exact same process (which I'd written into a fuction for the app) worked when I walked through it step by step in the flask shell.

I ended up realizing that I'd been passing a bad parameter into the `.timeline()` method. I'd been passing in `mode="extended"` instead of `tweet_mode="extended"`. The reason for that error was because I'd written a function to make it easier, but had pulled out a bit of it to use in the actual app. I forgot to change the parameter name back to what it should've been.


