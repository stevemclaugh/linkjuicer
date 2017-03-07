import sys
import re

# A progress bar!
class ProgressBar(object):
    DEFAULT = 'Progress: %(bar)s %(percent)3d%%'
    FULL = '%(bar)s %(current)d/%(total)d (%(percent)3d%%) %(remaining)d to go'

    def __init__(self, total, width=40, fmt=DEFAULT, symbol='=',
                 output=sys.stderr):
        assert len(symbol) == 1

        self.total = total
        self.width = width
        self.symbol = symbol
        self.output = output
        self.fmt = re.sub(r'(?P<name>%\(.+?\))d',
            r'\g<name>%dd' % len(str(total)), fmt)

        self.current = 0

    def __call__(self):
        percent = self.current / float(self.total)
        size = int(self.width * percent)
        remaining = self.total - self.current
        bar = '[' + self.symbol * size + ' ' * (self.width - size) + ']'

        args = {
            'total': self.total,
            'bar': bar,
            'current': self.current,
            'percent': percent * 100,
            'remaining': remaining
        }
        print('\r' + self.fmt % args, file=self.output, end='')

    def done(self):
        self.current = self.total
        self()
        print('', file=self.output)

# For incremental updates of a file. Useful when a file should be updated
# incrementally but the update values are in, e.g. a set, and you can't
# be sure which ones have already been written.
class UniqueFileWrite(object):

    def __init__(self, fileObject):
        self.fileObject = fileObject
        self.inFile = set()

    def update_file(self, iterable):
        currentObjects = set(iterable)
        newObjects = currentObjects.difference(self.inFile)
        for obj in newObjects:
            self.fileObject.write(str(obj) + "\n")
        self.inFile.update(currentObjects)

    def update_file_and_flush(self,iterable):
        self.update_file(iterable)
        self.fileObject.flush()
