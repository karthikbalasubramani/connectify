from typing import List
from typing import Optional

import strawberry
from bson import ObjectId


# Get Tweets Response Model
@strawberry.type
class TweetModel:
    id: Optional[str] = None
    description: Optional[str] = None
    hashtags: Optional[str] = None

    @classmethod
    def from_dict(cls, data):
        instance = cls()
        for key, value in data.items():
            if isinstance(value, ObjectId):
                setattr(instance, key, value)
                continue
            setattr(instance, key, value)
        return instance


# SingleTweetModel
@strawberry.type
class SingleTweetModel:
    tweet: TweetModel
    success: bool


@strawberry.type
class ListTweetModel:
    success: bool
    tweets: List[TweetModel]
