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

import inspect
import json
import warnings
import typing

import json_repair


def filter_kwargs(
    func: typing.Callable,
    kwargs_: typing.Dict[str, typing.Any],
    prefix: str = ""
) -> typing.Dict[str, typing.Any]:
    """
    Filter out invalid keyword arguments for a given function by comparing the provided
    keyword arguments to the function's signature. Only valid keyword arguments are returned.

    This function filters out invalid keyword arguments for a given function by comparing
    the provided keyword arguments to the function's signature. Only valid keyword arguments
    are returned. It is useful for functions that accept keyword arguments that are not used
    by the function itself, but are instead used by other functions called by the function.

    Args:
        func (Callable): The function to filter keyword arguments for.
        kwargs_ (Dict[str, Any]): The keyword arguments to filter.
        prefix (str, optional): The prefix to add to the keyword arguments. Defaults to "".

    Returns:
        Dict[str, Any]: The filtered keyword arguments.
    """

    # Remove the prefix of the keyword arguments
    kwargs = {key[prefix.__len__():]: value for key, value in kwargs_.items() if key.startswith(prefix)}
    return {
        key: value
        for key, value in kwargs.items()
        if key in inspect.signature(func).parameters and key not in ["self", "cls"]
    }


def deserialize_json(json_: str) -> typing.Dict[str, typing.Any]:
    """
    Deserialize a JSON string, repairing it if necessary.

    This function deserializes a JSON string, repairing it if necessary. If the JSON string
    is malformed, it is repaired using the provided repair_json function. The repaired JSON
    string is then deserialized and returned as a dictionary.

    Args:
        json_ (str): The JSON string to deserialize.

    Returns:
        Dict[str, Any]: The deserialized JSON string as a dictionary.
    """

    try:
        result = json.loads(json_)
    except json.JSONDecodeError:
        # Fixup potentially malformed json string using json_repair.
        try:
            result = json_repair.repair_json(json_str=json_, return_objects=True)
        except json.JSONDecodeError:
            warnings.warn(f"Error loading JSON: {json_}", RuntimeWarning)
            return {}
    if not isinstance(result, dict):
        warnings.warn(f"Unexpected type: {type(result)}", RuntimeWarning)
        return {}
    return result
