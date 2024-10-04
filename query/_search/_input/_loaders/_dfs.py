# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from __future__ import annotations

from typing import List, Optional

import pandas as pd

from .... import _vector_stores
from ...._search import _model
from ...._search._input._loaders import _utils


def read_entities(
    df: pd.DataFrame,
    *,
    id_col: str = "id",
    short_id_col: Optional[str] = "short_id",
    title_col: str = "title",
    type_col: Optional[str] = "type",
    description_col: Optional[str] = "description",
    name_embedding_col: Optional[str] = "name_embedding",
    description_embedding_col: Optional[str] = "description_embedding",
    graph_embedding_col: Optional[str] = "graph_embedding",
    community_col: Optional[str] = "community_ids",
    text_unit_ids_col: Optional[str] = "text_unit_ids",
    document_ids_col: Optional[str] = "document_ids",
    rank_col: Optional[str] = "degree",
    attributes_cols: Optional[List[str]] = None,
) -> List[_model.Entity]:
    """Read entities from a dataframe."""
    entities = []
    for idx, row in df.iterrows():
        entity = _model.Entity(
            id=_utils.to_str(row, id_col),
            short_id=_utils.to_optional_str(row, short_id_col) if short_id_col else str(idx),
            title=_utils.to_str(row, title_col),
            type=_utils.to_optional_str(row, type_col),
            description=_utils.to_optional_str(row, description_col),
            name_embedding=_utils.to_optional_list(row, name_embedding_col, item_type=float),
            description_embedding=_utils.to_optional_list(
                row, description_embedding_col, item_type=float
            ),
            graph_embedding=_utils.to_optional_list(row, graph_embedding_col, item_type=float),
            community_ids=_utils.to_optional_list(row, community_col, item_type=str),
            text_unit_ids=_utils.to_optional_list(row, text_unit_ids_col),
            document_ids=_utils.to_optional_list(row, document_ids_col),
            rank=_utils.to_optional_int(row, rank_col) or 0,
            attributes=(
                {col: row.get(col) for col in attributes_cols} if attributes_cols else None
            ),
        )
        entities.append(entity)
    return entities


def store_entity_semantic_embeddings(
    entities: List[_model.Entity],
    vectorstore: _vector_stores.BaseVectorStore,
) -> _vector_stores.BaseVectorStore:
    """Store entity semantic embeddings in a vectorstore."""
    documents = [
        _vector_stores.VectorStoreDocument(
            id=entity.id,
            text=entity.description,
            vector=entity.description_embedding,
            attributes=(
                {"title": entity.title, **entity.attributes} if entity.attributes else {"title": entity.title}
            ),
        )
        for entity in entities
    ]
    vectorstore.load_documents(documents=documents)
    return vectorstore


def store_entity_behavior_embeddings(
    entities: List[_model.Entity],
    vectorstore: _vector_stores.BaseVectorStore,
) -> _vector_stores.BaseVectorStore:
    """Store entity behavior embeddings in a vectorstore."""
    documents = [
        _vector_stores.VectorStoreDocument(
            id=entity.id,
            text=entity.description,
            vector=entity.graph_embedding,
            attributes=(
                {"title": entity.title, **entity.attributes} if entity.attributes else {"title": entity.title}
            ),
        )
        for entity in entities
    ]
    vectorstore.load_documents(documents=documents)
    return vectorstore


