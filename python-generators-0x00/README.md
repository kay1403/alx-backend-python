#  Seed 

## Description

This script (`seed.py`) connects to a local MySQL server, creates a database named `ALX_prodev` if it does not exist, creates a table called `user_data`, and populates it with data from a `user_data.csv` file.

## Features

- Connects to MySQL server
- Creates the `ALX_prodev` database
- Creates the `user_data` table with the following schema:
  - `user_id` (UUID, primary key, indexed)
  - `name` (VARCHAR, not null)
  - `email` (VARCHAR, not null)
  - `age` (DECIMAL, not null)
- Loads and inserts data from a CSV file, ensuring no duplicates

## Files

- `seed.py`: Main script to seed the database
- `user_data.csv`: Source file containing user data

## Usage

```bash
python3 0-main.py
