#  Pyrofork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#
#  This file is part of Pyrofork.
#
#  Pyrofork is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrofork is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrofork.  If not, see <http://www.gnu.org/licenses/>.

import re
from struct import unpack

# SMP = Supplementary Multilingual Plane: https://en.wikipedia.org/wiki/Plane_(Unicode)#Overview
SMP_RE = re.compile(r"[\U00010000-\U0010FFFF]")


def add_surrogates(text):
    # Replace each SMP code point with a surrogate pair
    return SMP_RE.sub(
        lambda match:  # Split SMP in two surrogates
        "".join(chr(i) for i in unpack("<HH", match.group().encode("utf-16le"))),
        text
    )


def remove_surrogates(text):
    # Replace each surrogate pair with a SMP code point
    return text.encode("utf-16", "surrogatepass").decode("utf-16")


def replace_once(source: str, old: str, new: str, start: int):
    return source[:start] + source[start:].replace(old, new, 1)

def within_surrogate(text, index, *, length=None):
    """
    `True` if ``index`` is within a surrogate (before and after it, not at!).
    """
    if length is None:
        length = len(text)

    return (
            1 < index < len(text) and  # in bounds
            '\ud800' <= text[index - 1] <= '\udbff' and  # previous is
            '\ud800' <= text[index] <= '\udfff'  # current is
    )
