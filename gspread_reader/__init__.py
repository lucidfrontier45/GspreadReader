__author__ = 'du'

import string
import itertools

import gspread


alphabets = list(string.uppercase) + map(lambda (x, y): x + y, itertools.product(string.uppercase, repeat=2))


class GspreadReader():
    def __init__(self, account, passwd, sheet_name=None, sheet_id=0, offset=0, buffer_len=10, return_type="list"):
        gc = gspread.login(account, passwd)
        self._ws = gc.open(sheet_name).get_worksheet(sheet_id)
        s = "{0}1:{1}1".format(alphabets[0], alphabets[30])
        headers = [c.value for c in self._ws.range(s)]
        self._header = headers[:headers.index("")]
        self._header_len = len(self._header)
        self._buffer_len = buffer_len
        self._buffer = []
        self._last = offset + 1
        self._return_type = return_type

    @property
    def header(self):
        return self._header


    def __iter__(self):
        return self

    def next(self):
        if len(self._buffer) == 0:
            s = "{0}{2}:{1}{3}".format(alphabets[0], alphabets[self._header_len - 1], self._last + 1,
                                       self._last + self._buffer_len)
            self._buffer = self._ws.range(s)
            self._last += self._buffer_len
        if self._buffer[0] == "":
            raise StopIteration
        ret = (c.value for c in self._buffer[:self._header_len])
        del self._buffer[:self._header_len]
        if self._return_type == "list":
            return list(ret)
        elif self._return_type == "dict":
            return dict(zip(self._header, ret))
