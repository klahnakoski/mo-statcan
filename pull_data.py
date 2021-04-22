# encoding: utf-8
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Contact: Kyle Lahnakoski (kyle@lahnakoski.com)
#

import pandas as pd
import plotly.graph_objects as go
from mo_dots import to_data, from_data, listwrap, is_many
from mo_files import mimetype
from mo_http import http
from mo_logs import Log
from mo_times import Date


# PROVINCE = 7
# PROVINCE_NAME = "Ontario"

PROVINCE = 11
PROVINCE_NAME = "British Columbia"

Log.start(trace=True)

http.DEBUG = True
http.default_headers = to_data({
    "From": "kyle@lahnakoski.com",
    "Referer": "https://github.com/klahnakoski/mo-statcan",
    "User-Agent": "mo-statscan",
    "Accept": mimetype.ANY,
})

# LESS DETAILED CAUSES
CAUSE_OF_DEATH = (
    13_10_0394  # https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1310039401
)

# DETAILED CAUSES
GROUPED_CAUSE_DEATH = (
    13_10_0392  # https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1310039201
)

#
WEEKLY_DEATHS = (
    13_10_0784  # https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1310078401
)
WEEKLY_DEATHS_OLD = 13_10_0779
WEEKLY_DEATHS_NEW = 13_10_0768  # by age and province
#
MONTHLY_DEATHS = (
    13_10_0708  # https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1310070801
)

#
POPULATION_ESTIMATES = (
    17_10_0005  # https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710000501
)

MORTALITY_BY_AGE = (
    13_10_0710  # https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1310071001
)


def metadata(cube_id):
    """
    RETURN CUBE METADATA (DESCRIPTION OF EDGES)
    :param cube_id: STATCAN CUBE ID NUMBER
    :return: METADATA IN JSON FORM
    """
    return http.post_json(
        "https://www150.statcan.gc.ca/t1/wds/rest/getCubeMetadata",
        json=[{"productId": cube_id}],
    )


def format_coordinate(coord):
    coordinates = coord.split(".")
    coordinates.extend(["0"] * (10 - len(coordinates)))
    return ".".join(coordinates)


def data(cube_id, coord, num):
    """
    RETURN DATA FOR ONE COORDINATE
    :param cube_id:
    :param coord:
    :param num: HOW FAR BACK TO GO, LENGTH OF SERIES TO CAPTURE
    :return:
    """
    coordinates = [format_coordinate(c) for c in listwrap(coord)]
    data = http.post_json(
        "https://www150.statcan.gc.ca/t1/wds/rest/getDataFromCubePidCoordAndLatestNPeriods",
        json=[
            {"productId": cube_id, "coordinate": c, "latestN": num} for c in coordinates
        ],
    )
    output = [None] * len(coordinates)
    for d in data:
        df = pd.DataFrame(columns=[k for k, _ in d.object.vectorDataPoint[0].items()])
        # TODO: GOT TO BE A FASTER WAY
        for point in from_data(d.object.vectorDataPoint):
            df = df.append(point, ignore_index=True)
        i = coordinates.index(d.object.coordinate)
        output[i] = df

    if is_many(coord):
        return output
    else:
        return output[0]


# # ALL CUBES
# cubes = http.get_json("https://www150.statcan.gc.ca/t1/wds/rest/getAllCubesListLite")
# Log.note("There are {{num}} cubes", cubes=len(cubes))
# Log.note("death cubes\n{{names}}", names=[(c.productId, c.cubeTitleEn) for c in cubes if str(c.productId).startswith('1310')])

#
# # PULL METADATA
# result = http.post_json(
#     "https://www150.statcan.gc.ca/t1/wds/rest/getCubeMetadata",
#     json=[{"productId": WEEKLY_DEATHS}],
# )
# Log.note("{{data}}", data=result)
#
# PULL SERIES METADATA
# series = http.post_json(
#     "https://www150.statcan.gc.ca/t1/wds/rest/getSeriesInfoFromCubePidCoord",
#     json=[{"productId": WEEKLY_DEATHS, "coordinate": "1.1.0.0.0.0.0.0.0.0"}]
# )
# Log.note("{{series}}", series=series)
#
# # PULL DATA
# data = http.post_json(
#     "https://www150.statcan.gc.ca/t1/wds/rest/getDataFromCubePidCoordAndLatestNPeriods",
#     json=[{"productId": GROUPED_CAUSE_DEATH, "coordinate": "1.1.2.1.1.0.0.0.0.0", "latestN": 3}]
# )
# Log.note("{{data}}", data=data)
#


