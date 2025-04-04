from __future__ import annotations

import typing

import pandas as pd

from ... import _model


def get_candidate_communities(
    selected_entities: typing.List[_model.Entity],
    community_reports: typing.List[_model.CommunityReport],
    include_community_rank: bool = False,
    use_community_summary: bool = False,
) -> pd.DataFrame:
    """Get all communities that are related to selected entities."""
    selected_community_ids_ = [
        entity.community_ids for entity in selected_entities if entity.community_ids
    ]
    selected_community_ids = [
        item for sublist in selected_community_ids_ for item in sublist
    ]
    selected_reports = [
        community
        for community in community_reports if community.id in selected_community_ids
    ]
    return to_community_report_dataframe(
        reports=selected_reports,
        include_community_rank=include_community_rank,
        use_community_summary=use_community_summary,
    )


def to_community_report_dataframe(
    reports: typing.List[_model.CommunityReport],
    include_community_rank: bool = False,
    use_community_summary: bool = False,
) -> pd.DataFrame:
    """Convert a list of communities to a pandas dataframe."""
    if len(reports) == 0:
        return pd.DataFrame()

    # add header
    header = ["id", "title"]
    attribute_cols = list(reports[0].attributes.keys()) if reports[0].attributes else []
    attribute_cols = [col for col in attribute_cols if col not in header]
    header.extend(attribute_cols)
    header.append("summary" if use_community_summary else "content")
    if include_community_rank:
        header.append("rank")

    records = []
    for report in reports:
        new_record = [report.short_id if report.short_id else "", report.title, *[
            str(report.attributes.get(field, ""))
            if report.attributes and report.attributes.get(field)
            else ""
            for field in attribute_cols
        ], report.summary if use_community_summary else report.full_content]
        if include_community_rank:
            new_record.append(str(report.rank))
        records.append(new_record)
    return pd.DataFrame(records, columns=typing.cast(typing.Any, header))
