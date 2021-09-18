"""
Ultrabasic demo api "scraper" that pulls all the notices of a given type from
PCS in a given output format and prints some salient details.

See: https://api.publiccontractsscotland.gov.uk/v1/Notices
"""
import argparse
import asyncio

import httpx
from ocdskit.combine import merge

from scraping_by.scrapers.pcs.response_model import Model


# curl --location --request GET 'https://api.publiccontractsscotland.gov.uk/v1/Notices?noticeType=2&outputType=0' > release_packages.json
# cat release_packages.json | ocdskit --encoding iso-8859-1 compile > compiled_releases.json

API_URL = "https://api.publiccontractsscotland.gov.uk/v1/Notices"

NOTICE_TYPES = {
    1: "OJEU - F1 - Prior Information Notice",
    2: "OJEU - F2 - Contract Notice",
    3: "OJEU - F3 - Contract Award Notice",
    4: "OJEU - F4 - Prior Information Notice (Utilities)",
    5: "OJEU - F5 - Contract Notice (Utilities)",
    6: "OJEU - F6 - Contract Award Notice (Utilities)",
    7: "OJEU - F7 - Qualification Systems (Utilities)",
    12: "OJEU - F12 - Public design contest",
    13: "OJEU - F13 - Results of Design Contest",
    14: "OJEU - F14 - Corrigendum",
    15: "OJEU - F15 - Voluntary Ex Ante Transparency Notice",
    20: "OJEU - F20 - Modification Notice",
    21: "OJEU - F21 - Social And other Specific Services (Public Contracts)",
    22: "OJEU - F22 - Social and other specific services (Utilities)",
    23: "OJEU - F23 - Social and other specific services (Concessions)",
    24: "OJEU - F24 - Concession Notice",
    25: "OJEU - F25 - Concession Award Notice",
    101: "Site Notice - Website Prior Information Notice",
    102: "Site Notice - Website Contract Notice",
    103: "Site Notice - Website Contract Award Notice",
    104: "Site Notice - Quick Quote Award",
}


parser = argparse.ArgumentParser()
parser.add_argument(
    "-n",
    "--notice-type",
    dest="notice_type",
    type=int,
    default=2,
    help="2: contract notice, 3 contract award notice",
)
parser.add_argument(
    "-o",
    "--output-type",
    dest="output_type",
    type=int,
    default=0,
    help="\n".join([f"{k} : {v}" for k, v in NOTICE_TYPES.items()]),
)


async def query_api(client, params: dict):
    response = await client.get(API_URL, params=params)
    return response


async def get_notices(params: dict):
    async with httpx.AsyncClient() as client:
        response = await query_api(client, params)
    data = response.json()
    # RAM non-issue here; evaluate generator for all releases
    data["releases"] = list(merge(data["releases"]))
    # deserialise JSON
    data = Model(**data)
    return data


# top level
# release["id"]: "rls-1-SEP427811"
# release["ocid"]: "ocds-r6ebe6-0000667263"
# release["date"]: "2021-09-17T00:00:00Z"
# release["initiationType"]: "tender"
# release["parties"] = [{party1, party2}]


if __name__ == "__main__":

    args = parser.parse_args()
    params = dict(
        noticeType=args.notice_type,  # 2: contract notice, 3 contract award notice
        outputType=args.output_type,  # 0: OCDS, 1: TED/custom
    )

    # obtain releases from API
    data = asyncio.run(get_notices(params))
    print(f"Found {len(data.releases)} records")
    print(data)
