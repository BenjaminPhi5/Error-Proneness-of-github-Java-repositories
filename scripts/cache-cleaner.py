import os

"""
note this is for gradle projects only.

The cache of the ~/.gradle folder leaves broken symbolic links when the repository is deleted.
in particular the fileHashes folder needs an empty lock file
there may be some other cache files that need to be cleaned too.

so this script will go the the relevant folder and clean on the caches
"""


def gradle_cache_clean():
    # remove the lock file if it exists
    try:
        os.remove(os.path.expanduser("~/.gradle/caches/5.5/fileHashes/fileHashes.lock"))
    except FileNotFoundError as e:
        print("file didn't exist anyway ", e.errno)

    # recreate the file, with nothing in it
    file_hash_lock = open(os.path.expanduser("~/.gradle/caches/5.5/fileHashes/fileHashes.lock"), "x")

    # close the file
    file_hash_lock.close()


gradle_cache_clean()