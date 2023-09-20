import json

class Db:
    def __init__(self, path, *, default):
        self.path = path
        self.value = default
        self.reload()

    def __enter__(self):
        pass

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(json.dumps(self.value, ensure_ascii=False))

    def reload(self):
        try:
            with open(self.path, encoding="utf-8") as f:
                self.value = json.loads(f.read())
        except FileNotFoundError:
            pass

    def __exit__(self, *extras):
        self.save()

    def __getitem__(self, key):
        return self.value[key]

    def __setitem__(self, key, value):
        self.value[key] = value
