import pandas as pd


fileOutSpeed = open("speed.txt", "w")
fileOutAccel = open("accel.txt", "w")
gps_data = pd.read_csv('gps.csv')
gps_data.groupby(['GameID','PlayerID'])['Speed'].mean()
gps_data.groupby(['GameID','PlayerID'])['AccelImpulse'].mean()
gps_data.groupby(['GameID','PlayerID'])['Speed'].mean().to_csv(path_or_buf="avg speed.csv")
gps_data.groupby(['GameID','PlayerID'])['AccelImpulse'].mean().to_csv(path_or_buf="avg accel.csv")