import time


class StringConverter:
    """ Convert/Format plural words, time & bytes """

    @staticmethod
    def pluralS(v):
        return 's' if not abs(v) == 1 else ''

    @staticmethod
    def convertTime(seconds):
        return time.strftime("%H:%M:%S", time.gmtime(seconds))

    @staticmethod
    def formatBytes(size):
        power = 2**10
        n = 0
        power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
        while size > power:
            size /= power
            n += 1
        return "{}{}b".format(round(size, 2), power_labels[n])
