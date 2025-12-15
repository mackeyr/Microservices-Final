from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from .stats_middleware import StatsMiddleware
from .routers import facts, admin, auth, live
import random
from . import crud, schemas
from sqlalchemy.orm import Session
from .database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(StatsMiddleware)

app.include_router(facts.router)
app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(live.router)

@app.on_event("startup")
def startup_event():
    db = next(get_db())
    insert_default_facts(db)


DEFAULT_FACTS = [
    "Bananas are berries, but strawberries are not!",
    "Butterflies can taste with their feet.",
    "Octopuses have three hearts.",
    "Honey never spoils.",
    "Sharks existed before trees.",
    "A group of flamingos is called a 'flamboyance'.",
    "Sloths can hold their breath longer than dolphins.",
    "Wombat poop is cube-shaped.",
    "There’s a species of jellyfish that is immortal.",
    "Some turtles can breathe through their butts.",
    "Cows have best friends and can get stressed when separated.",
    "Sea otters hold hands while sleeping to stay together.",
    "You can’t burp in space due to lack of gravity.",
    "Pineapples take about two years to grow.",
    "Humans and giraffes have the same number of neck vertebrae.",
    "A day on Venus is longer than a year on Venus.",
    "Sharks can live up to 500 years in some cases.",
    "Sloths can rotate their heads almost 360 degrees.",
    "Wombats can run up to 40 km/h for short distances.",
    "An ostrich’s eye is bigger than its brain.",
    "Butterflies can see red, green, and yellow, but not blue.",
    "A newborn kangaroo is smaller than a cherry.",
    "The Eiffel Tower can be 15 cm taller during the summer.",
    "The unicorn is Scotland’s national animal.",
    "The longest hiccuping spree lasted 68 years.",
    "There’s a species of frog that can freeze completely and survive.",
    "Octopuses have blue blood due to copper in it.",
    "Crows can recognize human faces and remember them for years.",
    "The Great Wall of China is not visible from space with the naked eye.",
    "Sea cucumbers fight off predators by shooting out their own internal organs.",
    "Sloths can swim three times faster than they can walk.",
    "A shrimp’s heart is located in its head.",
    "A day on Saturn lasts about 10 hours and 33 minutes.",
    "Koalas have fingerprints almost identical to humans.",
    "Some bamboo species can grow almost a meter in a single day.",
    "There’s a species of mushroom that glows in the dark.",
    "Turtles can live without food for more than a year by slowing metabolism.",
    "Penguins propose to their mates with pebbles.",
    "A sneeze can travel up to 100 miles per hour.",
    "Owls can rotate their heads up to 270 degrees.",
    "Slugs have four noses.",
    "Dolphins have been observed teaching each other tricks.",
    "The world’s oldest known living tree is over 5,000 years old.",
    "Cats can make over 100 different sounds.",
    "Elephants can communicate using infrasound, below human hearing.",
    "Sharks existed before trees.",
    "Butterflies taste with their feet.",
    "There’s a species of lizard that can squirt blood from its eyes.",
    "A day on Mercury lasts 59 Earth days.",
    "Some birds can sleep while flying.",
    "The honeybee has been around for more than 30 million years.",
]


def insert_default_facts(db: Session):
    if db.query(crud.models.Fact).count() == 0:
        for text in DEFAULT_FACTS:
            fact = schemas.FactCreate(text=text)
            crud.create_fact(db, fact)


@app.get("/", response_class=HTMLResponse)
def root():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Random Fun Fact</title>
<style>
  body {
    font-family: Arial, sans-serif;
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    transition: background-color 0.5s;
  }
  #fact-box {
    padding: 2rem;
    border-radius: 15px;
    text-align: center;
    font-size: 1.5rem;
    max-width: 600px;
  }
  button {
    margin-top: 1rem;
    padding: 0.5rem 1rem;
    font-size: 1rem;
    cursor: pointer;
  }
</style>
</head>
<body>
<div id="fact-box">
  Loading fact...
  <button onclick="getFact()">New Fact</button>
</div>

<script>
function randomColor() {
    return '#' + Math.floor(Math.random()*16777215).toString(16);
}

// SSE connection for live updates
const evtSource = new EventSource("/live/facts/stream");

evtSource.onmessage = function(event) {
    const data = JSON.parse(event.data);
    const box = document.getElementById('fact-box');
    box.innerHTML = `<p>${data.text}</p><button onclick="getFact()">New Fact</button>`;
    document.body.style.backgroundColor = randomColor();
};

evtSource.onerror = function(err) {
    console.error("SSE connection error:", err);
    // Optionally close or reconnect here
};

// Fallback button for manual fetch
async function getFact() {
    const response = await fetch('/facts/random'); // add headers if your API key is needed
    const data = await response.json();
    const box = document.getElementById('fact-box');
    box.innerHTML = `<p>${data.text}</p><button onclick="getFact()">New Fact</button>`;
    document.body.style.backgroundColor = randomColor();
}
</script>
</body>
</html>
"""
