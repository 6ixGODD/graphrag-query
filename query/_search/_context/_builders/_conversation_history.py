# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import (
    Dict,
    List,
    Literal,
    Optional,
    Self,
)

import pandas as pd
import tiktoken

from .... import _utils
from ...._search._context import _types

ROLE__SYSTEM = "system"
ROLE__USER = "user"
ROLE__ASSISTANT = "assistant"


class ConversationRole(str, Enum):
    """Enum for conversation roles."""

    SYSTEM = ROLE__SYSTEM
    USER = ROLE__USER
    ASSISTANT = ROLE__ASSISTANT

    @staticmethod
    def from_string(value: str) -> "ConversationRole":
        """Convert string to ConversationRole."""
        match value:
            case ConversationRole.SYSTEM.value:
                return ConversationRole.SYSTEM
            case ConversationRole.USER.value:
                return ConversationRole.USER
            case ConversationRole.ASSISTANT.value:
                return ConversationRole.ASSISTANT

        raise ValueError(f"Invalid Role: {value}")

    def __str__(self) -> str:
        return self.value


@dataclass
class ConversationTurn:
    """Data class for storing a single conversation turn."""

    role: ConversationRole
    content: str

    def __str__(self) -> str:
        """Return string representation of the conversation turn."""
        return f"{self.role}: {self.content}"


@dataclass
class QATurn:
    """
    Data class for storing a QA turn.

    A QA turn contains a user question and one more multiple assistant answers.
    """

    user_query: ConversationTurn
    assistant_answers: Optional[List[ConversationTurn]] = None

    def get_answer_text(self) -> Optional[str]:
        """Get the text of the assistant answers."""
        return (
            "\n".join([answer.content for answer in self.assistant_answers])
            if self.assistant_answers else None
        )

    def __str__(self) -> str:
        """Return string representation of the QA turn."""
        answers = self.get_answer_text()
        return (
            f"Question: {self.user_query.content}\nAnswer: {answers}"
            if answers else f"Question: {self.user_query.content}"
        )


class ConversationHistory:
    """Class for storing a conversation history."""

    _turns: List[ConversationTurn] = []
    _max_length: Optional[int] = None

    @property
    def max_length(self) -> Optional[int]:
        """Get the maximum length of the conversation history."""
        return self._max_length

    @max_length.setter
    def max_length(self, value: int) -> None:
        """Set the maximum length of the conversation history."""
        self._max_length = value

    @classmethod
    def from_list(
        cls,
        conversation_turns: List[Dict[Literal["role", "content"], str]],
        max_length: Optional[int] = None,
    ) -> Self:
        """
        Create a conversation history from a list of conversation turns.

        Each turn is a dictionary in the form of `{"role": "<conversation_role>", "content": "<turn content>"}`
        """
        history = cls()
        for turn in conversation_turns:
            history._turns.append(
                ConversationTurn(
                    role=ConversationRole.from_string(turn.get("role", ConversationRole.USER)),
                    content=turn.get("content", ""),
                )
            )
            if max_length and len(history._turns) >= max_length:
                history._turns.pop(0)
        return history

    def add_turn(self, role: ConversationRole, content: str) -> None:
        """Add a new turn to the conversation history."""
        self._turns.append(ConversationTurn(role=role, content=content))

    def to_qa_turns(self) -> List[QATurn]:
        """Convert conversation history to a list of QA turns."""
        qa_turns: List[QATurn] = []
        current_qa_turn = None
        for turn in self._turns:
            if turn.role == ConversationRole.USER:
                if current_qa_turn:
                    qa_turns.append(current_qa_turn)
                current_qa_turn = QATurn(user_query=turn, assistant_answers=[])
            else:
                if current_qa_turn:
                    current_qa_turn.assistant_answers.append(turn)  # type: ignore
        if current_qa_turn:
            qa_turns.append(current_qa_turn)
        return qa_turns

    def get_user_turns(self, max_user_turns: int = 1) -> List[str]:
        """Get the last user turns in the conversation history."""
        user_turns = []
        for turn in self._turns[::-1]:
            if turn.role == ConversationRole.USER:
                user_turns.append(turn.content)
                if max_user_turns and len(user_turns) >= max_user_turns:
                    break
        return user_turns

    def build_context(
        self,
        token_encoder: Optional[tiktoken.Encoding] = None,
        include_user_turns_only: bool = True,
        max_qa_turns: int = 5,
        max_tokens: int = 8000,
        recency_bias: bool = True,
        column_delimiter: str = "|",
        context_name: str = "Conversation History",
    ) -> _types.SingleContext_T:
        """
        Prepare conversation history as context data for system prompt.
        """
        qa_turns = self.to_qa_turns()
        if include_user_turns_only:
            qa_turns = [
                QATurn(user_query=qa_turn.user_query, assistant_answers=None)
                for qa_turn in qa_turns
            ]
        if recency_bias:
            qa_turns = qa_turns[::-1]
        if max_qa_turns and len(qa_turns) > max_qa_turns:
            qa_turns = qa_turns[:max_qa_turns]

        # build context for qa turns
        # add context header
        if len(qa_turns) == 0 or not qa_turns:
            return "", {context_name: pd.DataFrame()}

        # add table header
        header = f"-----{context_name}-----" + "\n"

        turn_list = []
        current_context_df = pd.DataFrame()
        for turn in qa_turns:
            turn_list.append(
                {
                    "turn":    ConversationRole.USER.__str__(),
                    "content": turn.user_query.content,
                }
            )
            if turn.assistant_answers:
                turn_list.append(
                    {
                        "turn":    ConversationRole.ASSISTANT.__str__(),
                        "content": turn.get_answer_text() or "",
                    }
                )

            context_df = pd.DataFrame(turn_list)
            context_text = header + context_df.to_csv(sep=column_delimiter, index=False)
            if _utils.num_tokens(context_text, token_encoder) > max_tokens:
                break

            current_context_df = context_df
        context_text = header + current_context_df.to_csv(
            sep=column_delimiter, index=False
        )
        return context_text, {context_name.lower(): current_context_df}

    def to_dict(self) -> List[Dict[str, str]]:
        """Convert conversation history to a list of dictionaries."""
        return [{"role": turn.role.value, "content": turn.content}
                for turn in self._turns][-(self._max_length or 0):]
