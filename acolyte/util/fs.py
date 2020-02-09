import os
import aiofiles
from pathlib import Path
from random import randint
from functools import wraps


class Filesystem:
    def path_wrapper(func):
        """ Wrap method calls in the make_path call for platform-agnostic calls """
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Change the args to a mutable data structure
            # This feels wrong!
            arg_list = list(args)
            arg_list[0] = self.make_path(arg_list[0])

            return func(self, *tuple(arg_list), **kwargs)
        return wrapper

    @path_wrapper
    async def read_binary_file(self, filepath: str) -> bytes:
        """ Asynchronously read a binary file """
        async with aiofiles.open(filepath, mode="rb") as f:
            return await f.read()

    @path_wrapper
    async def write_binary_file(self, filepath: str, file: bytes) -> None:
        """ Asynchronously write a binary file """
        async with aiofiles.open(filepath, mode="wb") as fp:
            await fp.write(file)

    @path_wrapper
    def remove_file(self, filepath):
        """ Remove a file """
        return os.remove(filepath)

    @path_wrapper
    def get_directory_listing(self, path: str) -> list:
        return os.listdir(path)

    @path_wrapper
    def get_random_file_path(self, path: str) -> str:
        files = self.get_directory_listing(path)
        random_file = Path(files[randint(1, len(files))])
        return str(Path(path) / random_file)

    def make_path(self, path: str) -> str:
        """
            Convert a path to a platform dependant path

            E.g. converts /a/b/c to \a\b\c if you're on Windows
        """
        return str(Path(path))
