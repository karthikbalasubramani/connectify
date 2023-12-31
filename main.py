import strawberry
import uvicorn
from fastapi import FastAPI
from strawberry.asgi import GraphQL

from mutation.comment_mutation import CommentMutattion
from mutation.likes_mutation import LikesMutattion
from mutation.tweet_mutation import TweetMutation
from mutation.user_mutation import UserMutation
from query.tweet_query import TweetQuery
from query.user_query import UserQuery

app = FastAPI()

# templates = Jinja2Templates(directory="templates")


# app.mount("/static", StaticFiles(directory="templates/static"), name="static")
# app.mount("/templates", StaticFiles(directory="templates"), name="templates")


# @app.get("/login", response_class=HTMLResponse)
# async def get_login(request: Request):
#     return templates.TemplateResponse("login.html", {"request": request})


# Mutation Class which imports all the functionalities Mutation Classes
@strawberry.type
class Mutation(UserMutation, TweetMutation, LikesMutattion, CommentMutattion):
    pass


# Query Class which imports all the functionalities Query Classes
@strawberry.type
class Query(UserQuery, TweetQuery):
    pass


# Initialize Fastapi application
schema = strawberry.Schema(query=Query, mutation=Mutation)

# Create the GraphQL app
graphql_app = GraphQL(schema)

# Add the GraphQL route to the FastAPI application
app.add_route("/graphql", graphql_app)

# Run the FastAPI application
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
