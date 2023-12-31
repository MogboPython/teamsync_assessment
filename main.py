from schemas import *
from models import *
from utils import get_hashed_password, verify_password, create_access_token
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth import get_current_user

Base.metadata.create_all(engine)

app = FastAPI()

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@app.get("/api/v1/healthcheck")
def read_root():
    return {"status": "ok"}

@app.post("/api/v1/register")
async def register_user(user: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.query(User).filter_by(username=user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    encrypted_password = get_hashed_password(user.password)

    new_user = User(username=user.username, password=encrypted_password)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message":"user created successfully"}

@app.post('/api/v1/login' ,response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.query(User).filter_by(username=form_data.username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    hashed_pass = user.password
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": user.username}
    )

    return {"access_token": access_token, "token_type": "bearer"}
    
@app.post("/api/v1/post")
async def create_post(post: PostCreate, current_user: str = Depends(get_current_user), session: Session = Depends(get_session)):
    new_post = Post(title=post.title, content=post.content, author=current_user)
    session.add(new_post)
    session.commit()
    session.refresh(new_post)

    return {"message":f"post created successfully by {current_user}"}


@app.get("/api/v1/posts")
async def get_posts(session: Session = Depends(get_session)):
    posts = session.query(Post).all()
    return posts

@app.put("/api/v1/posts/{post_id}")
async def update_post(post_id: int, post_update: PostCreate, current_user: str = Depends(get_current_user),session: Session = Depends(get_session)):
    post = session.query(Post).filter_by(id = post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.author != current_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="You do not own this post",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    post.title = post_update.title
    post.content = post_update.content
    session.commit()
    session.refresh(post)
    
    return {"message": f"post updated successfully by {current_user}"}

@app.delete("/api/v1/posts/{post_id}")
async def delete_post(post_id: int, current_user: str = Depends(get_current_user), session: Session = Depends(get_session)):
    post = session.query(Post).filter_by(id = post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author != current_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="You do not own this post",
            headers={"WWW-Authenticate": "Bearer"},
        )
    session.delete(post)
    session.commit()
    return {"message": f"Post {post_id} deleted successfully by {current_user}"}

if __name__ == "__main__":
    app.run()
