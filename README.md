# Eccom Analysis

This project provides a complete data analysis workflow for the Superstore sales dataset, including data cleaning, feature engineering, database storage, SQL-based analytics, visualization, and Tableau integration.

## Project Structure

- **data/raw/**: Contains the original raw data files (e.g., `Sample - Superstore.csv`).
- **data/proccesed/**: All processed outputs (analysis CSVs, images, Tableau-ready CSV) are saved here.
- **src/**: Python scripts for data cleaning, EDA, database loading, SQL queries, and Tableau export.
- **notebooks/**: Jupyter notebook for interactive EDA and visualization.

## Workflow

1. **Data Cleaning & Feature Engineering**
   - Standardizes column names, parses dates, and creates new features (e.g., shipping days, profit margin).
2. **Database Storage**
   - Loads cleaned data into a SQLite database for efficient querying.
3. **Analysis & Reporting**
   - Runs SQL queries to generate business insights (monthly trends, category breakdowns, regional performance, shipping analysis, top customers, discount impact).
   - Exports results as CSVs for further use (e.g., Tableau).
4. **Visualization**
   - EDA scripts and notebooks create summary plots, saved as images.
5. **Tableau Integration**
   - Exports a clean, analysis-ready CSV for direct Tableau connection.

## Getting Started

1. Clone the repository:
   ```
   git clone https://github.com/abhi-7-7/Eccom_Analysis.git
   cd Eccom_Analysis
   ```
2. Create and activate the conda environment:
   ```
   conda create -n eccom python=3.11
   conda activate eccom
   pip install -r requirements.txt
   ```
3. Run the scripts in order:
   ```
   python src/load_to_sqlite.py
   python src/sql_queries.py
   python src/eda.py
   python src/export_tableau.py
   ```
4. Open and explore the notebook in `notebooks/superstore_analysis.ipynb`.

## Outputs
- All processed CSVs and images are in `data/proccesed/`.
- Connect Tableau to `data/proccesed/superstore_tableau.csv` for dashboarding.

## License
MIT License
