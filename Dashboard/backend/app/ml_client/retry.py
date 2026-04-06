# retry.py
import time

def retry_request(func, *args, retries=3, delay=1, **kwargs):
    for i in range(retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if i < retries - 1:
                time.sleep(delay)
            else:
                raise e