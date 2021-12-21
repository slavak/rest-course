from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.bdb import BDB
from ...models.bdb_params import BDBParams
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: BDBParams,
) -> Dict[str, Any]:
    url = "{}/bdbs".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[BDB, HTTPValidationError]]:
    if response.status_code == 201:
        response_201 = BDB.from_dict(response.json())

        return response_201
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[BDB, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: BDBParams,
) -> Response[Union[BDB, HTTPValidationError]]:
    """Create Bdb

    Args:
        json_body (BDBParams):

    Returns:
        Response[Union[BDB, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.post(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    json_body: BDBParams,
) -> Optional[Union[BDB, HTTPValidationError]]:
    """Create Bdb

    Args:
        json_body (BDBParams):

    Returns:
        Response[Union[BDB, HTTPValidationError]]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: BDBParams,
) -> Response[Union[BDB, HTTPValidationError]]:
    """Create Bdb

    Args:
        json_body (BDBParams):

    Returns:
        Response[Union[BDB, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    json_body: BDBParams,
) -> Optional[Union[BDB, HTTPValidationError]]:
    """Create Bdb

    Args:
        json_body (BDBParams):

    Returns:
        Response[Union[BDB, HTTPValidationError]]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
