# encoding=utf-8
from __future__ import print_function

import functools
import json
import re
import string
import sys
from inspect import getargspec
from inspect import getdoc

from docopt import DocoptExit, docopt


def hex_to_uint(s):
    return int(s, 16)


def uint_to_hex(n):
    return hex(n)[:-1]


def bytes_to_str(b):
    b = b[2:]
    n = 2
    b_a = [b[i:i + n] for i in range(0, len(b), n)]
    return "".join([chr(int(ib, 16)) for ib in b_a])


def print_dict(d, prefix=''):
    """
    :type d: dict
    """
    for k, v in d.items():
        if isinstance(v, dict):
            print('%s%s:' % (prefix, k))
            print_dict(v, prefix + ' ' * 4)
        else:
            print('%s%s = %s' % (prefix, k, v))


def memoize(fn):
    cache = fn.cache = {}

    @functools.wraps(fn)
    def _memoize(*args, **kwargs):
        kwargs.update(dict(zip(getargspec(fn).args, args)))
        key = tuple(kwargs.get(k, None) for k in getargspec(fn).args)
        if key not in cache:
            cache[key] = fn(**kwargs)
        return cache[key]

    return _memoize


def load_json_from(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def dump_to(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


class Template(string.Template):
    delimiter = '^^'


def load_template(filename):
    with open(filename, 'r') as f:
        s = f.read()
        return Template(s).substitute


class NoSuchCommand(Exception):
    def __init__(self, command, supercommand):
        super(NoSuchCommand, self).__init__("No such command: %s" % command)

        self.command = command
        self.supercommand = supercommand


def docopt_full_help(docstring, *args, **kwargs):
    try:
        return docopt(docstring, *args, **kwargs)
    except DocoptExit:
        raise SystemExit(docstring)


class DocoptCommand(object):
    def docopt_options(self):
        return {'options_first': True}

    def sys_dispatch(self):
        self.dispatch(sys.argv[1:], None)

    def dispatch(self, argv, global_options):
        self.perform_command(*self.parse(argv, global_options))

    def perform_command(self, *args):
        raise NotImplementedError()

    def parse(self, argv, global_options):
        command_help = getdoc(self)
        options = docopt_full_help(getdoc(self), argv, **self.docopt_options())
        command = options['COMMAND']

        if command is None:
            raise SystemExit(command_help)

        handler = self.get_handler(command)
        docstring = getdoc(handler)

        if docstring is None:
            raise NoSuchCommand(command, self)

        command_options = docopt_full_help(docstring, options['ARGS'], options_first=True)
        return options, handler, command_options

    def get_handler(self, command):
        command = command.replace('-', '_')

        if not hasattr(self, command):
            raise NoSuchCommand(command, self)

        return getattr(self, command)


def parse_doc_section(name, source):
    pattern = re.compile('^([^\n]*' + name + '[^\n]*\n?(?:[ \t].*?(?:\n|$))*)',
                         re.IGNORECASE | re.MULTILINE)
    return [s.strip() for s in pattern.findall(source)]


def wrap_print(array, n, prefix='', sep=' '):
    maxlen = max([len(s) for s in array])
    fmt = '%-' + str(maxlen) + 's' + sep
    print(prefix, end='')
    for i, v in enumerate(array):
        if i % n == 0 and i:
            print('\n%s' % prefix, end='')
        print(fmt % v, end='')