# PULL METADATA
result = metadata(MONTHLY_DEATHS)
Log.note("{{data}}", data=result)


# result = metadata(POPULATION_ESTIMATES)
# Log.note("{{data}}", data=result)

(
    a00_14,
    a15_19,
    a20_24,
    a25_44,
    a45_64,
    a65_69,
    a70_74,
    a75_79,
    a80_84,
    a85_89,
    a90,
) = data(
    POPULATION_ESTIMATES,
    [
        ""+str(PROVINCE)+".1.91",  # 0-14
        ""+str(PROVINCE)+".1.25",  # 15-19
        ""+str(PROVINCE)+".1.31",  # 20-24
        ""+str(PROVINCE)+".1.102",  # 25-44
        ""+str(PROVINCE)+".1.103",  # 45-64
        ""+str(PROVINCE)+".1.85",  # 65-69  **
        ""+str(PROVINCE)+".1.86",  # 70-74  **
        ""+str(PROVINCE)+".1.87",  # 75-79  **
        ""+str(PROVINCE)+".1.88",  # 80-84  **
        ""+str(PROVINCE)+".1.89",  # 85-89
        ""+str(PROVINCE)+".1.90",  # 90+
    ],
    12,
)

DATE_COLUMN = "refPerRaw"
populations = a00_14
populations = populations.join(
    a15_19.set_index(DATE_COLUMN), on=DATE_COLUMN, how="inner", lsuffix="", rsuffix="_15"
)
populations = populations.join(
    a20_24.set_index(DATE_COLUMN), on=DATE_COLUMN, how="inner", lsuffix="", rsuffix="_20"
)
populations = populations.join(
    a25_44.set_index(DATE_COLUMN), on=DATE_COLUMN, how="inner", lsuffix="", rsuffix="_25"
)
populations = populations.join(
    a45_64.set_index(DATE_COLUMN), on=DATE_COLUMN, how="inner", lsuffix="", rsuffix="_45"
)
populations = populations.join(
    a65_69.set_index(DATE_COLUMN), on=DATE_COLUMN, how="inner", lsuffix="", rsuffix="_65"
)
populations = populations.join(
    a70_74.set_index(DATE_COLUMN), on=DATE_COLUMN, how="inner", lsuffix="", rsuffix="_70"
)
populations = populations.join(
    a75_79.set_index(DATE_COLUMN), on=DATE_COLUMN, how="inner", lsuffix="", rsuffix="_75"
)
populations = populations.join(
    a80_84.set_index(DATE_COLUMN), on=DATE_COLUMN, how="inner", lsuffix="", rsuffix="_80"
)
populations = populations.join(
    a85_89.set_index(DATE_COLUMN), on=DATE_COLUMN, how="inner", lsuffix="", rsuffix="_85"
)
populations = populations.join(
    a90.set_index(DATE_COLUMN), on=DATE_COLUMN, how="inner", lsuffix="", rsuffix="_90"
)

populations["00"] = (
        populations["value"]
        + populations["value_15"]
        + populations["value_20"]
        + populations["value_25"]
)
populations["45"] = populations["value_45"]
populations["65"] = (
        populations["value_65"]
        + populations["value_70"]
        + populations["value_75"]
        + populations["value_80"]
)
populations["85"] = populations["value_85"] + populations["value_90"]

# fig = go.Figure(data=[
#     go.Bar(name="0-44", x=populations[DATE_COLUMN], y=populations["00"]),
#     go.Bar(name="45-64", x=populations[DATE_COLUMN], y=populations["45"]),
#     go.Bar(name="65-84", x=populations[DATE_COLUMN], y=populations["65"]),
#     go.Bar(name="85+", x=populations[DATE_COLUMN], y=populations["85"]),
# ])
# fig.update_layout(title="Population, "+PROVINCE_NAME, barmode="stack")
# fig.show()


