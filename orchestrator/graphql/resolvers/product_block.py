from typing import Union

import structlog

from orchestrator.db.filters import Filter
from orchestrator.db.filters.product_block import filter_product_blocks
from orchestrator.db.models import ProductBlockTable
from orchestrator.db.range.range import apply_range_to_query
from orchestrator.db.sorting.product_block import sort_product_blocks
from orchestrator.db.sorting.sorting import Sort
from orchestrator.graphql.pagination import Connection
from orchestrator.graphql.schemas.product_block import ProductBlock
from orchestrator.graphql.types import GraphqlFilter, GraphqlSort, OrchestratorInfo
from orchestrator.graphql.utils.create_resolver_error_handler import create_resolver_error_handler
from orchestrator.graphql.utils.to_graphql_result_page import to_graphql_result_page

logger = structlog.get_logger(__name__)


async def resolve_product_blocks(
    info: OrchestratorInfo,
    filter_by: Union[list[GraphqlFilter], None] = None,
    sort_by: Union[list[GraphqlSort], None] = None,
    first: int = 10,
    after: int = 0,
) -> Connection[ProductBlock]:
    _error_handler = create_resolver_error_handler(info)

    pydantic_filter_by: list[Filter] = [item.to_pydantic() for item in filter_by] if filter_by else []
    pydantic_sort_by: list[Sort] = [item.to_pydantic() for item in sort_by] if sort_by else []
    logger.debug(
        "resolve_product_blocks() called", range=[after, after + first], sort=sort_by, filter=pydantic_filter_by
    )

    query = filter_product_blocks(ProductBlockTable.query, pydantic_filter_by, _error_handler)
    query = sort_product_blocks(query, pydantic_sort_by, _error_handler)
    total = query.count()
    query = apply_range_to_query(query, after, first)

    product_blocks = query.all()
    graphql_product_blocks = [ProductBlock.from_pydantic(p) for p in product_blocks]
    return to_graphql_result_page(graphql_product_blocks, first, after, total)
