# LabThings Python Client

This is an (extremely early) minimal Python client for LabThings devices

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
