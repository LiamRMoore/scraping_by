from fastapi import FastAPI, Query
from typing import List, Optional

import scraping_by.scrapers.pcs as pcs

app = FastAPI()


@app.get("/contracts/pcs")
async def get_contracts(
    output_type: Optional[int] = Query(
        0, description="An integer specifying the output format"
    ),
    notice_type: Optional[int] = Query(
        2, description="An integer specifying the notice type"
    ),
) -> List:
    data = await pcs.get_notices(output_type, notice_type)
    contracts = [pcs.contract_cls(d).contract for d in data.releases]
    return contracts
