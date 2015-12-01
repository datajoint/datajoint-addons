from numpy.testing import assert_array_equal
import numpy as np
from nose.tools import assert_raises, assert_equal, assert_not_equal, \
    assert_false, assert_true, assert_list_equal, \
    assert_tuple_equal, assert_dict_equal, raises

from . import schema
import datajoint as dj
import os

class TestRelation:
    """
    Test base relations: insert, delete
    """

    def __init__(self):
        self.hdf = schema.HDFTest()

    def test_contents(self):
        """
        Tests whether hdf5 saving works
        """

        n = len(self.hdf)
        self.hdf.to_hdf5('/tmp/tmp.h5')
        self.hdf.delete()
        self.hdf.read_hdf5('/tmp/tmp.h5')
        os.remove('/tmp/tmp.h5')

        assert_equal(len(self.hdf), n, "Original and recovered length are not the same.")


