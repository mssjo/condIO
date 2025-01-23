import sys
from condIO import CondIO

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
