# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from __future__ import annotations

import os
import pathlib
import typing

import pandas as pd
import tiktoken
import typing_extensions

from . import _base, _defaults, _utils
from .. import _builders
from ... import _llm
from .... import _utils as _common_utils


class LocalContextLoader(_base.BaseContextLoader):
    _nodes: pd.DataFrame
    _entities: pd.DataFrame
    _community_reports: pd.DataFrame
    _text_units: pd.DataFrame
    _relationships: pd.DataFrame
    _covariates: typing.Optional[pd.DataFrame] = None

    @classmethod
    @typing_extensions.override
    def from_parquet_directory(
        cls,
        directory: typing.Union[str, os.PathLike[str], pathlib.Path],
        **kwargs: str
    ) -> typing.Self:
        directory = pathlib.Path(directory)
        if not directory.exists() or not directory.is_dir():
            raise FileNotFoundError(f"Directory not found: {directory}")
        nodes = pd.read_parquet(directory / kwargs.get("nodes", _defaults.PARQUET_FILE_NAME__NODES))
        entities = pd.read_parquet(directory / kwargs.get("entities", _defaults.PARQUET_FILE_NAME__ENTITIES))
        community_reports = pd.read_parquet(
            directory / kwargs.get("community_reports", _defaults.PARQUET_FILE_NAME__COMMUNITY_REPORTS)
        )
        text_units = pd.read_parquet(directory / kwargs.get("text_units", _defaults.PARQUET_FILE_NAME__TEXT_UNITS))
        relationships = pd.read_parquet(
            directory / kwargs.get("relationships", _defaults.PARQUET_FILE_NAME__RELATIONSHIPS)
        )
        covariates_path = directory / kwargs.get("covariates", _defaults.PARQUET_FILE_NAME__COVARIATES)
        covariates = pd.read_parquet(covariates_path) if covariates_path.exists() else None
        return cls(
            nodes=nodes,
            entities=entities,
            community_reports=community_reports,
            text_units=text_units,
            relationships=relationships,
            covariates=covariates,
        )

    def __init__(
        self,
        *,
        nodes: pd.DataFrame,
        entities: pd.DataFrame,
        community_reports: pd.DataFrame,
        text_units: pd.DataFrame,
        relationships: pd.DataFrame,
        covariates: typing.Optional[pd.DataFrame],
    ) -> None:
        self._nodes = nodes
        self._entities = entities
        self._community_reports = community_reports
        self._text_units = text_units
        self._relationships = relationships
        self._covariates = covariates

    @typing_extensions.override
    def to_context_builder(
        self,
        community_level: int,
        embedder: _llm.BaseEmbedding,
        store_coll_name: str,
        store_uri: str,
        encoding_model: str,
        **kwargs: typing.Any
    ) -> _builders.LocalContextBuilder:
        entities_list = _utils.get_entities(
            nodes=self._nodes,
            entities=self._entities,
            community_level=community_level,
            **_common_utils.filter_kwargs(_utils.get_entities, kwargs, prefix="entities__")
        )
        community_reports_list = _utils.get_community_reports(
            community_reports=self._community_reports,
            nodes=self._nodes,
            community_level=community_level,
            **_common_utils.filter_kwargs(_utils.get_community_reports, kwargs, prefix="community_reports__")
        )
        text_units_list = _utils.get_text_units(
            text_units=self._text_units,
            **_common_utils.filter_kwargs(_utils.get_text_units, kwargs, prefix="text_units__")
        )
        relationships_list = _utils.get_relationships(
            relationships=self._relationships,
            **_common_utils.filter_kwargs(_utils.get_relationships, kwargs, prefix="relationships__")
        )
        covariates_dict = {
            "claims": _utils.get_covariates(
                self._covariates,
                **_common_utils.filter_kwargs(_utils.get_covariates, kwargs, prefix="covariates__")
            ) if self._covariates is not None else []
        }
        store = _utils.get_store(entities_list, coll_name=store_coll_name, uri=store_uri)
        return _builders.LocalContextBuilder(
            entities=entities_list,
            entity_text_embeddings=store,
            community_reports=community_reports_list,
            text_units=text_units_list,
            relationships=relationships_list,
            covariates=covariates_dict,
            text_embedder=embedder,
            token_encoder=tiktoken.get_encoding(encoding_model),
        )

    @typing_extensions.override
    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}(\n"
            f"\tnum_nodes={len(self._nodes)}, \n"
            f"\tnum_entities={len(self._entities)}, \n"
            f"\tnum_community_reports={len(self._community_reports)}, \n"
            f"\tnum_text_units={len(self._text_units)}, \n"
            f"\tnum_relationships={len(self._relationships)}, \n"
            f"\tnum_covariates={self._covariates and len(self._covariates) or 0}\n"
            f")"
        )

    @typing_extensions.override
    def __repr__(self) -> str:
        return self.__str__()


class GlobalContextLoader(_base.BaseContextLoader):
    _nodes: pd.DataFrame
    _entities: pd.DataFrame
    _community_reports: pd.DataFrame

    @classmethod
    @typing_extensions.override
    def from_parquet_directory(
        cls,
        directory: typing.Union[str, os.PathLike[str], pathlib.Path],
        **kwargs: str
    ) -> typing.Self:
        directory = pathlib.Path(directory)
        if not directory.exists() or not directory.is_dir():
            raise FileNotFoundError(f"Directory not found: {directory}")

        nodes = pd.read_parquet(
            directory / kwargs.get("nodes", _defaults.PARQUET_FILE_NAME__NODES)
        )
        entities = pd.read_parquet(
            directory / kwargs.get("entities", _defaults.PARQUET_FILE_NAME__ENTITIES)
        )
        community_reports = pd.read_parquet(
            directory / kwargs.get("community_reports", _defaults.PARQUET_FILE_NAME__COMMUNITY_REPORTS)
        )

        return cls(
            nodes=nodes,
            entities=entities,
            community_reports=community_reports,
        )

    def __init__(
        self,
        *,
        nodes: pd.DataFrame,
        entities: pd.DataFrame,
        community_reports: pd.DataFrame,
    ) -> None:
        self._nodes = nodes
        self._entities = entities
        self._community_reports = community_reports

    @typing_extensions.override
    def to_context_builder(
        self,
        community_level: int,
        encoding_model: str,
        **kwargs: typing.Any
    ) -> _builders.GlobalContextBuilder:
        community_reports_list = _utils.get_community_reports(
            community_reports=self._community_reports,
            nodes=self._nodes,
            community_level=community_level,
            **_common_utils.filter_kwargs(_utils.get_community_reports, kwargs, prefix="community_reports__")
        )
        entities_list = _utils.get_entities(
            nodes=self._nodes,
            entities=self._entities,
            community_level=community_level,
            **_common_utils.filter_kwargs(_utils.get_entities, kwargs, prefix="entities__")
        )
        return _builders.GlobalContextBuilder(
            community_reports=community_reports_list,
            entities=entities_list,
            token_encoder=tiktoken.get_encoding(encoding_model),
        )

    @typing_extensions.override
    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}(\n"
            f"\tnum_nodes={len(self._nodes)}, \n"
            f"\tnum_entities={len(self._entities)}, \n"
            f"\tnum_community_reports={len(self._community_reports)}\n"
            f")"
        )

    @typing_extensions.override
    def __repr__(self) -> str:
        return self.__str__()
