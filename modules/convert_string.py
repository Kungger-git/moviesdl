import time


class String_Converters:
    """ Convert/Format plural words, time & bytes """

    def plural_s(self, v):
        return 's' if not abs(v) == 1 else ''

    def convert(self, seconds):
        return time.strftime("%H:%M:%S", time.gmtime(seconds))

    def format_bytes(self, size):
        power = 2**10
        n = 0
        power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
        while size > power:
            size /= power
            n += 1
        return f'{round(size, 2)}{power_labels[n]}b'
