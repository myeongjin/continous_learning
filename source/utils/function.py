
import time


def mainloop(seconds=0.1):
    try:
        while True:
            time.sleep(seconds)
    except KeyboardInterrupt:
        pass
