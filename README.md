# Siralim Ultimate API

## About

This project is a JSON API for Game data from [Siralim Ultimate](https://store.steampowered.com/app/1289810/Siralim_Ultimate/) by [Thylacine Studios](http://www.thylacinestudios.com/).

It is written in [Python](https://www.python.org/) using [FastAPI](https://fastapi.tiangolo.com/).

[Live Swagger Doc](https://siralim-ultimate.rovermicrover.com/api/docs)

[Live Redoc](https://siralim-ultimate.rovermicrover.com/api/redoc)

## How To Dev

See [rovermicrover/siralim-ultimate-dev](https://github.com/rovermicrover/siralim-ultimate-dev) which allows for easy deving via docker-compose all of parts of this projet.

Also runs everything almost just like in production, even with NGINX, so no "It worked on my box" type issues.

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