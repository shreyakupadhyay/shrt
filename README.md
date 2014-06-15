#Chota
Chota - meaning short in Urdu - is an awesome url shortener written in `Flask` as my personal project to dive deeper into flask, it is simple yet powerful. Fork this repo and play around with it, don't forget to make pull requests and make it even better. See the app in [action](http://chota-tk.herokuapp.com/).
<a href="http://imgur.com/KEIT77n"><img src="http://i.imgur.com/KEIT77n.png" title="Hosted by imgur.com" /></a>

###Installation:
 - Clone this repo ```git clone https://github.com/itsnauman/chota.git```
 - Install the requirements, only Flask is required though ```pip install -r requirements.txt```

###Setting up a development enviroment:
Edit `__init__.py` and provide your db path instead of `os.environ['DATABASE_URL']` - as this is setup for heroku, also add `db.create_all()` in the `runserver.py` file to create the db when you run the app for the first time. That's all, Run the `runserver.py` file and boom, you are up and running :)

###Api:
The api is very basic at the moment and needs a lot of improvement but it gets the job done, in order to shorten a url, send a GET request to chota-tk.herokuapp.com/api with long url.
Request:
```
curl http://chota-tk.herokuapp.com/api/google.com
```
Response:
```
{
  "short_url": "http://chota-tk.herokuapp.com/czidce",
  "success": true
}
```
###Contributing:
 - Improve loading speed
 - Tests

###License:
Chota is distributed under MIT license, see license for more details.
