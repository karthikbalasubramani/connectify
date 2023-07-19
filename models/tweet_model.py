import dataclasses
from typing import List
from typing import Optional

import strawberry
from bson import ObjectId

from models.user_model import User


# Get Tweets Response Model
@strawberry.type
class TweetModel:
    id: Optional[str] = None
    description: Optional[str] = None
    hashtags: Optional[str] = None
    likes_count: int = 0
    liked_users: List[User] = None

    @classmethod
    def from_dict(cls, data):
        instance = cls()
        user_details = []
        for key, value in data.items():
            if isinstance(value, ObjectId):
                setattr(instance, key, value)
                continue
            elif key == "liked_users":
                for user in value:
                    user_details.append(User().from_dict(user))
                setattr(instance, key, user_details)
                continue
            setattr(instance, key, value)
        return instance


# SingleTweetModel
@strawberry.type
class SingleTweetModel:
    tweet: TweetModel
    success: bool

    @classmethod
    def from_dict(cls, data):
        instance = cls()
        for key, value in data.items():
            if isinstance(value, ObjectId):
                setattr(instance, key, value)
                continue
            setattr(instance, key, value)
        return instance


# List of Tweets
@strawberry.type
class ListTweetModel:
    success: bool
    tweets: List[TweetModel]


# UpdateTweetInput
@strawberry.input
class UpdateTweetInput:
    description: Optional[str] = None
    hashtags: Optional[str] = None

    def to_dict(self) -> dict:
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data):
        instance = cls()
        for key, value in data.items():
            if isinstance(value, ObjectId):
                setattr(instance, key, value)
                continue
            setattr(instance, key, value)
        return instance
