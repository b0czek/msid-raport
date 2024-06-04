import pandas as pd
from ydata_profiling import ProfileReport

df = pd.read_csv('data.csv')

profile = ProfileReport(df, title="Pandas Profiling Report", explorative=True)

profile.to_notebook_iframe()

profile.to_file("report.html")

