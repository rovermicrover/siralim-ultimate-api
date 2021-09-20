# Siralim Ultimate API

## About

This project is a JSON API for Game data from Siralim Ultimate.

It is written in [Python](https://www.python.org/) using [FastAPI](https://fastapi.tiangolo.com/).

[Live Swagger Doc](https://siralim-ultimate.rovermicrover.com/api/docs)
[Live Redoc](https://siralim-ultimate.rovermicrover.com/api/redoc)

## How To Dev

### Requirements

1. Bash

2. git

3. Docker Compose

### Walk Through To Get Dev ENV Started

Run

```bash
$ commands/dev-bootstrap
```

All app files are synced via docker-compose so you can just start deving and changes will show up automatically 

[The app can then be accessed here](http://localhost/api/)

[API End Points Swagger here](http://localhost/api/docs)

[API End Points Redoc here](http://localhost/api/redoc)

## How to Test

### Requirements

1. Bash

2. Docker Compose

### Walk Through To Get Test To Run

Run

```bash
$ commands/test
```

## TODO

### Data

* Race Icons

* Spell Animations

* Creature Overworld Sprites Sprites

* Creature Attack Animations

* Specializations and Perks, including Icons

* Skins including Battle and Overworld Sprites

* Wardrobe including Overworld Sprites

* Spell Gem Properties

* Realm Properties

* Cleanup sources

### Tests

* More creature router tests