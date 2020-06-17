import requests


class ActionTask:
    def __init__(self, task_description: dict):
        self.task_description = task_description
        self.self_url = self.task_description.get("href")

        self._value = None

    def update(self):
        r = requests.get(self.self_url)
        r.raise_for_status()
        self.task_description = r.json()

    @property
    def status(self):
        return self.task_description.get("status")

    @property
    def log(self):
        return self.task_description.get("log")

    @property
    def value(self):
        if not self._value:
            if not self.task_description.get("return"):
                self.update()
            self._value = self.task_description.get("return")
        return self._value

    def wait(self):
        """Poll the task until it finishes, and return the return value"""
        log_n = 0
        while self.status in ["running", "idle"]:
            self.update()
            while len(self.log) > log_n:
                d = self.log[log_n]
                logging.log(d["levelno"], d["message"])
                log_n += 1
        return self.value
