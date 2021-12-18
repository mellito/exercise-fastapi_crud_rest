from datetime import datetime
from typing import Text,Optional
from pydantic import BaseModel
from fastapi import FastAPI,Path,HTTPException
from uuid import uuid4 as uuid

app = FastAPI()

posts = []

#post model
class Post(BaseModel):
    id:Optional[str]
    tittle:str
    author:str
    content:Text
    created_at: datetime = datetime.now()
    published_at: Optional[datetime]
    published: bool = False

@app.get("/")
def read_root():
    return{"welcome":"to my api"}

@app.get("/post")
def  get_post():
    return posts

@app.post("/post")
def save_post(post:Post):
    post.id = str(uuid())
    posts.append(post.dict())
    return posts[-1]

@app.get("/post/{post_id}")
def get_post(post_id:str= Path(
    ...,
    min_length=1  
    )
):
    for post in posts:
        if post["id"] == post_id:
            return post
    raise HTTPException(status_code=404, detail="post not found")

@app.delete("/post/{post_id}")
def delete_post(post_id:str):
    for index,post in enumerate(posts):
        if post["id"]==post_id:
            posts.pop(index)
            return {"message": "psot has been deleted successfully"}
    raise HTTPException(status_code=404, detail="post not found")

@app.put("/post/{post_id}")
def update_post(post_id:str,updatepost:Post):
    for index,post in enumerate(posts):
        if post["id"] == post_id:
            posts[index]["tittle"] = updatepost.tittle
            posts[index]["content"] = updatepost.content
            posts[index]["author"] = updatepost.author
            return {"message": "post has been updated successfully"}
    raise HTTPException(status_code=404, detail="post not found")
