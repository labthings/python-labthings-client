# LabThings Python Client

[![LabThings](https://img.shields.io/badge/-LabThings-8E00FF?style=flat&logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4NCjwhRE9DVFlQRSBzdmcgIFBVQkxJQyAnLS8vVzNDLy9EVEQgU1ZHIDEuMS8vRU4nICAnaHR0cDovL3d3dy53My5vcmcvR3JhcGhpY3MvU1ZHLzEuMS9EVEQvc3ZnMTEuZHRkJz4NCjxzdmcgY2xpcC1ydWxlPSJldmVub2RkIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIHN0cm9rZS1taXRlcmxpbWl0PSIyIiB2ZXJzaW9uPSIxLjEiIHZpZXdCb3g9IjAgMCAxNjMgMTYzIiB4bWw6c3BhY2U9InByZXNlcnZlIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxwYXRoIGQ9Im0xMjIuMjQgMTYyLjk5aDQwLjc0OHYtMTYyLjk5aC0xMDEuODd2NDAuNzQ4aDYxLjEyMnYxMjIuMjR6IiBmaWxsPSIjZmZmIi8+PHBhdGggZD0ibTAgMTIuMjI0di0xMi4yMjRoNDAuNzQ4djEyMi4yNGg2MS4xMjJ2NDAuNzQ4aC0xMDEuODd2LTEyLjIyNGgyMC4zNzR2LTguMTVoLTIwLjM3NHYtOC4xNDloOC4wMTl2LTguMTVoLTguMDE5di04LjE1aDIwLjM3NHYtOC4xNDloLTIwLjM3NHYtOC4xNWg4LjAxOXYtOC4xNWgtOC4wMTl2LTguMTQ5aDIwLjM3NHYtOC4xNWgtMjAuMzc0di04LjE0OWg4LjAxOXYtOC4xNWgtOC4wMTl2LTguMTVoMjAuMzc0di04LjE0OWgtMjAuMzc0di04LjE1aDguMDE5di04LjE0OWgtOC4wMTl2LTguMTVoMjAuMzc0di04LjE1aC0yMC4zNzR6IiBmaWxsPSIjZmZmIi8+PC9zdmc+DQo=)](https://github.com/labthings/)
![PyPI](https://img.shields.io/pypi/v/labthings-client)

This is an (extremely early) minimal Python client for LabThings devices

## Installation

```
pip install labthings-client
```

## Usage example

```python
import atexit
from labthings_client.discovery import ThingBrowser

# Create a Thing discoverer
browser = ThingBrowser().open()
# Close the discoverer when this script exits
atexit.register(browser.close)

# Wait for the first found LabThing on the network
thing = browser.wait_for_first()
```

### Managing properties

```python
>>> thing.properties
{'pdfComponentMagicDenoise': <affordances.Property object at 0x00000288F4095548>}

>>> thing.properties.pdfComponentMagicDenoise.set(500) 
500

>>> thing.properties.pdfComponentMagicDenoise.get()    
500

>>> 
```


### Managing actions

```python
>>> thing.actions
{'averageDataAction': <affordances.Action object at 0x00000288F40955C8>}

>>> thing.actions.averageDataAction.args
{'type': <class 'dict'>,
 'properties': {'n': {'format': 'int32',
                      'required': True,
                      'type': <class 'int'>},
                'optlist': {'example': [1, 2, 3],
                            'items': {'format': 'int32', 'type': <class 'int'>},
                            'nullable': True,
                            'required': False,
                            'type': <class 'list'>}},
}

>>> thing.actions.averageDataAction(n=10)       
<tasks.ActionTask object at 0x00000288F40D1348>

>>> thing.actions.averageDataAction(n=10).wait()
[0.0013352326078147302, 0.0008734229673564006, 0.0009756767699519994, 0.0008614760409831329, ...

>>> 
```
