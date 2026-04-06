# queue.py
from queue import Queue

frame_queue = Queue(maxsize=1000)

def enqueue(frames):
    for frame in frames:
        frame_queue.put(frame)

def dequeue_batch(batch_size=50):
    items = []
    for _ in range(batch_size):
        if not frame_queue.empty():
            items.append(frame_queue.get())
    return items