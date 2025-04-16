import pandas as pd

# Load the uploaded CSV file
file_path = "/mnt/data/Valve_Player_Data.csv"
df = pd.read_csv("C:/Users/eirc/Desktop/9014/9014project/Valve_Player_Data.csv")

# Display the first few rows and column info to understand the structure
df_head = df.head()
df_info = df.dtypes

df_head, df_info

df = pd.read_csv("C:/Users/eirc/Desktop/9014/9014project/Valve_Player_Data.csv")
