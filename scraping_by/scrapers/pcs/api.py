"""
Ultrabasic demo api "scraper" that pulls all the notices of a given type from
PCS in a given output format and prints some salient details.

See: https://api.publiccontractsscotland.gov.uk/v1/Notices
"""
# import sys
import argparse
import asyncio

import httpx


API_URL = "https://api.publiccontractsscotland.gov.uk/v1/Notices"


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
    help="0: OCDS, 1: TED/custom",
)


async def query_api(client, params: dict):
    response = await client.get(API_URL, params=params)
    return response


async def main(params: dict):
    async with httpx.AsyncClient() as client:
        response = await query_api(client, params)
    return response.json()


def same_structure(n1: dict, n2: dict) -> bool:
    """
    recursive structure checker for two nested jsons

    returns True if all keys are the same at every level of nesting,
    False otherwise
    """
    for (k1, v1), (k2, v2) in zip(n1.items(), n2.items()):
        if not (k1 == k2):
            return False
        if isinstance(v1, dict):
            if isinstance(v2, dict):
                return same_structure(v1, v2)
            else:
                raise ValueError("structures different for:", k1, ",", k2)
    return True


if __name__ == "__main__":

    args = parser.parse_args()

    params = dict(
        noticeType=args.notice_type,  # 2: contract notice, 3 contract award notice
        outputType=args.output_type,  # 0: OCDS, 1: TED/custom
    )
    results = asyncio.run(main(params))
    notices = results["releases"]

    print(f"Found {len(notices)} records")

    # check all records have exactly the same structure
    for n1, n2 in zip(notices, notices[1:]):
        print(n1["id"], "&", n2["id"], ":", same_structure(n1, n2))
