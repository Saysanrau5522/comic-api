 # Main FastAPI app with all routes
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
from models import Comic

# Initialize app and database
app = FastAPI()
Base.metadata.create_all(bind=engine)

# Comic Input Model
class ComicRequest(BaseModel):
    topic: str
    characters: list[str] = []  # Optional list of custom characters
    premium: bool = False       # Premium user flag for detailed comics

# Comic Output Model
class ComicResponse(BaseModel):
    id: int
    topic: str
    panels: list[dict]

# Root route
@app.get("/")
def root():
    return {"message": "Welcome to the Comic Generation API!"}

# Generate Comic
@app.post("/comics/", response_model=ComicResponse)
def create_comic(comic_req: ComicRequest):
    # Generate panels (simplified example)
    panels = []
    for i in range(1, 6 if not comic_req.premium else 11):
        panels.append({
            "panel_number": i,
            "text": f"This is panel {i} of the comic about {comic_req.topic}.",
            "image_placeholder": f"image_panel_{i}.png"
        })

    # Save to database
    with Session(engine) as session:
        new_comic = Comic(topic=comic_req.topic, panels=panels)
        session.add(new_comic)
        session.commit()
        session.refresh(new_comic)

    return {"id": new_comic.id, "topic": comic_req.topic, "panels": panels}

# Retrieve Comic by ID
@app.get("/comics/{comic_id}", response_model=ComicResponse)
def get_comic(comic_id: int):
    with Session(engine) as session:
        comic = session.get(Comic, comic_id)
        if not comic:
            raise HTTPException(status_code=404, detail="Comic not found")

    return {"id": comic.id, "topic": comic.topic, "panels": comic.panels}