def read_relationships(
    df: pd.DataFrame,
    id_col: str = "id",
    short_id_col: Optional[str] = "short_id",
    source_col: str = "source",
    target_col: str = "target",
    description_col: Optional[str] = "description",
    description_embedding_col: Optional[str] = "description_embedding",
    weight_col: Optional[str] = "weight",
    text_unit_ids_col: Optional[str] = "text_unit_ids",
    document_ids_col: Optional[str] = "document_ids",
    attributes_cols: Optional[List[str]] = None,
) -> List[_model.Relationship]:
    """Read relationships from a dataframe."""
    relationships = []
    for idx, row in df.iterrows():
        rel = _model.Relationship(
            id=_utils.to_str(row, id_col),
            short_id=_utils.to_optional_str(row, short_id_col) if short_id_col else str(idx),
            source=_utils.to_str(row, source_col),
            target=_utils.to_str(row, target_col),
            description=_utils.to_optional_str(row, description_col),
            description_embedding=_utils.to_optional_list(
                row, description_embedding_col, item_type=float
            ),
            weight=_utils.to_optional_float(row, weight_col) or 0.0,
            text_unit_ids=_utils.to_optional_list(row, text_unit_ids_col, item_type=str),
            document_ids=_utils.to_optional_list(row, document_ids_col, item_type=str),
            attributes=(
                {col: row.get(col) for col in attributes_cols} if attributes_cols else None
            ),
        )
        relationships.append(rel)
    return relationships


def read_covariates(
    df: pd.DataFrame,
    id_col: str = "id",
    short_id_col: Optional[str] = "short_id",
    subject_col: str = "subject_id",
    subject_type_col: Optional[str] = "subject_type",
    covariate_type_col: Optional[str] = "covariate_type",
    text_unit_ids_col: Optional[str] = "text_unit_ids",
    document_ids_col: Optional[str] = "document_ids",
    attributes_cols: Optional[List[str]] = None,
) -> List[_model.Covariate]:
    """Read covariates from a dataframe."""
    covariates = []
    for idx, row in df.iterrows():
        cov = _model.Covariate(
            id=_utils.to_str(row, id_col),
            short_id=_utils.to_optional_str(row, short_id_col) if short_id_col else str(idx),
            subject_id=_utils.to_str(row, subject_col),
            subject_type=(
                _utils.to_str(row, subject_type_col) if subject_type_col else "entity"
            ),
            covariate_type=(
                _utils.to_str(row, covariate_type_col) if covariate_type_col else "claim"
            ),
            text_unit_ids=_utils.to_optional_list(row, text_unit_ids_col, item_type=str),
            document_ids=_utils.to_optional_list(row, document_ids_col, item_type=str),
            attributes=(
                {col: row.get(col) for col in attributes_cols} if attributes_cols else None
            ),
        )
        covariates.append(cov)
    return covariates


def read_communities(
    df: pd.DataFrame,
    id_col: str = "id",
    short_id_col: Optional[str] = "short_id",
    title_col: str = "title",
    level_col: str = "level",
    entities_col: Optional[str] = "entity_ids",
    relationships_col: Optional[str] = "relationship_ids",
    covariates_col: Optional[str] = "covariate_ids",
    attributes_cols: Optional[List[str]] = None,
) -> List[_model.Community]:
    """Read communities from a dataframe."""
    communities = []
    for idx, row in df.iterrows():
        comm = _model.Community(
            id=_utils.to_str(row, id_col),
            short_id=_utils.to_optional_str(row, short_id_col) if short_id_col else str(idx),
            title=_utils.to_str(row, title_col),
            level=_utils.to_str(row, level_col),
            entity_ids=_utils.to_optional_list(row, entities_col, item_type=str),
            relationship_ids=_utils.to_optional_list(row, relationships_col, item_type=str),
            covariate_ids=_utils.to_optional_dict(
                row, covariates_col, key_type=str, value_type=str
            ),
            attributes=(
                {col: row.get(col) for col in attributes_cols} if attributes_cols else None
            ),
        )
        communities.append(comm)
    return communities


