import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, FileSystemEventHandler

"""
Extremely simple implementation of a file watcher and hot reload for python using watchdog.
"""


class MyHandler(FileSystemEventHandler):
    # def on_created(self, event: FileSystemEvent) -> None:
    #     print(f'event type: {event.event_type}  path : {event.src_path}')
    #     return super().on_created(event)

    def on_modified(self, event: FileSystemEvent) -> None:
        print(f'event type: {event.event_type}  path : {event.src_path}')

        # Format path
        formatted_path = event.src_path.replace('\\', '/').replace('./', '')

        try:
            with open(formatted_path, 'r') as file:
                file_contents = file.read()
                # print(file_contents)
                exec(file_contents)

        except Exception as e:
            print(e)

        return super().on_modified(event)

    # def on_deleted(self, event: FileSystemEvent) -> None:
    #     print(f'event type: {event.event_type}  path : {event.src_path}')
    #     return super().on_deleted(event)

    # def on_any_event(self, event: FileSystemEvent) -> None:
    #     print(f'event type: {event.event_type}  path : {event.src_path}')
    #     return super().on_any_event(event)

    # def on_opened(self, event: FileSystemEvent) -> None:
    #     print(f'event type: {event.event_type}  path : {event.src_path}')
    #     return super().on_opened(event)

    # def on_closed(self, event: FileSystemEvent) -> None:
    #     print(f'event type: {event.event_type}  path : {event.src_path}')
    #     return super().on_closed(event)

    # def on_moved(self, event: FileSystemEvent) -> None:
    #     print(f'event type: {event.event_type}  path : {event.src_path}')
    #     return super().on_moved(event)


if __name__ == "__main__":
    path = "./src"  # sys.argv[1] if len(sys.argv) > 1 else '.'

    logging.info(   f'start watching directory {path!r}')

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
