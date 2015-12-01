import git
import inspect
from functools import wraps
import datajoint as dj
import os
from datajoint import DataJointError

def _log_git_status(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        ret = func(*args, **kwargs)
        for key in (args[0] - args[0].GitKey()).project().fetch.as_dict:
            args[0].GitKey().log_key(key)
        return ret

    return with_logging


def gitlog(cls):
    """
    Decorator that equips a datajoint class of the type datajoint.Computeed or datajoint.Imported with
    an additional datajoint. Part table that stores the current sha1, the branch, and whether the code
    was modified since the last commit, for the class representing the master table. Use the instantiated
    version of the decorator. Here is an example:

    .. code-block:: python
       :linenos:

        import datajoint as dj
        from djaddon import gitlog

        schema = dj.schema('mydb',locals())

        @schema
        @gitlog
        class MyRelation(dj.Computed):
            definition = ...


    """
    class GitKey(dj.Part):
        definition = """
        ->%s
        ---
        sha1        : varchar(40)
        branch      : varchar(50)
        modified    : int   # whether there are modified files or not
        """ % (cls.__name__,)

        def log_key(self, key):
            path = inspect.getabsfile(cls).split('/')
            for i in reversed(range(len(path))):
                if os.path.exists('/'.join(path[:i]) + '/.git'):
                    repo = git.Repo()
                    break
            else:
                raise DataJointError("%s.GitKey could not find a .git directory for %s" % (cls.__name__, cls.__name__))
            sha1, branch = repo.head.commit.name_rev.split()
            modified = (repo.git.status().find("modified") > 0) * 1
            key['sha1'] = sha1
            key['branch'] = branch
            key['modified'] = modified
            self.insert1(key)

    cls.GitKey = GitKey
    cls._make_tuples = _log_git_status(cls._make_tuples)

    return cls


