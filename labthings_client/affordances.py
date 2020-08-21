import requests

from .td_parsers import find_self_link
from .json_typing import json_to_typing_basic
from .tasks import ActionTask


class Affordance:
    def __init__(self, title, affordance_description: dict, base_url: str = ""):
        self.title = title
        self.base_url = base_url.strip("/")
        self.affordance_description = affordance_description

        self.url_suffix = find_self_link(self.affordance_description.get("links"))
        self.self_url = f"{self.base_url}{self.url_suffix}"

        self.description = self.affordance_description.get("description")

    def find_verbs(self):
        """Verify available HTTP methods

        Returns:
            [list] -- List of HTTP verb strings
        """
        return requests.options(self.self_url).headers["allow"].split(", ")


class Property(Affordance):
    def __init__(self, title, affordance_description: dict, base_url: str = ""):
        Affordance.__init__(self, title, affordance_description, base_url=base_url)

        self.read_only = self.affordance_description.get("readOnly")
        self.write_only = self.affordance_description.get("writeOnly")

    def __call__(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def get(self):
        if not self.write_only:
            r = requests.get(self.self_url)
            r.raise_for_status()
            return r.json()
        else:
            raise AttributeError("Can't read attribute, is write-only")

    def set(self, *args, **kwargs):
        return self.put(*args, **kwargs)

    def put(self, value):
        if value is None:
            value = {}
        if not self.read_only:
            r = requests.put(self.self_url, json=value)
            r.raise_for_status()
            return r.json()
        else:
            raise AttributeError("Can't set attribute, is read-only")

    def post(self, value):
        if value is None:
            value = {}
        if not self.read_only:
            r = requests.post(self.self_url, json=value)
            r.raise_for_status()
            return r.json()
        else:
            raise AttributeError("Can't set attribute, is read-only")

    def delete(self):
        if not self.read_only:
            r = requests.delete(self.self_url)
            r.raise_for_status()
            return r.json()
        else:
            raise AttributeError("Can't delete attribute, is read-only")


class MozillaProperty(Property):
    def _post_process(self, value):
        if isinstance(value, dict) and self.title in value:
            return value.get(self.title)

    def _pre_process(self, value):
        return {self.title: value}

    def get(self):
        return self._post_process(Property.get(self))

    def put(self, value):
        return self._post_process(Property.put(self, self._pre_process(value)))

    def post(self, value):
        return self._post_process(Property.post(self, self._pre_process(value)))

    def delete(self):
        return self._post_process(Property.delete(self))


class Action(Affordance):
    def __init__(self, title, affordance_description: dict, base_url: str = ""):
        Affordance.__init__(self, title, affordance_description, base_url=base_url)

        self.args = json_to_typing_basic(self.affordance_description.get("input", {}))

    def __call__(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def post(self, *args, **kwargs):

        # Only accept a single positional argument, at most
        if len(args) > 1:
            raise ValueError(
                "If passing parameters as a positional argument, the only argument must be a single dictionary"
            )

        # Single positional argument MUST be a dictionary
        if args and not isinstance(args[0], dict):
            raise TypeError(
                "If passing parameters as a positional argument, the argument must be a dictionary"
            )

        # Use positional dictionary as parameters base
        if args:
            params = args[0]
        else:
            params = {}

        params.update(kwargs)

        r = requests.post(self.self_url, json=params or {})
        r.raise_for_status()

        return ActionTask(r.json())
