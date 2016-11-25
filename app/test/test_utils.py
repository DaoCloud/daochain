from __future__ import absolute_import

import unittest

from app.utils import parse_image_name

_IMAGE_NAME_TEST_DATA = \
    '''
    python                                              ,registry-1.docker.io,library,python,latest
    python:1.1                                          ,registry-1.docker.io,library,python,1.1
    revol/python                                        ,registry-1.docker.io,revol  ,python,latest
    revol/python:1.1                                    ,registry-1.docker.io,revol  ,python,1.1
    revol/python@sha256:5a35100239643bfe                ,registry-1.docker.io,revol  ,python,sha256:5a35100239643bfe

    daocloud.io/python                                  ,daocloud.io         ,library,python,latest
    daocloud.io/python:1.1                              ,daocloud.io         ,library,python,1.1
    daocloud.io/revol/python                            ,daocloud.io         ,revol  ,python,latest
    daocloud.io/revol/python:1.1                        ,daocloud.io         ,revol  ,python,1.1
    daocloud.io/revol/python@sha256:5a35100239643bfe    ,daocloud.io         ,revol  ,python,sha256:5a35100239643bfe

    localhost/python                                    ,localhost           ,       ,python,latest
    localhost/python:1.1                                ,localhost           ,       ,python,1.1
    localhost/revol/python                              ,localhost           ,revol  ,python,latest
    localhost/revol/python:1.1                          ,localhost           ,revol  ,python,1.1
    localhost/revol/python@sha256:5a35100239643bfe      ,localhost           ,revol  ,python,sha256:5a35100239643bfe

    localhost:5000/python                               ,localhost:5000      ,       ,python,latest
    localhost:5000/python:1.1                           ,localhost:5000      ,       ,python,1.1
    localhost:5000/revol/python                         ,localhost:5000      ,revol  ,python,latest
    localhost:5000/revol/python:1.1                     ,localhost:5000      ,revol  ,python,1.1
    localhost:5000/revol/python@sha256:5a35100239643bfe ,localhost:5000      ,revol  ,python,sha256:5a35100239643bfe

    10.0.0.1/python                                     ,10.0.0.1            ,       ,python,latest
    10.0.0.1/python:1.1                                 ,10.0.0.1            ,       ,python,1.1
    10.0.0.1/revol/python                               ,10.0.0.1            ,revol  ,python,latest
    10.0.0.1/revol/python:1.1                           ,10.0.0.1            ,revol  ,python,1.1
    10.0.0.1/revol/python@sha256:5a35100239643bfe       ,10.0.0.1            ,revol  ,python,sha256:5a35100239643bfe

    aaa:5000/python                                     ,aaa:5000            ,       ,python,latest
    aaa:5000/python:1.1                                 ,aaa:5000            ,       ,python,1.1
    aaa:5000/revol/python                               ,aaa:5000            ,revol  ,python,latest
    aaa:5000/revol/python:1.1                           ,aaa:5000            ,revol  ,python,1.1
    aaa:5000/revol/python@sha256:5a35100239643bfe       ,aaa:5000            ,revol  ,python,sha256:5a35100239643bfe
    '''.strip().replace(' ', '').splitlines()
IMAGE_NAME_TEST_DATA = (x.split(',') for x in _IMAGE_NAME_TEST_DATA if x)


class MyTestCase(unittest.TestCase):
    def test_parse_image_name(self):
        for line in IMAGE_NAME_TEST_DATA:
            _input = line[0]  # raw_name
            _output = tuple(line[1:])  # registry, default_namespace, name, tag
            self.assertEqual(parse_image_name(_input), _output)


if __name__ == '__main__':
    unittest.main(verbosity=2)
