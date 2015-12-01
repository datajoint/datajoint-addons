"""
Sample scheme with realistic tables for testing
"""

import random
import numpy as np
import datajoint as dj
from . import PREFIX, CONN_INFO
from djaddon import hdf5, gitlog

schema = dj.schema(PREFIX + '_test1', locals(), connection=dj.conn(**CONN_INFO))


@schema
class Index(dj.Lookup):
    definition = """
    idx : int
    """

    @property
    def contents(self):
        yield from zip(range(10))


@schema
@gitlog
class Comp(dj.Computed):
    definition = """
    ->Index
    ---
    value : double
    """

    def _make_tuples(self, key):
        key['value'] = np.random.randn()
        self.insert1(key)

@schema
@hdf5
class HDFTest(dj.Lookup):
    definition = """
    idx     : int
    ---
    value   : double
    str     : varchar(10)
    range   : longblob
    random  : longblob
    """

    contents = [
        (0, 1., 'number 1', np.arange(5), np.random.randn(10, 2)),
        (1, 2., 'number 2', np.arange(5, 10), np.random.randn(10, 2)),
    ]

@schema
@gitlog
class Imp(dj.Imported):
    definition = """
    ->Index
    ---
    measurement : double
    """

    def _make_tuples(self, key):
        key['measurement'] = np.random.randn()
        self.insert1(key)

