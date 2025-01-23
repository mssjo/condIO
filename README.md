# CondIO

Utility for conditionally doing I/O on multiple files.
By Mattias Sjö, 2025

## Installation

This is a python package, so just use `pip install` on the directory containing `setup.py`.

## Usage

`CondIO` is a context manager that essentially bundles a number of nested `with open(file, mode) as alias`. Each one is added with `add(enable, file, mode, alias)` (or `add_if_exists` and `add_if_not_exists` which set `enable` according to the existence of `file`), and they are then all opened and closed with a single `with` statement.
Importantly, only those for which `enable == True` are actually opened, which provides a more convenient alternative to conditionals with `contextlib.nullcontext`.
Inside the context,  one can perform read/write operations to all the files, but only the operations done on enabled files will actually happen, removing the need for clumsy conditionals in the potentially complicated code.

Inside `with CondIO().add(...)...add(...) as io`, each file is accessed via `io['alias']` (where `alias` is the file's path if nothing else is specified); such an expression is still valid even if the file is not enabled, but in that case `os.devnull` is returned instead of the actual file, so it will appear empty when reading and silently discard all writes.
One can also use `io.print(string, alias)`, which will print `string` to the file if it is enabled.
If `alias` is omitted, printing is done to `sys.stdout` if `enable_std==True` is set when creating the `CondIO` object (which is the default), and not at all otherwise.

## Example program

This program prints "Hello, world!" in different languages into corresponding files, but only the languages mentioned in the command-line arguments are actually used.
If a file `names.txt` is present, the program says hello to them as well.

```python
import condIO

languages = set(sys.argv[1:])

with (CondIO()
        .add_if_exists('names.txt')
        .add('swedish' in languages, "hej.txt", 'w', alias='sw')
        .add('english' in languages, "hello.txt", 'w', alias='en')
        .add('french' in languages, "bonjour.txt", 'w', alias='fr')
        .add('german' in languages, "guten_tag.txt", 'w', alias='de')
        ) as io:

    io.print("Hej, världen!", 'sw')
    io.print("Hello, world!", 'en')
    io.print("Bonjour, monde !", 'fr')
    io.print("Guten Tag, Welt!", 'de')

    for name in io['names.txt']:
        name = name.strip()
        io.print(f"Hej, {name}!", 'sw')
        io.print(f"Hello, {name}!", 'en')
        io.print(f"Bonjour, {name} !", 'fr')
        io.print(f"Guten Tag, {name}!", 'de')

io.print("All files have been closed, only stdout remains")
```
