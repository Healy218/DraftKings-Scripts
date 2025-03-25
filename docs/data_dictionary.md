# Data Dictionary

## File Naming Convention

Files in this project follow this naming pattern:
`{sport}_{season}_{type}_{date}_{version}.csv`

Example: `nba_2024-25_game_20240203_v1.csv`

## Data Types

### Game Data Files

#### NBA Game Files

- **Format**: CSV
- **Location**: `data/raw/nba/`
- **Columns**:
  - `player_name`: Player's full name
  - `position`: Player's position
  - `salary`: DraftKings salary
  - `team`: Player's team
  - `opponent`: Opposing team
  - `game_date`: Date of the game
  - `projected_points`: Projected fantasy points
  - [Add other columns as needed]

#### NFL Game Files

- **Format**: CSV
- **Location**: `data/raw/nfl/`
- **Columns**:
  - `player_name`: Player's full name
  - `position`: Player's position
  - `salary`: DraftKings salary
  - `team`: Player's team
  - `opponent`: Opposing team
  - `game_date`: Date of the game
  - `projected_points`: Projected fantasy points
  - [Add other columns as needed]

### Processed Data

#### Player Statistics

- **Format**: CSV
- **Location**: `data/processed/{sport}/`
- **Description**: Cleaned and aggregated player statistics
- **Columns**: [Add specific columns]

#### Model Outputs

- **Format**: CSV
- **Location**: `data/models/`
- **Description**: Results from optimization models
- **Columns**: [Add specific columns]

## Update Frequency

- Raw game data: Updated daily
- Processed statistics: Updated after each game day
- Model outputs: Generated on-demand

## Data Sources

- DraftKings API
- ESPN Stats
- Yahoo Sports
- [Add other sources]

## Notes

- All dates are in YYYY-MM-DD format
- All times are in EST/EDT
- Missing values are represented as NA
- [Add other important notes]
