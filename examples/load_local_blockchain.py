"""
Copyright  2014-2020 Vincent Texier <vit@free.fr>

DuniterPy is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

DuniterPy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


# this example lets you load locally copy of duniter blockchain into duniterpy objects
# by default, it searches in ~/.config/duniter/duniter_default/g1/

from duniterpy.helpers.blockchain import load

bc = load()  # gets blockchain iterator
b = next(bc)  # gets block
print(f"first block number is: {b.number}")  # should return 0
# you can access all properties of this block through it's duniterpy objects attributes
print(f"second block number is: {next(bc).number}")  # should return 1
print(f"third block number is: {next(bc).number}")  # should return 2
# (and so on)
