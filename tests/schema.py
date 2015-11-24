"""
Sample scheme with realistic tables for testing
"""

import random
import numpy as np
import datajoint as dj
from . import PREFIX, CONN_INFO
from djaddon import gitlog

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


