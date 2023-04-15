import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import MinMaxScaler
from fpdf import FPDF

matplotlib.use('TkAgg')

class MyUtilities:
    def read_csv_multiple(self, list):
        for i in list:
            list[i] = pd.read_csv("resources/" + i + ".csv")
        return list
    def export_xml_multiple(self, list, directory):
        for i in list:
            list[i].to_xml("outputs/" + directory + "/" + i + ".xml")
    def export_json_multiple(self, list, directory):
        for i in list:
            list[i].to_json("outputs/" + directory + "/" + i + ".json")
    def fix_all(self, list):
        for i in list:
            list[i] = list[i].replace("\\N", None)
        return list
    def to_pdf(self, title, data, filename):
        pdf = FPDF()
        pdf.add_page(orientation="L")

        pdf.set_font("Arial", size=16)

        pdf.cell(200, 10, txt=title, ln=1, align="C")

        pdf.set_font("Arial", size=12)

        pdf.cell(30, 10, "", border=1)
        for index in data.columns:
            pdf.cell(30, 10, index, border=1)
        pdf.ln()

        for index, row in data.iterrows():
            pdf.cell(30, 10, str(index), border=1)
            for index2 in data.columns:
                pdf.cell(30, 10, '{:.3f}'.format(row[index2]), border=1)
            pdf.ln()

        pdf.output("outputs/analysis/" + filename + ".pdf")

myUtilities = MyUtilities()

data = {'constructors':0, 'drivers':0, 'lapTimes':0, 'pitStops':0, 'races':0, 'results':0, 'sprintResults':0}

data = myUtilities.read_csv_multiple(data)

myUtilities.export_xml_multiple(data, "raw")
myUtilities.export_json_multiple(data, "raw")

# Replacing "\\N" to None
data = myUtilities.fix_all(data)

scaler = MinMaxScaler()

data['lapTimes']["milliseconds_scaled"] = scaler.fit_transform(np.asarray(data['lapTimes']['milliseconds']).reshape(-1, 1))
data['pitStops']["milliseconds_scaled"] = scaler.fit_transform(np.asarray(data['pitStops']['milliseconds']).reshape(-1, 1))

myUtilities.export_xml_multiple(data, "pre-processed")
myUtilities.export_json_multiple(data, "pre-processed")

# DataFrame - df_lapTimes
# Average Lap Time of all races in a year(2011-2022) for each driver
df_lapTimes = data['lapTimes'].loc[:, ['raceId', 'driverId', 'milliseconds']].merge(data['races'].loc[:, ['raceId', 'year']], how='left', on='raceId')
df_lapTimesAvgByYear = df_lapTimes.groupby(['year'])['year', 'milliseconds'].mean()
df_lapTimes = df_lapTimes.groupby(['driverId', 'year'])['driverId', 'year', 'milliseconds'].mean()
df_lapTimes.index = pd.RangeIndex(len(df_lapTimes.index))
df_lapTimes = df_lapTimes.merge(data['drivers'].loc[:, ['driverId', 'forename', 'surname']], how='left', on='driverId')
df_lapTimes['driverName'] = df_lapTimes['forename'] + " " + df_lapTimes['surname']
pt_lapTimes = pd.pivot_table(df_lapTimes.loc[:, ['driverName', 'year', 'milliseconds']], values='milliseconds',index='driverName', columns='year', aggfunc='sum')

# DataFrame - df_pitStops
# Total PitStop Time and count for each constructor in each year
df_pitStops = data['pitStops'].loc[:, ['raceId', 'driverId', 'milliseconds']].merge(data['results'].loc[:, ['raceId', 'driverId', 'constructorId']], how='left', on=('raceId', 'driverId'))
df_pitStops = df_pitStops.merge(data['races'].loc[:, ['raceId', 'year']], on='raceId', how='left')
df_pitStops = df_pitStops.groupby(['constructorId', 'year'])['constructorId', 'year', 'milliseconds'].agg(['mean', 'count', 'sum'])
df_pitStops = df_pitStops.iloc[:, [0, 3, 7, 8]]
df_pitStops.index = pd.RangeIndex(len(df_pitStops.index))
df_pitStops.columns = ['constructorId', 'year', 'pitCounts', 'totalPitTime']
df_pitStops = df_pitStops.merge(data['constructors'].loc[:, ['constructorId', 'constructorRef']], how='left', on='constructorId')
pt_pitStops = pd.pivot_table(df_pitStops.loc[:, ['constructorRef', 'year', 'pitCounts']], index='year', columns='constructorRef', values='pitCounts')

# DataFrame - df_overallStats
# Overall stats for each driver in each race
# - Lap Count
# - Average Lap Time
# - Total Lap Time
# - Points
# - Pit Stop Counts
# - Average Pit Stop Time
# - Total Pit Stop Time
# - Year
df_overallStats = data['lapTimes'].groupby(['raceId', 'driverId'])['raceId', 'driverId', 'milliseconds'].agg(['count', 'mean', 'sum'])
df_overallStats.index = pd.RangeIndex(len(df_overallStats.index))
df_overallStats = df_overallStats.iloc[:, [1, 4, 6, 7, 8]]
df_overallStats.columns = ['raceId', 'driverId', 'lapCounts', 'avgLapTime', 'totalLapTime']

