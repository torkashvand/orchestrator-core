# Copyright 2019-2023 SURF.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Callable

from sqlalchemy import Column

from orchestrator.db.database import SearchQuery


def generic_bool_filter(field: Column) -> Callable[[SearchQuery, str], SearchQuery]:
    def bool_filter(query: SearchQuery, value: str) -> SearchQuery:
        value_as_bool = value.lower() in ("yes", "y", "true", "1", "ja", "j")
        return query.filter(field.is_(value_as_bool))

    return bool_filter
