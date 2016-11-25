# encoding=utf-8
from __future__ import print_function

import base64
import functools
import json
import os
import re
import string
import sys
from inspect import getargspec
from inspect import getdoc

from docopt import DocoptExit, docopt


def gen_random_str(length):
    return base64.b32encode(os.urandom(3 * length))[:length].lower()


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


def parse_image_name(raw_name):
    DEFAULT_REGISTRY_NAMESPACE = 'library'
    DEFAULT_IMAGE_TAG = 'latest'
    DEFAULT_REGISTRY_URL = 'registry-1.docker.io'
    IS_REGISTRY = re.compile(r'\.|:|localhost')
    IS_NONE_PRIVATE_REGISTRY = re.compile(DEFAULT_REGISTRY_URL + r'|daocloud.io')

    def _name_tag(n):
        s = n.split('@')
        if len(s) != 1:
            return s[0], s[1]

        s = n.split(':')
        if len(s) == 1:
            return n, DEFAULT_IMAGE_TAG
        # elif len(s) == 2:
        else:
            return s[0], s[1]

    is_registry = lambda x: bool(IS_REGISTRY.search(x))
    is_none_private_registry = lambda x: bool(IS_NONE_PRIVATE_REGISTRY.search(x))
    raw_name = raw_name.strip()
    splited_name = raw_name.split('/')
    # deal with default registry
    name, tag = _name_tag(splited_name[-1])
    if len(splited_name) == 1:
        registry = DEFAULT_REGISTRY_URL
        namespace = DEFAULT_REGISTRY_NAMESPACE
    elif len(splited_name) == 2 and not is_registry(splited_name[0]):
        registry = DEFAULT_REGISTRY_URL
        namespace = splited_name[0]
    # deal with none private
    elif len(splited_name) == 2 and is_none_private_registry(splited_name[0]):
        registry = splited_name[0]
        namespace = DEFAULT_REGISTRY_NAMESPACE
    elif len(splited_name) == 3 and is_none_private_registry(splited_name[0]):
        registry = splited_name[0]
        namespace = splited_name[1]
    # deal with private registry
    elif len(splited_name) == 2 and is_registry(splited_name[0]):
        registry = splited_name[0]
        namespace = ''
    # elif len(splited_name) == 2 and is_registry(splited_name[0]):
    else:
        registry = splited_name[0]
        namespace = splited_name[1]
    return registry, namespace, name, tag
