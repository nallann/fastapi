from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Annotated, Optional
from .. import models, schemas, oauth2
from ..database import get_db


    # console request
    # fetch("http://localhost:8000/posts").then(res => res.json()).then(console.log)


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
    )



@router.get("/", response_model=List[schemas.PostVote])
def get_all_post(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user),
                 limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts """) 
    # posts = cursor.fetchall()

    # posts = db.execute(
    #     """SELECT posts.*, COUNT(votes.post_id) AS votes FROM posts LEFT JOIN votes 
    #     ON posts.id = votes.post_id GROUP BY posts.id""")
    # results = []
    # for post in posts:
    #     results.append(dict(post))
    # print(results)


    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts




@router.get("/{id}", response_model=schemas.PostVote)
def get_individual_posts(id: int, db: Session = Depends(get_db), 
                         current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = (%s) """, [id], binary=True)
    # post = cursor.fetchone()


    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id: {id} was not found")
    
            
    
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), 
                 current_user: dict = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), 
                current_user: dict = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM  posts WHERE id = (%s) RETURNING *""", [id], binary=True)
    # deleted_post = cursor.fetchone()
    # conn.commit()


    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate,  db: Session = Depends(get_db),
                current_user: dict = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = (%s), content = (%s), published = (%s) 
    #                WHERE id = (%s) RETURNING *""", 
    #                (post.title, post.content, post.published, id), binary=True)
    # updated_post = cursor.fetchone()
    # conn.commit()


    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
