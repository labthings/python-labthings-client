from zeroconf import ServiceBrowser, Zeroconf
import ipaddress
import logging
import time

from pprint import pprint

from .thing import FoundThing

class Browser:
    def __init__(self, types=["labthing", "webthing"], protocol="tcp"):
        self.service_types = [f"_{service_type}._{protocol}.local." for service_type in types]

        self.services = {}

        self.add_service_callbacks = set()
        self.remove_service_callbacks = set()

        self._zeroconf = Zeroconf()
        self._browsers = set()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self ,type, value, traceback):
        return self.close()

    def open(self):
        for service_type in self.service_types:
            self._browsers.add(ServiceBrowser(self._zeroconf, service_type, self))
        return self

    def close(self, *args, **kwargs):
        logging.info(f"Closing browser {self}")
        return self._zeroconf.close(*args, **kwargs)

    def remove_service(self, zeroconf, type, name):
        service = zeroconf.get_service_info(type, name)
        if name in self.services:
            for callback in self.remove_service_callbacks:
                callback(self.services[name])
            del self.services[name]

    def add_service(self, zeroconf, type, name):
        service = zeroconf.get_service_info(type, name)
        self.services[name] = parse_service(service)
        for callback in self.add_service_callbacks:
            callback(self.services[name])

    ### TODO: The names of these functions are an abomination and should be renamed
    def add_add_service_callback(self, callback, run_on_existing: bool = True):
        self.add_service_callbacks.add(callback)
        if run_on_existing:
            for service in self.services:
                callback(service)

    def remove_add_service_callback(self, callback):
        self.add_service_callbacks.discard(callback)

    def add_remove_service_callback(self, callback):
        self.remove_service_callbacks.add(callback)

    def remove_add_service_callback(self, callback):
        self.remove_service_callbacks.discard(callback)


class ThingBrowser(Browser):
    def __init__(self, *args, **kwargs):
        Browser.__init__(self, *args, **kwargs)
        self._things = set()
        self.add_add_service_callback(self.add_service_to_things)
        self.add_remove_service_callback(self.remove_service_from_things)
        
    @property
    def things(self):
        return list(self._things)

    def add_service_to_things(self, service):
        self._things.add(service_to_thing(service))

    def remove_service_from_things(self, service):
        discards = set()
        for thing in self._things:
            if thing.name == service.get("name"):
                discards.add(thing)
        for discard_thing in discards:
            self._things.discard(discard_thing)

    def wait_for_first(self):
        while len(self.things) == 0:
            time.sleep(0.1)
        return self.things[0]

def parse_service(service):
    properties = {}
    for k, v in service.properties.items():
        properties[k.decode()] = v.decode()

    return {
        "address": ipaddress.ip_address(service.address),
        "addresses": {ipaddress.ip_address(a) for a in service.addresses},
        "port": service.port,
        "name": service.name,
        "server": service.server,
        "properties": properties,
    }


def service_to_thing(service: dict):
    if not ("addresses" in service or "port" in service or "path" in service.get("properties", {})):
        raise KeyError("Invalid service. Missing keys.")
    return FoundThing(service.get("name"), service.get("addresses"), service.get("port"), service.get("properties").get("path"))


if __name__ == "__main__":
    import atexit
    import time

    logging.getLogger().setLevel(logging.DEBUG)

    browser = ThingBrowser().open()
    atexit.register(browser.close)

    thing = browser.wait_for_first()