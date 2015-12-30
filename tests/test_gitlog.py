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
        self.imp = schema.Imp()

    def test_contents(self):
        """
        Tests whether git keys are properly logged
        """

        self.comp.delete()
        self.comp.populate()
        self.imp.delete()
        self.imp.populate()
        assert_equal(len(self.comp), len(self.comp.GitKey()), "GitKey does not have the same length as master table")
        assert_equal(len(self.imp), len(self.imp.GitKey()), "GitKey does not have the same length as master table")

    def test_lookup_insert(self):
        """
        Test whether insert of gitkey works with lookup tables
        """
        assert_true(len(schema.HDFTest()) == len(schema.HDFTest.GitKey()) > 0, "Nothing was inserted into GitKey")

    def test_manual_insert(self):
        """
        Test whether manual insert of gitkey works with different formats,
        """
        with dj.config(safemode=False):
            schema.Man().delete()
        # insert dictionary
        schema.Man().insert1(dict(idx=0, value=2.))

        # positional insert
        schema.Man().insert1((1, 2.))

        # fetch an np.void, modify, ans insert
        k = schema.Man().fetch.limit(1)()[0]
        k['idx'] = 2
        schema.Man().insert1(k)
        assert_true(len(schema.Man()) == len(schema.Man.GitKey()) == 3,
                    "Inserting with different datatypes did not work")

    def test_decoration(self):
        """
        Tests whether GitKey classes are different
        """

        assert_true(self.comp.GitKey is not self.imp.GitKey, "GitKey ids are the same but should not")
