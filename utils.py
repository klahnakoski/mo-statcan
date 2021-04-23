# encoding: utf-8
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Contact: Kyle Lahnakoski (kyle@lahnakoski.com)
#

from mo_future import first
from mo_math import ceiling, log10


def mostly_max(values):
    """
    RETURN A VALUE MORE THAN MOST OF THE VALUES
    :param values:
    """
    sorted = list(sorted(values))
    num = len(sorted)
    p50 = sorted[ceiling(num * 0.5)]
    p90 = sorted[ceiling(num * 0.9)]
    max = sorted[num]
    most = max(p50 * 2.0, p90 * 1.1)

    if most == 0:
        return max * 1.1

    return min(max * 1.1, most)


def nice_ceiling(value):
    """
    RETURN A NICE CEILING
    :param value:
    """
    if value == 0:
        return 1
    d = 10 ** (ceiling(log10(value)) - 1)
    norm = value / d
    nice = first(v for v in [1.5, 2, 3, 5, 7.5, 10] if norm <= v)

    return nice * d
