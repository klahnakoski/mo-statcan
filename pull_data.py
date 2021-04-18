# encoding: utf-8
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Contact: Kyle Lahnakoski (kyle@lahnakoski.com)
#
from mo_dots import to_data
from mo_json import value2json, json2value
from mo_logs import Log, strings

from mo_files import mimetype
from mo_http import http

Log.start(trace=True)

http.DEBUG = True
http.default_headers = to_data({
    "From": "kyle@lahnakoski.com",
    "Referer": "https://github.com/klahnakoski/mo-statcan",
    "User-Agent": "mo-statscan",
    "Accept": mimetype.ANY,
})

AGE_AT_DEATH = 13_10_0392

WEEKLY_DEATHS = 13_10_0784

DEATHS_BY_MONTH = 13_10_0708

# ALL CUBES
# cubes = http.get_json("https://www150.statcan.gc.ca/t1/wds/rest/getAllCubesListLite")
# Log.note("There are {{num}} cubes", cubes=len(cubes))

# # PULL METADATA
# result = http.post_json(
#     "https://www150.statcan.gc.ca/t1/wds/rest/getCubeMetadata",
#     json=[{"productId": WEEKLY_DEATHS}],
# )
# Log.note("{{data}}", data=result)

# series = http.post_json(
#     "https://www150.statcan.gc.ca/t1/wds/rest/getSeriesInfoFromCubePidCoord",
#     json=[{"productId": WEEKLY_DEATHS, "coordinate": "1.1.0.0.0.0.0.0.0.0"}]
# )
# Log.note("{{series}}", series=series)
#

# PULL DATA
data = http.post_json(
    "https://www150.statcan.gc.ca/t1/wds/rest/getDataFromCubePidCoordAndLatestNPeriods",
    json=[{"productId": AGE_AT_DEATH, "coordinate": "1.1.2.1.1.0.0.0.0.0", "latestN": 3}]
)
Log.note("{{data}}", data=data)

