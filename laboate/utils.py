import utime


def timeit(func):
    def _(*args, **kwargs):
        start = utime.ticks_ms()
        ret = func(*args, **kwargs)
        stop = utime.ticks_ms()
        print(b'%r took %d ms' % (func, utime.ticks_diff(stop, start)))
        return ret
    return _
