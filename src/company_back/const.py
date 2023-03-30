from enum import Enum


class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class PurchaseStatus(str, Enum):
    PENDING = "pending"
    SUCCESS = "success"


class MatchStatus(str, Enum):
    PENDING = "pending"
    REJECTED = "rejected"
    ACCEPTED = "accepted"


class MessageStatus(str, Enum):
    SENT = "sent"
    DELETED = "deleted"
