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
git clone 
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