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

## slack.notify_user

Decorator for `Computed` and `Imported` classes that notifies a user on slack via direct message that the `populate` is done. 

```python
import datajoint as dj
from djaddon.slack import notify_user

schema = dj.schema('datajoint_test',locals())

@schema
class Iterations(dj.Lookup):
    definition = """
    idx    : int
    ---
    """

    contents = list(zip(range(10)))

@schema
@notify_user('fabee', '<your slack API token>')
class Computations(dj.Computed):
    definition = """
    -> Iterations
    ---
    value      : float
    """

    def _make_tuples(self, key):
        key['value'] = 2
        self.insert1(key)


if __name__=="__main__":
    Computations().populate()

```
