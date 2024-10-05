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

import typing

import pydantic
import typing_extensions

__all__ = [
    'GraphRAGError',
    'ClientError',
    'CLIError',
    'InvalidMessageError',
    'InvalidEngineError',
    'InvalidParameterError',
]


class GraphRAGError(Exception):
    ...


class ClientError(GraphRAGError):
    ...


class CLIError(GraphRAGError):
    ...


# Client Errors
class InvalidMessageError(ClientError):
    def __init__(
        self,
        message: str = "The message must be in the format of alternating roles with the last role being 'user'"
    ):
        self.message = message
        super().__init__(message)

    @typing_extensions.override
    def __str__(self):
        return self.message

    @typing_extensions.override
    def __repr__(self):
        return f"{self.__class__.__name__}(message={self.message!r})"


class InvalidEngineError(ClientError):
    def __init__(
        self,
        engine: str,
        message: str = "Invalid engine. Must be either 'local' or 'global'"
    ):
        self.engine = engine
        self.message = message
        super().__init__(message)

    @typing_extensions.override
    def __str__(self):
        return self.message

    @typing_extensions.override
    def __repr__(self):
        return f"{self.__class__.__name__}(engine={self.engine!r}, message={self.message!r})"


# CLI Errors
class InvalidParameterError(CLIError):
    def __init__(
        self,
        *,
        params: typing.List[str],
        reason: typing.List[typing.Optional[str]],
        message: str = "Invalid parameter(s): \n"
    ) -> None:
        self.params = params
        self.reason = reason
        self.message = message
        for i in range(len(params)):
            self.message += f"  - {params[i]}: {reason[i] or 'Invalid parameter'}\n"
        super().__init__(self.message)

    @classmethod
    def from_pydantic_validation_error(cls, validation_error: pydantic.ValidationError) -> typing.Self:
        params = []
        reason = []
        for error in validation_error.errors():
            params.append(error["loc"][0])
            reason.append(error["msg"])
        return cls(params=params, reason=reason)

    @typing_extensions.override
    def __str__(self):
        return self.message

    @typing_extensions.override
    def __repr__(self):
        return f"{self.__class__.__name__}(params={self.params!r}, message={self.message!r})"
