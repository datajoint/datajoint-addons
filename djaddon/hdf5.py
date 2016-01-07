import pandas as pd
import datajoint as dj
from itertools import filterfalse
import h5py
import importlib


def hdf5(cls):
    """
    Decorator that equips a datajoint class with the ability to save and load it's data from hdf5.
    Internally uses pandas to save and load the data.

    .. code-block:: python
       :linenos:

        import datajoint as dj
        from djaddon import hdf5

        schema = dj.schema('mydb',locals())

        @schema
        @hdf5
        class MyRelation(dj.Computed):
            definition = ...


    """

    def to_hdf5(self, filepath):
        """
        Save the content of this table to the given hdf5 file.

        :param filepath: file path to which the data will be saved
        """
        df = pd.DataFrame(self.fetch())
        df.to_hdf(filepath, cls.__name__)

    def read_hdf5(self, filepath, **kwargs):
        """
        Read contents from hdf5 file into relation. Must haven been saved with `to_hdf5`.

        Keyword arguments are passed on to insert.

        :param filepath: path to the hdf5 file
        """
        df = pd.read_hdf(filepath, cls.__name__)

        for col in df.columns:
            if 'datetime' in df.ftypes[col]:
                df[col] = [str(d) for d in df[col]]
        self.insert((r.to_dict() for _, r in df.iterrows()), **kwargs)

    cls.to_hdf5 = to_hdf5
    cls.read_hdf5 = read_hdf5

    return cls


def _ordered_hierarchy(classes):
    if len(classes) == 0:
        return
    cls = classes[0]
    c = cls()
    erd = c.erd()
    ancestors = [kls for kls in classes[1:] if kls().full_table_name in erd.ancestors(c.full_table_name)]
    non_ancestors = [kls for kls in classes[1:] if kls not in ancestors]

    yield from _ordered_hierarchy(ancestors)
    yield cls
    yield from _ordered_hierarchy(non_ancestors)


def to_hdf5(filename, module):
    """
    Saves all elements from a given module that are subclasses of datajoint.BaseRelation.

    The relations do not need to be decorated with the hdf5 decorator.

    :param filename: filename to save to
    :param module: module containing relations
    """
    classes = [kls for kls in map(lambda c: getattr(module, c), filterfalse(lambda x: x.startswith('__'), dir(module)))
               if issubclass(kls, dj.BaseRelation)]
    assert len(classes) > 0, 'Nothing to save from this module'

    classes[0]().connection.dependencies.load()

    with h5py.File(filename) as fid:
        fid.attrs['rebuild_order'] = ';'.join([str(kls).split("'")[1] for kls in _ordered_hierarchy(classes)])

    for cls in classes:
        if issubclass(cls, dj.BaseRelation):
            print('Saving', cls.__name__)
            klass = hdf5(cls)
            klass().to_hdf5(filename)


def from_hdf5(filename, **kwargs):
    """
    Rebuilds a database that has been saved with to_hdf5.

    :param filename: hdf5 filename
    :param kwargs: keyword arguemnts that will be passed to insert
    """
    with h5py.File(filename, 'r') as fid:
        rebuild_order = fid.attrs['rebuild_order'].split(';')

    for path in rebuild_order:
        module_name, class_name = path.rsplit(".", 1)
        cls = getattr(importlib.import_module(module_name), class_name)
        klass = hdf5(cls)
        klass().read_hdf5(filename, **kwargs)