def read_community_reports(
    df: pd.DataFrame,
    id_col: str = "id",
    short_id_col: Optional[str] = "short_id",
    title_col: str = "title",
    community_col: str = "community",
    summary_col: str = "summary",
    content_col: str = "full_content",
    rank_col: Optional[str] = "rank",
    summary_embedding_col: Optional[str] = "summary_embedding",
    content_embedding_col: Optional[str] = "full_content_embedding",
    attributes_cols: Optional[List[str]] = None,
) -> List[_model.CommunityReport]:
    """Read community reports from a dataframe."""
    reports = []
    for idx, row in df.iterrows():
        report = _model.CommunityReport(
            id=_utils.to_str(row, id_col),
            short_id=_utils.to_optional_str(row, short_id_col) if short_id_col else str(idx),
            title=_utils.to_str(row, title_col),
            community_id=_utils.to_str(row, community_col),
            summary=_utils.to_str(row, summary_col),
            full_content=_utils.to_str(row, content_col),
            rank=_utils.to_optional_float(row, rank_col) or 0.0,
            summary_embedding=_utils.to_optional_list(
                row, summary_embedding_col, item_type=float
            ),
            full_content_embedding=_utils.to_optional_list(
                row, content_embedding_col, item_type=float
            ),
            attributes=(
                {col: row.get(col) for col in attributes_cols} if attributes_cols else None
            ),
        )
        reports.append(report)
    return reports


def read_text_units(
    df: pd.DataFrame,
    id_col: str = "id",
    short_id_col: Optional[str] = "short_id",
    text_col: str = "text",
    entities_col: Optional[str] = "entity_ids",
    relationships_col: Optional[str] = "relationship_ids",
    covariates_col: Optional[str] = "covariate_ids",
    tokens_col: Optional[str] = "n_tokens",
    document_ids_col: Optional[str] = "document_ids",
    embedding_col: Optional[str] = "text_embedding",
    attributes_cols: Optional[List[str]] = None,
) -> List[_model.TextUnit]:
    """Read text units from a dataframe."""
    text_units = []
    for idx, row in df.iterrows():
        chunk = _model.TextUnit(
            id=_utils.to_str(row, id_col),
            short_id=_utils.to_optional_str(row, short_id_col) if short_id_col else str(idx),
            text=_utils.to_str(row, text_col),
            entity_ids=_utils.to_optional_list(row, entities_col, item_type=str),
            relationship_ids=_utils.to_optional_list(row, relationships_col, item_type=str),
            covariate_ids=_utils.to_optional_dict(
                row, covariates_col, key_type=str, value_type=str
            ),
            text_embedding=_utils.to_optional_list(row, embedding_col, item_type=float),  # type: ignore
            n_tokens=_utils.to_optional_int(row, tokens_col),
            document_ids=_utils.to_optional_list(row, document_ids_col, item_type=str),
            attributes=(
                {col: row.get(col) for col in attributes_cols} if attributes_cols else None
            ),
        )
        text_units.append(chunk)
    return text_units


def read_documents(
    df: pd.DataFrame,
    id_col: str = "id",
    short_id_col: str = "short_id",
    title_col: str = "title",
    type_col: str = "type",
    summary_col: Optional[str] = "entities",
    raw_content_col: Optional[str] = "relationships",
    summary_embedding_col: Optional[str] = "summary_embedding",
    content_embedding_col: Optional[str] = "raw_content_embedding",
    text_units_col: Optional[str] = "text_units",
    attributes_cols: Optional[List[str]] = None,
) -> List[_model.Document]:
    """Read documents from a dataframe."""
    docs = []
    for idx, row in df.iterrows():
        doc = _model.Document(
            id=_utils.to_str(row, id_col),
            short_id=_utils.to_optional_str(row, short_id_col) if short_id_col else str(idx),
            title=_utils.to_str(row, title_col),
            type=_utils.to_str(row, type_col),
            summary=_utils.to_optional_str(row, summary_col),
            raw_content=_utils.to_str(row, raw_content_col),
            summary_embedding=_utils.to_optional_list(
                row, summary_embedding_col, item_type=float
            ),
            raw_content_embedding=_utils.to_optional_list(
                row, content_embedding_col, item_type=float
            ),
            text_units=to_list(row, text_units_col, item_type=str),  # type: ignore
            attributes=(
                {col: row.get(col) for col in attributes_cols} if attributes_cols else None
            ),
        )
        docs.append(doc)
    return docs
