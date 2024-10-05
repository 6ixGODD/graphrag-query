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

import abc
import typing
import warnings

import pandas as pd
import tiktoken
import typing_extensions

from .... import (
    _utils,
    _vector_stores,
)
from ...._search import (
    _llm,
    _model,
)
from ...._search._context import _types
from ...._search._context._builders import (
    _community_context,
    _conversation_history,
    _entity_extraction,
    _local_context,
    _source_context,
)
from ...._search._input._retrieval import (
    _community_reports,
    _text_units,
)


class BaseContextBuilder(abc.ABC):
    @abc.abstractmethod
    def build_context(self, *args: typing.Any, **kwargs: typing.Any) -> _types.Context_T: ...


class GlobalContextBuilder(BaseContextBuilder):

    def __init__(
        self,
        *,
        community_reports: typing.List[_model.CommunityReport],
        entities: typing.Optional[typing.List[_model.Entity]] = None,
        token_encoder: typing.Optional[tiktoken.Encoding] = None,
        random_state: int = 42,
    ):
        self._community_reports = community_reports
        self._entities = entities
        self._token_encoder = token_encoder
        self._random_state = random_state

    @typing_extensions.override
    def build_context(
        self,
        *,
        conversation_history: typing.Optional[_conversation_history.ConversationHistory] = None,
        use_community_summary: bool = True,
        column_delimiter: str = "|",
        shuffle_data: bool = True,
        include_community_rank: bool = False,
        min_community_rank: int = 0,
        community_rank_name: str = "rank",
        include_community_weight: bool = True,
        community_weight_name: str = "occurrence",
        normalize_community_weight: bool = True,
        max_tokens: int = 8000,
        context_name: str = "Reports",
        conversation_history_user_turns_only: bool = True,
        conversation_history_max_turns: int = 5,
        **kwargs: typing.Any,
    ) -> _types.Context_T:
        """Prepare batches of community report data table as context data for global search."""
        conversation_history_context = ""
        final_context_data = {}
        if conversation_history:
            # build conversation history context
            (
                conversation_history_context,
                conversation_history_context_data,
            ) = conversation_history.build_context(
                include_user_turns_only=conversation_history_user_turns_only,
                max_qa_turns=conversation_history_max_turns,
                column_delimiter=column_delimiter,
                max_tokens=max_tokens,
                recency_bias=False,
            )
            if conversation_history_context != "":
                final_context_data = conversation_history_context_data

        community_context, community_context_data = _community_context.build_community_context(
            community_reports=self._community_reports,
            entities=self._entities,
            token_encoder=self._token_encoder,
            use_community_summary=use_community_summary,
            column_delimiter=column_delimiter,
            shuffle_data=shuffle_data,
            include_community_rank=include_community_rank,
            min_community_rank=min_community_rank,
            community_rank_name=community_rank_name,
            include_community_weight=include_community_weight,
            community_weight_name=community_weight_name,
            normalize_community_weight=normalize_community_weight,
            max_tokens=max_tokens,
            single_batch=False,
            context_name=context_name,
            random_state=self._random_state,
        )
        final_context_data.update(community_context_data)
        if isinstance(community_context, list):
            return [
                f"{conversation_history_context}\n\n{context}"
                for context in community_context
            ], final_context_data
        else:
            return f"{conversation_history_context}\n\n{community_context}", final_context_data


