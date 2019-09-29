import time
import re
import os
import stat
import logging
import datetime
import logging.handlers as handlers


class SizedRotatingFileHandler(handlers.TimedRotatingFileHandler):
    """
    Handler for logging to a set of files, which switches from one file
    to the next when the current file reaches a certain size, or at certain
    timed intervals
    """

    def __init__(self, filename, maxBytes=0, backupCount=0, encoding=None,
                 delay=0, when='h', interval=1, utc=False):
        handlers.TimedRotatingFileHandler.__init__(
            self, filename, when, interval, backupCount, encoding, delay, utc)
        self.maxBytes = maxBytes

    def shouldRollover(self, record):
        """
        Determine if rollover should occur.

        Basically, see if the supplied record would cause the file to exceed
        the size limit we have.
        """
        # delay was set...
        msg = record
        if self.stream is None:
            # due to non-posix-compliant Windows feature
            #self.stream.seek(0, 2)
            self.stream = self._open()
        if self.maxBytes > 0:                   # are we rolling over?
            if self.stream.tell() + len(str(msg)) >= self.maxBytes:
                print('roll over')
                return 1
        t = int(time.time())
        return 0



