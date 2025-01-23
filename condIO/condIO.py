
import sys, os.path

class CondIO:
    """
    Context manager that contains a number of conditionally enabled input/output files.

    Files can be added using add (see its documentation) and thereafter accessed with
    as if this object was a dict of files.
    They are all opened and closed when this manager is entered and exited.

    Files that are added but not enabled are not opened, and attempting to access one
    will return an empty iterable.
    This class also provides a print function that only performs the print operation if the target file is active (see its documentation).
    """

    class _io:
        def __init__(self, enable, path, mode):
            self._enabled = enable
            self._path = path
            self._mode = mode
            self._file = None

    def __init__(self, enable_std=True, ios=[]):
        """
        Create a multiplexer.

        Arguments:
        enable_std -- if True, the multiplexer will print to stdout when no other file is specified.
        ios -- an array of files to be added (each element should be a set of arguments for the add method)
        """
        self._enable_std = enable_std
        self._ios = {}
        for io in ios:
            self.add(*io)

    def add(self, enable, path, mode='r', alias=None):
        """
        Add a file to the multiplexer.

        Arguments:
        enable -- the file is only open and operated on if this is True
        path -- the path to the file
        mode -- the file is opened with open(path, mode) (defaults to 'r')
        alias -- the file is accessed with self[alias] (defaults to path)

        Returns:
        self, to allow chaining
        """

        self._ios[alias if alias is not None else path] = self._io(enable, path, mode)
        return self

    def add_if_exists(self, path, mode='r', alias=None):
        """ Like add, enabled if path exists """
        return self.add(os.path.isfile(path), path, mode, alias)
    def add_if_not_exists(self, path, mode='r', alias=None):
        """ Like add, enabled if path does not exist """
        return self.add(not os.path.isfile(path), path, mode, alias)


    def print(self, string, where=None):
        """
        Print to a stream if it is enabled.

        Arguments:
        string -- the string to be printed
        where -- the name/alias of a file; if omitted, printing is done to stdout
        """
        if where is None:
            if self._enable_std:
                print(string)
        elif where not in self._ios:
            raise KeyError(f"No multiplexed input/output called '{where}'")
        elif self._ios[where]._enabled:
            print(string, file=self._ios[where]._file)

    def __enter__(self):
        for io in self._ios.values():
            io._file = open(io._path if io._enabled else os.devnull, io._mode)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # TODO: handle exc_type, exc_val, exc_tb
        for io in reversed(self._ios.values()):
            io._file.close()

    def __getitem__(self, key):
        if key not in self._ios:
            raise KeyError(f"No multiplexed input/output called '{key}'")
        return self._ios[key]._file

import sys,os.path

def main():
    languages = set(sys.argv[1:])

    with (CondIO()
            .add_if_exists('names.txt')
            .add('english' in languages, "hello.txt", 'w', alias='en')
            .add('french' in languages, "bonjour.txt", 'w', alias='fr')
            .add('german' in languages, "guten_tag.txt", 'w', alias='de')
            .add('swedish' in languages, "hej.txt", 'w', alias='sw')
            ) as io:

        io.print("Hello, world!", 'en')
        io.print("Bonjour, monde !", 'fr')
        io.print("Guten Tag, Welt!", 'de')
        io.print("Hej, världen!", 'sw')

        for name in io['names.txt']:
            name = name.strip()
            io.print(f"Hello, {name}!", 'en')
            io.print(f"Bonjour, {name} !", 'fr')
            io.print(f"Guten Tag, {name}!", 'de')
            io.print(f"Hej, {name}!", 'sw')

    io.print("All files have been closed, only stdio remains")

if __name__ == '__main__':
    main()

