# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License.
#
# Copyright (c) 2024 6ixGODD.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import typing

from ..._search._model import _identified


class TextUnit(_identified.Identified):
    """A protocol for a TextUnit item in a Document database."""

    text: str = ""
    """The text of the unit."""

    text_embedding: typing.Optional[typing.List[float]] = None
    """The text embedding for the text unit (optional)."""

    entity_ids: typing.Optional[typing.List[str]] = None
    """List of entity IDs related to the text unit (optional)."""

    relationship_ids: typing.Optional[typing.List[str]] = None
    """List of relationship IDs related to the text unit (optional)."""

    covariate_ids: typing.Optional[typing.Dict[str, typing.List[str]]] = None
    """Dictionary of different types of covariates related to the text unit (optional)."""

    n_tokens: typing.Optional[int] = None
    """The number of tokens in the text (optional)."""

    document_ids: typing.Optional[typing.List[str]] = None
    """List of document IDs in which the text unit appears (optional)."""

    attributes: typing.Optional[typing.Dict[str, typing.Any]] = None
    """A dictionary of additional attributes associated with the text unit (optional)."""
