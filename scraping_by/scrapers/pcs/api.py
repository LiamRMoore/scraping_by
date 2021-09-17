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
    default=1,
    help="0: OCDS, 1: TED/custom",
)


async def query_api(client, params):
    response = await client.get(API_URL, params=params)
    return response


async def main(params):
    async with httpx.AsyncClient() as client:
        response = await query_api(client, params)
    return response.json()


if __name__ == "__main__":

    args = parser.parse_args()

    params = dict(
        noticeType=args.notice_type,  # 2: contract notice, 3 contract award notice
        outputType=args.output_type,  # 0: OCDS, 1: TED/custom
    )
    results = asyncio.run(main(params))
    print(results.keys())
    notices = results["notices"]

    print(f"Found {len(notices)} records")
    # sys.exit(0)
    for n in notices:

        print(n)
        # TODO: look into best json parser for using native python getattr object notation
        # Short description
        descr = n["Form_Section"]["F03_2014"]["Object_Contract"]
        # print("Short description:")
        # print(descr)

        # URLs for more details @
        url = n["Form_Section"]["F03_2014"]["Contracting_Body"][
            "Address_Contracting_Body"
        ]["URL_Buyer"]
        print("URL:")
        print(url)
        break
