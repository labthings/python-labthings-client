import requests
from ipaddress import IPv4Address, IPv6Address

from utilities import AttributeDict
from affordances import Property, Action

class FoundThing:
    def __init__(self, name, addresses, port, path, protocol="http"):
        self.name = name
        self.addresses = addresses
        self._address_strings = {
            f"[{address}]" if isinstance(address, IPv6Address) else f"{address}"
            for address in self.addresses
        }
        self.port = port
        self.path = path
        self.protocol = protocol

        self.urls = {
            f"{self.protocol}://{address}:{self.port}{self.path}"
            for address in self._address_strings
        }

        # No initial description
        self.thing_description = {}
        self.properties = AttributeDict()
        self.actions = AttributeDict()

        # Update description
        self.update()

    # Properties from Thing Description
    @property
    def base(self):
        return self.thing_description.get("base", "")

    @property
    def description(self):
        return self.thing_description.get("description", "")

    def update(self):
        self.thing_description = self.fetch_description()
        self.properties = AttributeDict({k: Property(v, base_url = self.base) for k, v in self.thing_description.get("properties", {}).items()})
        self.actions = AttributeDict({k: Action(v, base_url = self.base) for k, v in self.thing_description.get("actions", {}).items()})

    def fetch_description(self):
        for url in self.urls:
            response = requests.get(url)
            if response.json():
                return response.json()
        # If we reach this line, no URL gave a valid JSON response
        raise RuntimeError("No valid Thing Description found")