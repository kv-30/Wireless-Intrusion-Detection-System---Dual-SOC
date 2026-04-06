# backpressure.py
from app.core.queue import frame_queue

def is_overloaded():
    """
    Check if the queue is too full
    """
    return frame_queue.qsize() > 800  # example threshold