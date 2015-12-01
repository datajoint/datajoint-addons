# datajoint-addons

A collection of addons and nice-to-haves for datajoint-python

## gitlog

A decorator for `dj.Computed` and `dj.Imported`. Here is an example how to use it

```python

  import datajoint as dj
  from djaddon import gitlog

  schema = dj.schema('mydb',locals())

  @schema
  @gitlog
  class MyRelation(dj.Computed):
      definition = """
      # example table
      ->SomeForeignKey
      idx     : int # some index
      ---
      value   : double # some value
      """

      def _make_tuples(self, key):
        ...
```

The `@gitlog` decorator will add a member class called `GitKey` with tier `dj.Part` to `MyRelation` that stores the sha1, the branch, and whether currently modified files exist for the directory `MyRelation` lives in for each entry computed with `_make_tuples`.

## hdf5

Adds the functions `to_hdf5` and `read_hdf5` to a relation. These functions can save and load the table to and from hdf5 files.

```python
 import datajoint as dj
 from djaddon import hdf5

 schema = dj.schema('mydb',locals())

 @schema
 @hdf5
 class MyRelation(dj.Computed):
     definition = ...
```