temp_results = data['results'].loc[:, ['raceId', 'driverId', 'points']]
temp_sprintResult = data['sprintResults'].loc[:, ['raceId', 'driverId', 'points']]
temp_sprintResult.columns = ['raceId', 'driverId', 'sprintPoints']
temp_results = temp_results.merge(temp_sprintResult, on=('raceId', 'driverId'), how='left')
temp_results = temp_results.fillna(0)
temp_results['points'] = temp_results['points'] + temp_results['sprintPoints']

df_overallStats = df_overallStats.merge(temp_results.loc[:, ['raceId', 'driverId', 'points']], on=('raceId', 'driverId'), how='left')

temp_pitStops = data['pitStops'].groupby(['raceId', 'driverId'])['raceId', 'driverId', 'milliseconds'].agg(['count', 'mean', 'sum'])
temp_pitStops.index = pd.RangeIndex(len(temp_pitStops.index))
temp_pitStops = temp_pitStops.iloc[:, [1, 4, 6, 7, 8]]
temp_pitStops.columns = ['raceId', 'driverId', 'pitCounts', 'avgPitTime', 'totalPitTime']
df_overallStats = df_overallStats.merge(temp_pitStops, on=('raceId', 'driverId'), how='left')

df_overallStats = df_overallStats.fillna(0)

df_overallStats = df_overallStats.merge(data['races'].loc[:, ['raceId', 'year', 'circuitId', 'name']], on='raceId', how='left')
df_overallStats = df_overallStats.rename(columns={'name': 'circuitName'})
df_overallStats = df_overallStats.merge(data['drivers'].loc[:, ['driverId', 'forename', 'surname']], on='driverId', how='left')
df_overallStats['driverName'] = df_overallStats['forename'] + " " + df_overallStats['surname']


# ------------ XML ------------
df_lapTimes.to_xml("outputs/tables/df_lapTimes.xml")
df_pitStops.to_xml("outputs/tables/df_pitStops.xml")
df_overallStats.to_xml("outputs/tables/df_overallStats.xml")


# --------- PDF / TXT ---------

# Descriptive Statistics
# PDF: analysis/descriptive_statistics.pdf
# TXT: outputs/analysis/descriptive_statistics.txt
myUtilities.to_pdf("Descriptive Statistics", df_overallStats.iloc[:, 2:9].describe(), "descriptive_statistics")
df_overallStats.iloc[:, 2:10].describe().to_csv('outputs/analysis/descriptive_statistics.txt', sep=',', float_format='%.3f')

# Correlation Analysis
# PDF: analysis/correlation_analysis.pdf
# TXT: outputs/analysis/descriptive_statistics.txt
myUtilities.to_pdf("Correlation Analysis", df_overallStats.iloc[:, 2:10].corr(), "correlation_analysis")
df_overallStats.iloc[:, 2:10].corr().to_csv('outputs/analysis/correlation_analysis.txt', sep=',', float_format='%.3f')


# ---------- CHARTS -----------

# Bar Chart - "visualization/Average_Lap_Times_For_Each_Year.png"
fig1, ax1 = plt.subplots()
ax1.bar(df_lapTimesAvgByYear.year, df_lapTimesAvgByYear.milliseconds)
ax1.set_xlabel('Years')
ax1.set_ylabel('Lap Times in Milliseconds')
ax1.set_title('Bar Chart')

# Histogram - "visualization/Number_of_Pit_Stops_in_Races.png"
temp = df_overallStats.groupby(['raceId'])['raceId', 'pitCounts'].agg(['mean', 'sum'])
temp = temp.iloc[:, [0, 3]]
temp.columns = ['raceId', 'pitCounts']
temp.index = pd.RangeIndex(len(temp.index))
fig2, ax2 = plt.subplots()
ax2.hist(temp.pitCounts, bins=30, color='green', alpha=0.5)
ax2.set_xlabel('Number of Pit Stops in Races')
ax2.set_ylabel('Frequency')
ax2.set_title('Histogram')

# 3D Scatter Plot - "visualization/Number_of_Pit_Stop_For_Each_Constructors.png"
fig3 = plt.figure()
ax3 = fig3.add_subplot(111, projection='3d')
ax3.scatter(df_pitStops.constructorId, df_pitStops.year, df_pitStops.pitCounts, c=df_pitStops.pitCounts, cmap='coolwarm')
ax3.set_xlabel('Constructor IDs')
ax3.set_ylabel('Years')
ax3.set_zlabel('Pit Counts')
ax3.set_title('Scatter Plot')

# Show all plots
plt.show()
