# Copyright 2022 The Feathub Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Optional, Dict, Sequence
from datetime import timedelta

from feathub.feature_views.transforms.transformation import Transformation


class WindowAggTransform(Transformation):
    """
    Derives feature values by applying Feathub expression and aggregation function on
    multiple rows of the parent table at a time.
    """

    def __init__(
        self,
        expr: str,
        agg_func: str,
        group_by_keys: Sequence[str] = (),
        window_size: Optional[timedelta] = None,
        filter_expr: Optional[str] = None,
        limit: Optional[int] = None,
    ):
        """
        :param expr: A Feathub expression composed of UDF and feature names.
        :param agg_func: The name of an aggregation function such as MAX, AVG.
        :param group_by_keys: The names of fields to be used as the grouping key.
        :param window_size: Optional. If it is not None, for any row in the table with
                            timestamp = t0, only rows whose timestamp fall in range
                            [t0 - timedelta, t0] can be included in the aggregation. If
                            it is None, the window size is effectively unlimited.
        :param filter_expr: Optional. If it is not None, it represents a Feathub
                            expression. A row can be included in the aggregation only
                            if the expression result on this row is true.
        :param limit: Optional. If it is not None, up to `limit` number of most recent
                      rows prior to this row can be included in the aggregation.
        """
        super().__init__()
        self.expr = expr
        self.agg_func = agg_func
        self.group_by_keys = group_by_keys
        self.window_size = window_size
        self.filter_expr = filter_expr
        self.limit = limit

    def to_json(self) -> Dict:
        return {
            "type": "WindowAggTransform",
            "expr": self.expr,
            "agg_func": self.agg_func,
            "group_by_keys": self.group_by_keys,
            "window_size_ms": None
            if self.window_size is None
            else self.window_size / timedelta(milliseconds=1),
            "filter_expr": self.filter_expr,
            "limit": self.limit,
        }