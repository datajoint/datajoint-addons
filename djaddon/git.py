import git
import inspect
from functools import wraps
import datajoint as dj


def log_git_status(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        ret = func(*args, **kwargs)
        for key in (args[0] - args[0].GitKey()).project().fetch.as_dict:
            args[0].GitKey().log_key(key)
        return ret

    return with_logging


class GitLog:
    def __call__(self, cls):
        class GitKey(dj.Part):
            definition = """
            ->%s
            ---
            sha1        : varchar(40)
            branch      : varchar(50)
            modified    : int   # whether there are modified files or not
            """ % (cls.__name__,)

            def log_key(self, key):
                repo = git.Repo('/'.join(inspect.getabsfile(cls).split('/')[:-1]))
                sha1, branch = repo.head.commit.name_rev.split()
                modified = (repo.git.status().find("modified") > 0) * 1
                key['sha1'] = sha1
                key['branch'] = branch
                key['modified'] = modified
                self.insert1(key)

            _master = cls

        cls.GitKey = GitKey

        GitKey.database = cls.database
        GitKey._connection = cls._connection
        GitKey._heading = dj.Heading()
        GitKey._context = dict(cls._context, **{cls.__name__: cls})
        GitKey().declare()
        GitKey()._prepare()

        cls._make_tuples = log_git_status(cls._make_tuples)

        return cls


gitlog = GitLog()
