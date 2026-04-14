# E-Commerce / Dog Survey Data Reengineering Pipeline

## Overview

This project is a structured data cleaning and reengineering pipeline built using Python.  
It processes a raw dog survey dataset and applies systematic data quality improvements across multiple dimensions:

- Data profiling
- Missing value handling (completeness)
- Data standardisation (consistency)
- Duplicate detection and removal

Each module is designed to be independently testable and reproducible.

---

## Dataset Source

This project uses a publicly available dataset:

- **Dog Survey Dataset (Dirty Data Project)**  
- Source: https://github.com/alasdairgm/dirty_data_project  
- File used: `task6/raw_data/dog_survey.csv`

### License

This dataset is distributed under the **MIT License**:

MIT License

Copyright (c) 2023 alasdairgm

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.

---

## Project Structure
```bash
📦 ecommerce-data-reengineering
┣ 📂 data
┃ ┣ 📂 raw
┃ ┃ ┗ dog_survey.csv
┃ ┣ 📂 processed
┃ ┃ ┣ dog_survey_cleaned.csv
┃ ┃ ┣ completeness_dog_survey_cleaned.csv
┃ ┃ ┣ consistency_dog_survey_cleaned.csv
┃ ┃ ┗ duplicates_dog_survey_cleaned.csv
┣ 📂 src
┃ ┣ 📂 scripts
┃ ┃ ┣ profiling.py
┃ ┃ ┣ completeness.py
┃ ┃ ┣ consistency.py
┃ ┃ ┗ duplicates.py
┃ ┣ 📂 notebooks
┃ ┃ ┣ data_cleansing_demo.ipynb
┃ ┃ ┣ completeness_cleansing.ipynb
┃ ┃ ┣ consistency_cleansing.ipynb
┃ ┃ ┗ duplicates_cleansing.ipynb
┣ main.py
┣ requirements.txt
┣ README.md
```

---

## Features

### 1. Data Profiling
- Dataset overview
- Missing value detection
- Initial quality analysis

### 2. Completeness Cleaning
- Handles missing/null values
- Standardises missing representations

### 3. Consistency Cleaning
- Fixes inconsistent formatting
- Standardises categorical values (e.g. gender, size, email)

### 4. Duplicate Removal
- Detects duplicate records
- Removes redundant entries

---

## Setup Guide

### 1. Clone the repository

```bash
git clone https://github.com/KurenoChan/ecommerce-data-reengineering
cd ecommerce-data-reengineering
```
---

### 2. Create virtual environment (.venv)

```bash
python -m venv .venv
```
---

### 3. Activate virtual environment
#### Windows (PowerShell)

```bash
.venv\Scripts\Activate
```

#### Windows (CMD)
```bash
.venv\Scripts\activate.bat
```

You should see: `(.venv)`

---

### 4. Upgrade pip (recommended)
```bash
python -m pip install --upgrade pip
```

---

### 5. Install dependencies (requirements.txt)
```bash
python -m pip install -r requirements.txt
```
This installs all required Python packages for the project.

---

## Output Files

All processed datasets are saved in: ``data/processed/``

Each file corresponds to a specific stage of cleaning:
- completeness cleaning output
- consistency cleaned output
- duplicate-free dataset
- final cleaned dataset

---
