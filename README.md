# Traffic Data Analytics - Data Warehouse

## Table of Contents

- [Traffic Data Analytics Data Warehouse](#traffic-data-analytics-data-warehouse)
  - [Overview](#overview)
  - [Features](#Features)
  - [Getting Started](#Getting_Started)
  - [Prerequisites](#Prerequisites)
  - [Installation](#installation)
  - [Getting Started](#getting-started)
  - [Data Sources](#data-sources)
  - [Data Generation](#data-generation)
  - [Screenshots](#screenshots)
  - [Contributions](#contributions)
  - [License](#license)

## Overview

This project involves launching an AI startup that deploys sensors in business environments to collect and analyze data. This data helps organization gain insights from activities such as people’s interactions and traffic flows. The current focus is on aiding a city traffic department to improve traffic management using data from drones. The challenge includes building a scalable data warehouse using technologies PostgreSQL, DBT, Airflow, and Redash, employing an ELT framework to ensure efficient data querying for future projects.

### Features
- Data Collection: Integration with swarm UAVs and static cameras to collect real-time traffic data.
- Data Warehouse: Scalable storage in PostgreSQL, designed to support high-volume data from diverse sources.
- Data Transformation: Utilizing DBT to implement ELT processes for efficient data transformation directly within the data warehouse.
- Data Visualization: Dashboards in Redash providing actionable insights into traffic patterns and management.

## Getting Started

Explore the repository to understand the project structure and components. Refer to the [Installation](#installation) section for setup instructions. Detailed documentation for each component is available within their respective folders.

#### Prerequisites
- Docker
- Git
- PostgreSQL
- Apache Airflow
- DBT
- Redash

## Installation

1. **Clone this Repository:**

    Clone this repository:
    ```bash 
    git clone https://github.com/dev-abuke/DataWarehouseTrafficDataAnalytics.git
    ```

    Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. **Set Up Python Environment:**

    ```bash
    python -m venv your_env_name
    ```

    Replace `your_env_name` with the desired name for your environment.
    
    **Activate the Environment:**

    - On Windows:

    ```bash
    .\your_env_name\scripts\activate
    ```

    - On macOS/Linux:

    ```bash
    source your_env_name/bin/activate
    ```

## Data Sources

The project relies on data from the following sources:

- [Download Site](https://open-traffic.epfl.ch/index.php/downloads/#1599047632450-ebe509c8-1330)
- [Records](https://zenodo.org/records/7426506)

## Data Generation

Understand how the data is generated:

- [PIA15 Poster (datafromsky.com)](https://datafromsky.com/wp-content/uploads/2015/03/PIA15_poster.pdf)
- [(PDF) Automatic Vehicle Trajectory Extraction (researchgate.net)](https://www.researchgate.net/publication/276857533_Automatic_vehicle_trajectory_extraction_for_traffic_analysis_from_aerial_video_data)

## Screenshots

Navigate to the `screenshots` folder to view visual representations of the project.

## Contributions

We welcome contributions to this repository. Please submit pull requests with improvements to code, documentation, or visualizations. Refer to the [Contribution Guidelines](CONTRIBUTING.md) for details.

## License

This repository is licensed under the [MIT License](LICENSE).
