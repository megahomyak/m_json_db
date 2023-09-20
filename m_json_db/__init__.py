import json
import threading

class Accessor:

    def __init__(self, value):
        self.value = value
        self.was_mutated = False

    def __getitem__(self, key):
        return self.value[key]

    def __setitem__(self, key, value):
        self.was_mutated = True
        self.value[key] = value

_thread_local_storages = threading.local()

def _get_accessor_stack():
    if not hasattr(_thread_local_storages, "accessor_stack"):
        _thread_local_storages.accessor_stack = []
    return _thread_local_storages.accessor_stack

class Db:
    def __init__(self, path, *, default):
        self.path = path
        self.value = default
        self.taker_thread_id = None
        self.reload()

    def __enter__(self):
        accessor = Accessor(self.value)
        _get_accessor_stack().append(accessor)
        return accessor

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(json.dumps(self.value, ensure_ascii=False))

    def reload(self):
        try:
            with open(self.path, encoding="utf-8") as f:
                self.value = json.loads(f.read())
        except FileNotFoundError:
            pass

    def __exit__(self):
        accessor = _get_accessor_stack().pop()
        if accessor.was_mutated:
            self.save()
