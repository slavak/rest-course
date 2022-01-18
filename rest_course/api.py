# PEP 585
from collections.abc import Iterable

from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import NonNegativeInt

from . import bdb_manager
from .params import BDBParams, BDBResponse
from .types import UID
from .util import link, url_for

app = FastAPI(title="REST Course", description="REST API Course")


@app.post("/bdbs", tags=["bdb"], operation_id="create_bdb", response_model=BDBResponse)
def create_bdb(req: BDBParams, request: Request, response: Response):
    bdb = bdb_manager.create_bdb(req)

    # TODO: Add fields: created_at
    url = url_for(request, "get_bdb", uid=str(bdb.uid))
    response.headers["location"] = url
    return BDBResponse(bdb=bdb, url=url)


@app.get(
    "/bdbs/{uid}", tags=["bdb"], operation_id="get_bdb", response_model=BDBResponse
)
def get_bdb(uid: UID, request: Request):
    try:
        bdb = bdb_manager.get_bdb(uid)
        url = url_for(request, "get_bdb", uid=str(bdb.uid))
        return BDBResponse(bdb=bdb, url=url)
    except LookupError:
        raise HTTPException(status_code=404)


@app.get(
    "/bdbs",
    tags=["bdb"],
    operation_id="get_all_bdbs",
    response_model=Iterable[BDBResponse],
)
def get_all_bdbs(
    request: Request,
    response: Response,
    offset: NonNegativeInt = 0,
    limit: NonNegativeInt = 1000,
):
    def url_with_offset(offset, _limit=limit):
        return url_for(
            request, "get_all_bdbs", query_params=dict(offset=offset, limit=_limit)
        )

    bdb_count = len(list(bdb_manager.get_bdb_uids()))

    rels = dict(
        first=url_with_offset(0),
        last=url_with_offset(bdb_count - bdb_count % limit),
    )
    if 0 < offset <= bdb_count:
        prev = offset - limit
        prev_limit = limit
        if prev < 0:
            prev_limit = limit + prev
            prev = 0
        rels["prev"] = url_with_offset(prev, prev_limit)
    if offset + limit < bdb_count:
        _next = offset + limit
        rels["next"] = url_with_offset(_next)

    response.headers["link"] = link(rels)

    for bdb in bdb_manager.get_all_bdbs(offset=offset, limit=limit):
        url = url_for(request, "get_bdb", uid=str(bdb.uid))
        yield BDBResponse(bdb=bdb, url=url)
