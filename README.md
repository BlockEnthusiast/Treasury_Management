https://hackersandslackers.com/flask-assets/

# set up db
```bash
>>> sudo -i -u postgres
# sudo -i -u postgres
CREATE USER <DAT USER Name> WITH PASSWORD 'password';
CREATE DATABASE piedao_treasury WITH OWNER treasury ENCODING 'utf-8';
```

# Objectives
The goal hear is sorta to make a single use application for weaving all the python tooling I can find together.

Ideally with all this tooling, data collection, aggregation, and such modularized, it will be easy to add new features

I would like to see this evolve into the foundation for strong modeling of on and off chain data.

## To Do
* Sign in with Metamask (eventually but def on it)
* everything


# Structure

## Base
* wsgi.py
> Run this file to run locally
Port is set here

## /app

### Authentication
* Home
> Landing page

* Users
> Governs users
At present governs user owned simulations.
This will likely be consolidated into simulations

* Auth
> Governs Authentication.
Very lax. No email or anything.

### Environment
* Simulator
> Each simulation is linked to a user an owns mechanisms.
Functions can be added to trigger mechanisms into changing their state.

### Functions
* Market
* PieDAO
> to do

### Interpreters
* Plotly (Matplotlib)
> This enables Matplotlib to be used without any Javascript (at present effectively js free on the site.)
Though I do hope to enrich this section of the application, perhaps with it own richer JS powered display layer.

### Mechanisms
* AMM
> Govern the proceduer for shiting balances in an AMM.

  * AMM Records
  > Record the transition of state history for later assessment.
  These can be reset to rerun the simulation.
  Though note, each AMM records a record after initialization and reverts to those prices resets
  Ideally this gets better connected to oracles, and improved into a node tree for easier deviation
  of state change metrics.

### Oracles
  * External
    * API
    > At present, this is a singularized API manager for all API, but ideally the folder itself becomes that.
    Covers some Etherscan, Coingecko, and Liquidityfolio calls.
    Can add a module in #authentication for managing api keys?

  * Liquidityfolio
  > Due to the rich and relevant data, breaking out Liquidityfolio to seed the first self standing Oracle module.
  Pulling tokens, lps, contract addresses should make it easy to get the specific reference data we need to direct other oracles for further clarification.

### Static


### templates
> Global templates like layout and navigation live here.
