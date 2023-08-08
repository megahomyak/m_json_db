import json

class Db:
    def __init__(self, path, *, default):
        self.path = path
        try:
            with open(path, encoding="utf-8") as f:
                self.value = json.loads(f.read())
        except FileNotFoundError:
            self.value = default

    def __enter__(self):
        pass

    def __exit__(self, *args):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(json.dumps(self.value, ensure_ascii=False))

    def __getattr__(self, attrname):
        getattr(self.value, attrname)

__all__ = ["Db"]
