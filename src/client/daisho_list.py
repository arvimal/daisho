#!/usr/bin/env python3

# MIT License

# Copyright (C) 2018 Vimal A.R <arvimal@yahoo.in>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files(the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
daisho_list handles listing the tasks and notes, based on filters.

`filters` are any one of the following:

* all [default]
* today
* tomorrow
* date [`DD-MM-YYYY`]
* tags [#tag_val]
* prio [#high, #med, #low]
* trash

This also takes care on opening tasks which has active sub-tasks,
as well as notes in the pre-configured editor of your choice.
"""

from client import daisho_db


def list_all(val="all"):
    if val == "today":
        pass
        # daisho_db.sys(search.today)
    elif val == "tomorrow":
        pass
        # daisho_db.sys(search.tomorrow)
