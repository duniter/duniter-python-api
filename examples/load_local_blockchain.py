# this example lets you load locally copy of duniter blockchain into duniterpy objects
# by default, it searches in ~/.config/duniter/duniter_default/g1/

from duniterpy.helpers.blockchain import load

bc = load()  # gets blockchain iterator
b = next(bc)  # gets block
b.number  # should return 0
# you can access all properties of this block through it's duniterpy objects attributes
next(bc).number  # should return 1
next(bc).number  # should return 2 (and so on)
