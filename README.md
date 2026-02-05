## Live Demo
https://space-mission-dash.streamlit.app/

## Design and Usage

### Visuals Explanations
1. The first visual is a bar chart of the percentage success rate of each company, sorted from left to right in order of the companies with the most missions first. This is to demonstrate how successful a company is while also prioritizing companies with higher levels of activity.
2. The second visual is a line chart that plots both the amount of missions per year and the success rate for that year over the range of the earliest year in the data set to the latest. This is to show how the volume of missions and their overall success rate has changed as technology and strategies have evolved over time.
3. The last visual is a heatmap demonstrating the amount of certain types of failures or successes of each different rocket in the data set. This is to demonstrate the reliability of each rocket in a way that is visually intuitive.

### Usage Instructions
1. Install Python (I used version 3.12.6).
2. Clone the repo.
3. Create and activate your virtual environment using venv (these are Windows PowerShell oriented commands):
```
python -m venv .venv
.venv\Scripts\activate.ps1
```
4. Use pip to install the dependencies:
```
pip install -r requirements.txt
```
5. Run application:
```
streamlit run main.py
```
6. Navigate to http://localhost:8501/
