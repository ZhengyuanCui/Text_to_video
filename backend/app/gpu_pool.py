import threading
import itertools
import torch

_lock = threading.Lock()
_device_iter = itertools.cycle(range(torch.cuda.device_count()))

def next_device():
    with _lock:
        return next(_device_iter)
