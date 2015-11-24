from numpy.testing import assert_array_equal
import numpy as np
from nose.tools import assert_raises, assert_equal, assert_not_equal, \
    assert_false, assert_true, assert_list_equal, \
    assert_tuple_equal, assert_dict_equal, raises

from . import schema
from pymysql import IntegrityError, ProgrammingError
import datajoint as dj
from datajoint import utils
from unittest.mock import patch


class TestRelation:
    """
    Test base relations: insert, delete
    """

    def __init__(self):
        self.comp = schema.Comp()

    def test_contents(self):
        """
        Tests whether git keys are properly logged
        """

        self.comp.delete()
        self.comp.populate()
        assert_equal(len(self.comp), len(self.comp.GitKey()), "GitKey does not have the same length as master table")

