# buffer.py
from collections import deque

class StreamBuffer:
    """
    Simple in-memory buffer for live updates
    """
    def __init__(self, max_len=500):
        self.buffer = deque(maxlen=max_len)

    def append(self, item):
        self.buffer.append(item)

    def get_all(self):
        return list(self.buffer)