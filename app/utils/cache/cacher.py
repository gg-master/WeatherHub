import datetime
import functools
import pickle
import os
import time
from typing import Callable
from hashlib import md5


ENABLE_CACHE = True


class Cacher:
    def __init__(self, nargs=0):
        self._nargs = nargs

    def __call__(self, func) -> Callable:
        pass


class AsyncPickleCacher(Cacher):
    DEFAULT_PATH = "cache/"
    CACHE_LIVE_TIME = 600  # seconds
    FUNC_CALL_DELTA = 10  # seconds

    def __init__(self, nargs=0):
        super().__init__(nargs)

    @staticmethod
    def compute_hash(tuple):
        m = md5()
        for obj in tuple:
            m.update(str(obj).encode())
        return m.hexdigest()

    def __call__(self, func) -> Callable:
        @functools.wraps(func)
        async def _func_cached_wrapper(*args, **kwargs):
            if not os.path.isdir(self.DEFAULT_PATH):
                os.mkdir(self.DEFAULT_PATH)
            time_measure = time.time()
            cached_args = tuple(args[: self._nargs]) + tuple([func.__name__])
            filename = AsyncPickleCacher.compute_hash(cached_args)
            is_reload_required = True
            filepath = os.path.join(self.DEFAULT_PATH, filename)
            if os.path.exists(filepath):
                with open(filepath, "rb") as fobj:
                    data = pickle.load(fobj)
                    if hasattr(data, "_cached_timestamp"):
                        cache_age = time_measure - data._cached_timestamp
                        if cache_age <= self.CACHE_LIVE_TIME:
                            is_reload_required = False
            if is_reload_required:
                if hasattr(func, "_called_timestamp"):
                    if time_measure - func._called_timestamp <= self.FUNC_CALL_DELTA:
                        time.sleep(
                            self.FUNC_CALL_DELTA - time_measure + func._called_timestamp
                        )
                result = await func(*args, **kwargs)
                result._cached_timestamp = int(datetime.datetime.now().timestamp())
                func._called_timestamp = int(datetime.datetime.now().timestamp())
                with open(filepath, "wb") as fobj:
                    pickle.dump(result, fobj, protocol=pickle.HIGHEST_PROTOCOL)
                return result
            else:
                return data

        if ENABLE_CACHE:
            return _func_cached_wrapper
        else:
            return func