def get_population(y, date):
    """
    RETURN POPULATION AT GIVEN DATE
    :param date:
    :param y: WHICH POPULATION
    """
    for i, next in enumerate(populations[DATE_COLUMN]):
        next = Date(next)
        if date < next:
            prev = Date(populations[DATE_COLUMN][i - 1])
            y1, y2 = populations[y][i-1:i+1]
            ratio = (date-prev)/(next-prev)
            return (y2-y1)*ratio+y1
    # STRAIGHT LINE PROJECTION
    next = Date(populations[DATE_COLUMN][populations.shape[0]-1])
    prev = Date(populations[DATE_COLUMN][populations.shape[0]-2])
    y1, y2 = populations[y][-2:]
    ratio = (date-prev)/(next-prev)
    return (y2-y1)*ratio+y1



#
#
# combined = deaths.join(population.set_index('refPer'), on='refPer', how="inner", lsuffix="_deaths", rsuffix="_population")
# combined['Death Rate'] = (combined['value_deaths'] / combined['value_population'])
# fig = px.bar(combined, x="refPer", y="Death Rate")
# fig.update_layout(title="Death Rate, "+PROVINCE_NAME+", Normalized to population 65+")
# fig.show()


# WEEKLY DEATHS NEW
# result = metadata(WEEKLY_DEATHS_NEW)
# Log.note("{{data}}", data=result)

weekly_deaths0, weekly_deaths45, weekly_deaths65, weekly_deaths85 = data(
    WEEKLY_DEATHS_NEW, [""+str(PROVINCE)+".2.1.1", ""+str(PROVINCE)+".3.1.1", ""+str(PROVINCE)+".4.1.1", ""+str(PROVINCE)+".5.1.1"], 1000  # Jan 2010
)  # Ontario, 65+, both sex, count

deaths = weekly_deaths0
deaths = deaths.join(
    weekly_deaths45.set_index("refPer"),
    on="refPer",
    how="inner",
    lsuffix="",
    rsuffix="_45",
)
deaths = deaths.join(
    weekly_deaths65.set_index("refPer"),
    on="refPer",
    how="inner",
    lsuffix="",
    rsuffix="_65",
)
deaths = deaths.join(
    weekly_deaths85.set_index("refPer"),
    on="refPer",
    how="inner",
    lsuffix="",
    rsuffix="_85",
)

deaths["pop_00"] = [get_population("00", Date(date)) for date in deaths["refPer"]]
deaths["pop_45"] = [get_population("45", Date(date)) for date in deaths["refPer"]]
deaths["pop_65"] = [get_population("65", Date(date)) for date in deaths["refPer"]]
deaths["pop_85"] = [get_population("85", Date(date)) for date in deaths["refPer"]]

deaths["rate_00"] = deaths['value']/deaths['pop_00']*1_000_000
deaths["rate_45"] = deaths['value_45']/deaths['pop_45']*1_000_000
deaths["rate_65"] = deaths['value_65']/deaths['pop_65']*1_000_000
deaths["rate_85"] = deaths['value_85']/deaths['pop_85']*1_000_000


# fig = go.Figure(data=[
#     go.Bar(name="0-44", x=deaths["refPer"], y=deaths["value"]),
#     go.Bar(name="45-64", x=deaths["refPer"], y=deaths["value_45"]),
#     go.Bar(name="65-84", x=deaths["refPer"], y=deaths["value_65"]),
#     go.Bar(name="85+", x=deaths["refPer"], y=deaths["value_85"]),
# ])
# fig.update_layout(title="Weekly Deaths, "+PROVINCE_NAME, barmode="stack")
# fig.show()

fig = go.Figure(data=[
    go.Bar(name="0-44", x=deaths["refPer"], y=deaths["rate_00"]),
    go.Bar(name="45-64", x=deaths["refPer"], y=deaths["rate_45"]),
    go.Bar(name="65-84", x=deaths["refPer"], y=deaths["rate_65"]),
    go.Bar(name="85+", x=deaths["refPer"], y=deaths["rate_85"]),
])
fig.update_layout(title="Weekly Deaths per Million, "+PROVINCE_NAME, barmode="stack")
fig.show()

# fig = go.Figure(data=[
#     go.Bar(name="0-44", x=deaths["refPer"], y=deaths["pop_00"]),
#     go.Bar(name="45-64", x=deaths["refPer"], y=deaths["pop_45"]),
#     go.Bar(name="65-84", x=deaths["refPer"], y=deaths["pop_65"]),
#     go.Bar(name="85+", x=deaths["refPer"], y=deaths["pop_85"]),
# ])
# fig.update_layout(title="Weekly population, "+PROVINCE_NAME, barmode="stack")
# fig.show()
#
