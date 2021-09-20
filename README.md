# Siralim Ultimate API

## About

This project is a JSON API for Game data from Siralim Ultimate.

It is written in Python using FastAPI.

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

App can be accessed via http://localhost/api/creatures/

API End Points Swagger can be found at http://localhost/api/docs

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

### Github Actions

* Docker

### Docker

* Build Docker Image With Github Actions

### Routers

* Cache headers

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

### Terraform

* Build Example Terraform to build infrastruture that can be commited with zero secrets.