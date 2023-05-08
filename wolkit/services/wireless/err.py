
class WatcherNotFoundError(ValueError):
    def __init__(self, watcher_id: int):
        super().__init__(f"watcher with id {watcher_id} not found")
