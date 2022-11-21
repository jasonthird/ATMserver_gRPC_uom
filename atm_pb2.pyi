from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AuthenticateRequest(_message.Message):
    __slots__ = ["pin", "username"]
    PIN_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    pin: int
    username: str
    def __init__(self, username: _Optional[str] = ..., pin: _Optional[int] = ...) -> None: ...

class AuthenticateResponse(_message.Message):
    __slots__ = ["AuthCode", "error", "success"]
    AUTHCODE_FIELD_NUMBER: _ClassVar[int]
    AuthCode: str
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    error: str
    success: bool
    def __init__(self, success: bool = ..., error: _Optional[str] = ..., AuthCode: _Optional[str] = ...) -> None: ...

class BalanceReply(_message.Message):
    __slots__ = ["denomination", "error", "success", "units"]
    DENOMINATION_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    denomination: int
    error: str
    success: bool
    units: int
    def __init__(self, success: bool = ..., error: _Optional[str] = ..., units: _Optional[int] = ..., denomination: _Optional[int] = ...) -> None: ...

class BalanceRequest(_message.Message):
    __slots__ = ["AuthCode"]
    AUTHCODE_FIELD_NUMBER: _ClassVar[int]
    AuthCode: str
    def __init__(self, AuthCode: _Optional[str] = ...) -> None: ...

class DepositReply(_message.Message):
    __slots__ = ["denomination", "error", "success", "units"]
    DENOMINATION_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    denomination: int
    error: str
    success: bool
    units: int
    def __init__(self, success: bool = ..., error: _Optional[str] = ..., units: _Optional[int] = ..., denomination: _Optional[int] = ...) -> None: ...

class DepositRequest(_message.Message):
    __slots__ = ["AuthCode", "denomination", "units"]
    AUTHCODE_FIELD_NUMBER: _ClassVar[int]
    AuthCode: str
    DENOMINATION_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    denomination: int
    units: int
    def __init__(self, AuthCode: _Optional[str] = ..., units: _Optional[int] = ..., denomination: _Optional[int] = ...) -> None: ...

class WithdrawReply(_message.Message):
    __slots__ = ["denomination", "error", "success", "units"]
    DENOMINATION_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    denomination: int
    error: str
    success: bool
    units: int
    def __init__(self, success: bool = ..., error: _Optional[str] = ..., units: _Optional[int] = ..., denomination: _Optional[int] = ...) -> None: ...

class WithdrawRequest(_message.Message):
    __slots__ = ["AuthCode", "denomination", "units"]
    AUTHCODE_FIELD_NUMBER: _ClassVar[int]
    AuthCode: str
    DENOMINATION_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    denomination: int
    units: int
    def __init__(self, AuthCode: _Optional[str] = ..., units: _Optional[int] = ..., denomination: _Optional[int] = ...) -> None: ...
