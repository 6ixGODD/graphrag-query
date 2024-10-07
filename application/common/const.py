# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from __future__ import annotations


class Constants:
    # HTTP Headers
    REQUEST_ID_HEADER = "x-request-id"
    AUTHORIZATION_HEADER = "authorization"

    # Logging Tags
    SYS_LOGGING_TAG = "SYSTEM"
    MIDDLEWARE_LOGGING_TAG = "MIDDLEWARE"
    DAO_LOGGING_TAG = "DAO"
    ROUTER_LOGGING_TAG = "ROUTER"

    # Context Keys
    REQUEST_ID_CTX_KEY = "request_id"
    IP_CTX_KEY = "ip"

    # Scope Keys
    HEADERS_SCOPE_KEY = "headers"
    TYPE_SCOPE_KEY = "type"
    CLIENT_SCOPE_KEY = "client"
    SERVER_SCOPE_KEY = "server"
    METHOD_SCOPE_KEY = "method"
    PATH_SCOPE_KEY = "path"

    # Message Keys
    TYPE_MESSAGE_KEY = "type"
    BODY_MESSAGE_KEY = "body"
    HEADERS_MESSAGE_KEY = "headers"
    STATUS_MESSAGE_KEY = "status"

    # ID Prefix
    REQUEST_ID_PREFIX = 'req'
    SERVICE_KEY_PREFIX = 'sk'
    CHAT_ID_PREFIX = 'chat'
    IMAGE_ID_PREFIX = 'img'

    # Cache Splitter
    CACHE_SPLITTER = ':'