class LocalContextBuilder(BaseContextBuilder):

    def __init__(
        self,
        *,
        entities: typing.List[_model.Entity],
        entity_text_embeddings: _vector_stores.BaseVectorStore,
        text_embedder: _llm.BaseEmbedding,
        text_units: typing.Optional[typing.List[_model.TextUnit]] = None,
        community_reports: typing.Optional[typing.List[_model.CommunityReport]] = None,
        relationships: typing.Optional[typing.List[_model.Relationship]] = None,
        covariates: typing.Optional[typing.Dict[str, typing.List[_model.Covariate]]] = None,
        token_encoder: typing.Optional[tiktoken.Encoding] = None,
        embedding_vectorstore_key: str = _entity_extraction.EntityVectorStoreKey.ID,
    ) -> None:
        community_reports = community_reports or []
        relationships = relationships or []
        covariates = covariates or {}
        text_units = text_units or []

        self.entities = {
            entity.id: entity for entity in entities
        }
        self.community_reports = {
            community.id: community for community in community_reports
        }
        self.text_units = {
            unit.id: unit for unit in text_units
        }
        self.relationships = {
            relationship.id: relationship for relationship in relationships
        }

        self.covariates = covariates
        self.entity_text_embeddings = entity_text_embeddings
        self.text_embedder = text_embedder
        self.token_encoder = token_encoder
        self.embedding_vectorstore_key = embedding_vectorstore_key

    def filter_by_entity_keys(self, entity_keys: typing.Union[typing.List[int], typing.List[str]]) -> None:
        """Filter entity text embeddings by entity keys."""
        self.entity_text_embeddings.filter_by_id(entity_keys)

    @typing_extensions.override
    def build_context(
        self,
        *,
        query: str,
        conversation_history: typing.Optional[_conversation_history.ConversationHistory] = None,
        include_entity_names: typing.Optional[typing.List[str]] = None,
        exclude_entity_names: typing.Optional[typing.List[str]] = None,
        conversation_history_max_turns: int = 5,
        conversation_history_user_turns_only: bool = True,
        max_tokens: int = 8000,
        text_unit_prop: float = 0.5,
        community_prop: float = 0.25,
        top_k_mapped_entities: int = 10,
        top_k_relationships: int = 10,
        include_community_rank: bool = False,
        include_entity_rank: bool = False,
        rank_description: str = "number of relationships",
        include_relationship_weight: bool = False,
        relationship_ranking_attribute: str = "rank",
        return_candidate_context: bool = False,
        use_community_summary: bool = False,
        min_community_rank: int = 0,
        community_context_name: str = "Reports",
        column_delimiter: str = "|",
        **kwargs: typing.Any,
    ) -> _types.Context_T:
        """
        Build data context for local search prompt.

        Build a context by combining community reports and entity/relationship/covariate tables,
        and text units using a predefined ratio set by summary_prop.
        """
        include_entity_names = include_entity_names or []
        exclude_entity_names = exclude_entity_names or []
        if community_prop + text_unit_prop > 1:
            raise ValueError("The sum of community_prop and text_unit_prop should not exceed 1.")

        # map user query to entities
        # if there is conversation history, attached the previous user questions to the current query
        if conversation_history:
            pre_user_questions = "\n".join(
                conversation_history.get_user_turns(conversation_history_max_turns)
            )
            query = f"{query}\n{pre_user_questions}"

        selected_entities = _entity_extraction.map_query_to_entities(
            query=query,
            text_embedding_vectorstore=self.entity_text_embeddings,
            text_embedder=self.text_embedder,
            all_entities=list(self.entities.values()),
            embedding_vectorstore_key=self.embedding_vectorstore_key,
            include_entity_names=include_entity_names,
            exclude_entity_names=exclude_entity_names,
            k=top_k_mapped_entities,
            oversample_scaler=2,
        )

        # build context
        final_context: typing.List[str] = []
        final_context_data: typing.Dict[str, pd.DataFrame] = {}

        # build community context
        community_tokens = max(int(max_tokens * community_prop), 0)
        community_context, community_context_data = self._build_community_context(
            selected_entities=selected_entities,
            max_tokens=community_tokens,
            use_community_summary=use_community_summary,
            column_delimiter=column_delimiter,
            include_community_rank=include_community_rank,
            min_community_rank=min_community_rank,
            return_candidate_context=return_candidate_context,
            context_name=community_context_name,
        )
        if community_context.strip() != "":
            final_context.append(community_context)
            final_context_data = {**final_context_data, **community_context_data}

        # build local (i.e. entity-relationship-covariate) context
        local_prop = 1 - community_prop - text_unit_prop
        local_tokens = max(int(max_tokens * local_prop), 0)
        local_context, local_context_data = self._build_local_context(
            selected_entities=selected_entities,
            max_tokens=local_tokens,
            include_entity_rank=include_entity_rank,
            rank_description=rank_description,
            include_relationship_weight=include_relationship_weight,
            top_k_relationships=top_k_relationships,
            relationship_ranking_attribute=relationship_ranking_attribute,
            return_candidate_context=return_candidate_context,
            column_delimiter=column_delimiter,
        )
        if local_context.strip() != "":
            final_context.append(str(local_context))
            final_context_data = {**final_context_data, **local_context_data}

        # build text unit context
        text_unit_tokens = max(int(max_tokens * text_unit_prop), 0)
        text_unit_context, text_unit_context_data = self._build_text_unit_context(
            selected_entities=selected_entities,
            max_tokens=text_unit_tokens,
            return_candidate_context=return_candidate_context,
        )
        if text_unit_context.strip() != "":
            final_context.append(text_unit_context)
            final_context_data = {**final_context_data, **text_unit_context_data}

        return "\n\n".join(final_context), final_context_data

    def _build_community_context(
        self,
        *,
        selected_entities: typing.List[_model.Entity],
        max_tokens: int = 4000,
        use_community_summary: bool = False,
        column_delimiter: str = "|",
        include_community_rank: bool = False,
        min_community_rank: int = 0,
        return_candidate_context: bool = False,
        context_name: str = "Reports",
    ) -> _types.SingleContext_T:
        """Add community data to the context window until it hits the max_tokens limit."""
        if len(selected_entities) == 0 or len(self.community_reports) == 0:
            return "", {context_name.lower(): pd.DataFrame()}

        community_matches: typing.Dict[str, int] = {}
        for entity in selected_entities:
            # increase count of the community that this entity belongs to
            if entity.community_ids:
                for community_id in entity.community_ids:
                    community_matches[community_id] = community_matches.get(community_id, 0) + 1

        # sort communities by number of matched entities and rank
        selected_communities = [
            self.community_reports[community_id]
            for community_id in community_matches if community_id in self.community_reports
        ]
        for community in selected_communities:
            if community.attributes is None:
                community.attributes = {}
            community.attributes["matches"] = community_matches[community.id]
        selected_communities.sort(
            key=lambda x: (x.attributes["matches"], x.rank),  # type: ignore
            reverse=True,  # type: ignore
        )
        for community in selected_communities:
            del community.attributes["matches"]  # type: ignore

        context_text, context_data = _community_context.build_community_context(
            community_reports=selected_communities,
            token_encoder=self.token_encoder,
            use_community_summary=use_community_summary,
            column_delimiter=column_delimiter,
            shuffle_data=False,
            include_community_rank=include_community_rank,
            min_community_rank=min_community_rank,
            max_tokens=max_tokens,
            single_batch=True,
            context_name=context_name,
        )
        if isinstance(context_text, list) and len(context_text) > 0:
            context_text = "\n\n".join(context_text)

        if return_candidate_context:
            candidate_context_data = _community_reports.get_candidate_communities(
                selected_entities=selected_entities,
                community_reports=list(self.community_reports.values()),
                use_community_summary=use_community_summary,
                include_community_rank=include_community_rank,
            )
            context_key = context_name.lower()
            if context_key not in context_data:
                context_data[context_key] = candidate_context_data
                context_data[context_key]["in_context"] = False
            else:
                if (
                        "id" in candidate_context_data.columns
                        and "id" in context_data[context_key].columns
                ):
                    candidate_context_data["in_context"] = candidate_context_data["id"].isin(  # cspell:disable-line
                        context_data[context_key]["id"]
                    )
                    context_data[context_key] = candidate_context_data
                else:
                    context_data[context_key]["in_context"] = True
        return str(context_text), context_data

    def _build_text_unit_context(
        self,
        *,
        selected_entities: typing.List[_model.Entity],
        max_tokens: int = 8000,
        return_candidate_context: bool = False,
        column_delimiter: str = "|",
        context_name: str = "Sources",
    ) -> _types.SingleContext_T:
        """Rank matching text units and add them to the context window until it hits the max_tokens limit."""
        if not selected_entities or not self.text_units:
            return "", {context_name.lower(): pd.DataFrame()}

        selected_text_units = []
        text_unit_ids_set = set()

        for index, entity in enumerate(selected_entities):
            for text_id in entity.text_unit_ids or []:
                if text_id not in text_unit_ids_set and text_id in self.text_units:
                    text_unit_ids_set.add(text_id)
                    selected_unit = self.text_units[text_id]
                    num_relationships = _source_context.count_relationships(
                        selected_unit, entity, self.relationships
                    )
                    if selected_unit.attributes is None:
                        selected_unit.attributes = {}
                    selected_unit.attributes["entity_order"] = index
                    selected_unit.attributes["num_relationships"] = num_relationships
                    selected_text_units.append(selected_unit)

        selected_text_units.sort(
            key=lambda x: (
                x.attributes["entity_order"], -x.attributes["num_relationships"],  # type: ignore
            )
        )

        for unit in selected_text_units:
            unit.attributes.pop("entity_order", None)  # type: ignore
            unit.attributes.pop("num_relationships", None)  # type: ignore

        context_text, context_data = _source_context.build_text_unit_context(
            text_units=selected_text_units,
            token_encoder=self.token_encoder,
            max_tokens=max_tokens,
            shuffle_data=False,
            context_name=context_name,
            column_delimiter=column_delimiter,
        )

        if return_candidate_context:
            candidate_context_data = _text_units.get_candidate_text_units(
                selected_entities=selected_entities,
                text_units=list(self.text_units.values()),
            )
            context_key = context_name.lower()
            if context_key not in context_data:
                candidate_context_data["in_context"] = False
                context_data[context_key] = candidate_context_data
            else:
                if (
                        "id" in candidate_context_data.columns and "id" in context_data[context_key].columns
                ):
                    candidate_context_data["in_context"] = candidate_context_data["id"].isin(
                        context_data[context_key]["id"]
                    )
                    context_data[context_key] = candidate_context_data
                else:
                    context_data[context_key]["in_context"] = True

        return str(context_text), context_data

    def _build_local_context(
        self,
        *,
        selected_entities: typing.List[_model.Entity],
        max_tokens: int = 8000,
        include_entity_rank: bool = False,
        rank_description: str = "relationship count",
        include_relationship_weight: bool = False,
        top_k_relationships: int = 10,
        relationship_ranking_attribute: str = "rank",
        return_candidate_context: bool = False,
        column_delimiter: str = "|",
    ) -> _types.SingleContext_T:
        """Build data context for local search prompt combining entity/relationship/covariate tables."""
        # build entity context
        entity_context, entity_context_data = _local_context.build_entity_context(
            selected_entities=selected_entities,
            token_encoder=self.token_encoder,
            max_tokens=max_tokens,
            column_delimiter=column_delimiter,
            include_entity_rank=include_entity_rank,
            rank_description=rank_description,
            context_name="Entities",
        )
        entity_tokens = _utils.num_tokens(entity_context, self.token_encoder)

        # build relationship-covariate context
        added_entities = []
        final_context = []
        final_context_data = {}

        # gradually add entities and associated metadata to the context until we reach limit
        for entity in selected_entities:
            current_context = []
            current_context_data = {}
            added_entities.append(entity)

            # build relationship context
            (
                relationship_context,
                relationship_context_data,
            ) = _local_context.build_relationship_context(
                selected_entities=added_entities,
                relationships=list(self.relationships.values()),
                token_encoder=self.token_encoder,
                max_tokens=max_tokens,
                column_delimiter=column_delimiter,
                top_k_relationships=top_k_relationships,
                include_relationship_weight=include_relationship_weight,
                relationship_ranking_attribute=relationship_ranking_attribute,
                context_name="Relationships",
            )
            current_context.append(relationship_context)
            current_context_data["relationships"] = relationship_context_data
            total_tokens = entity_tokens + _utils.num_tokens(relationship_context, self.token_encoder)

            # build covariate context
            for covariate in self.covariates:
                covariate_context, covariate_context_data = _local_context.build_covariates_context(
                    selected_entities=added_entities,
                    covariates=self.covariates[covariate],
                    token_encoder=self.token_encoder,
                    max_tokens=max_tokens,
                    column_delimiter=column_delimiter,
                    context_name=covariate,
                )
                total_tokens += _utils.num_tokens(covariate_context, self.token_encoder)
                current_context.append(covariate_context)
                current_context_data[covariate.lower()] = covariate_context_data

            if total_tokens > max_tokens:
                warnings.warn("Reached token limit - reverting to previous context state", RuntimeWarning)
                break

            final_context = current_context
            final_context_data = current_context_data

        # attach entity context to final context
        final_context_text = entity_context + "\n\n" + "\n\n".join(final_context)
        final_context_data["entities"] = entity_context_data

        if return_candidate_context:
            # we return all the candidate entities/relationships/covariates (not only those that were fitted into the
            # context window)
            # and add a tag to indicate which records were included in the context window
            candidate_context_data = _local_context.get_candidate_context(
                selected_entities=selected_entities,
                entities=list(self.entities.values()),
                relationships=list(self.relationships.values()),
                covariates=self.covariates,
                include_entity_rank=include_entity_rank,
                entity_rank_description=rank_description,
                include_relationship_weight=include_relationship_weight,
            )
            for key in candidate_context_data:
                candidate_df = candidate_context_data[key]
                if key not in final_context_data:
                    final_context_data[key] = candidate_df
                    final_context_data[key]["in_context"] = False
                else:
                    in_context_df = final_context_data[key]

                    if "id" in in_context_df.columns and "id" in candidate_df.columns:
                        candidate_df["in_context"] = candidate_df["id"].isin(  # cspell:disable-line
                            in_context_df["id"]
                        )
                        final_context_data[key] = candidate_df
                    else:
                        final_context_data[key]["in_context"] = True

        else:
            for key in final_context_data:
                final_context_data[key]["in_context"] = True
        return final_context_text, final_context_data
