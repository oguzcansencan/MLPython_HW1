import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import MinMaxScaler
from fpdf import FPDF

matplotlib.use('TkAgg')

#def readFromCSV(filename):
#    return pd.read_csv("resources/" + filename + ".csv")
#file_constructors = readFromCSV("constructors")

def to_pdf(title, data, filename):
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

file_constructors = pd.read_csv("resources/constructors.csv")
file_drivers = pd.read_csv("resources/drivers.csv")
file_driverStandings = pd.read_csv("resources/driver_standings.csv")
file_lapTimes = pd.read_csv("resources/lap_times.csv")
file_pitStops = pd.read_csv("resources/pit_stops.csv")
file_races = pd.read_csv("resources/races.csv")
file_results = pd.read_csv("resources/results.csv")
file_sprintResults = pd.read_csv("resources/sprint_results.csv")

#
file_constructors.to_xml("outputs/raw/constructors.xml")
file_drivers.to_xml("outputs/raw/drivers.xml")
file_driverStandings.to_xml("outputs/raw/driver_standings.xml")
file_lapTimes.to_xml("outputs/raw/lap_times.xml")
file_pitStops.to_xml("outputs/raw/pit_stops.xml")
file_races.to_xml("outputs/raw/races.xml")
file_results.to_xml("outputs/raw/results.xml")
file_sprintResults.to_xml("outputs/raw/sprint_results.xml")

#
file_constructors.to_json("outputs/raw/constructors.json")
file_drivers.to_json("outputs/raw/drivers.json")
file_driverStandings.to_json("outputs/raw/driver_standings.json")
file_lapTimes.to_json("outputs/raw/lap_times.json")
file_pitStops.to_json("outputs/raw/pit_stops.json")
file_races.to_json("outputs/raw/races.json")
file_results.to_json("outputs/raw/results.json")
file_sprintResults.to_json("outputs/raw/sprint_results.json")

#
data_constructors = pd.read_json("outputs/raw/constructors.json")
data_drivers = pd.read_json("outputs/raw/drivers.json")
data_driverStandings = pd.read_json("outputs/raw/driver_standings.json")
data_lapTimes = pd.read_json("outputs/raw/lap_times.json")
data_pitStops = pd.read_json("outputs/raw/pit_stops.json")
data_races = pd.read_json("outputs/raw/races.json", convert_dates=False)
data_results = pd.read_json("outputs/raw/results.json")
data_sprintResults = pd.read_json("outputs/raw/sprint_results.json")

#
data_constructors = data_constructors.replace("\\N", None)
data_drivers = data_drivers.replace("\\N", None)
data_driverStandings = data_driverStandings.replace("\\N", None)
data_lapTimes = data_lapTimes.replace("\\N", None)
data_pitStops = data_pitStops.replace("\\N", None)
data_races = data_races.replace("\\N", None)
data_results = data_results.replace("\\N", None)
data_sprintResults = data_sprintResults.replace("\\N", None)

#
data_constructors.isnull().sum()
data_drivers.isnull().sum()
data_driverStandings.isnull().sum()
data_lapTimes.isnull().sum()
data_pitStops.isnull().sum()
data_races.isnull().sum()
data_results.isnull().sum()
data_sprintResults.isnull().sum()

#
# laptimes milliseconds (lap times per year for each constructors)
# pitstop milliseconds (pit stopes per year for each constructors)

scaler = MinMaxScaler()

data_lapTimes["milliseconds_scaled"] = scaler.fit_transform(np.asarray(data_lapTimes['milliseconds']).reshape(-1,1))
data_pitStops["milliseconds_scaled"] = scaler.fit_transform(np.asarray(data_pitStops['milliseconds']).reshape(-1,1))

#
data_constructors.to_xml("outputs/pre-processed/constructors.xml")
data_drivers.to_xml("outputs/pre-processed/drivers.xml")
data_driverStandings.to_xml("outputs/pre-processed/driver_standings.xml")
data_lapTimes.to_xml("outputs/pre-processed/lap_times.xml")
data_pitStops.to_xml("outputs/pre-processed/pit_stops.xml")
data_races.to_xml("outputs/pre-processed/races.xml")
data_results.to_xml("outputs/pre-processed/results.xml")
data_sprintResults.to_xml("outputs/pre-processed/sprint_results.xml")

#
data_constructors.to_json("outputs/pre-processed/constructors.json")
data_drivers.to_json("outputs/pre-processed/drivers.json")
data_driverStandings.to_json("outputs/pre-processed/driver_standings.json")
data_lapTimes.to_json("outputs/pre-processed/lap_times.json")
data_pitStops.to_json("outputs/pre-processed/pit_stops.json")
data_races.to_json("outputs/pre-processed/races.json")
data_results.to_json("outputs/pre-processed/results.json")
data_sprintResults.to_json("outputs/pre-processed/sprint_results.json")

pt1_lapTimes = data_lapTimes.loc[:, ['raceId', 'driverId', 'milliseconds']].merge(data_races.loc[:, ['raceId', 'year']], how='left', on='raceId')
pt4_lapTimes = pt1_lapTimes.groupby(['year'])['year', 'milliseconds'].mean()
pt1_lapTimes = pt1_lapTimes.groupby(['driverId', 'year'])['driverId', 'year', 'milliseconds'].mean()
pt1_lapTimes.index = pd.RangeIndex(len(pt1_lapTimes.index))

# Total PitStop Time and count for each constructor in each year
pt2_pitStops = data_pitStops.loc[:, ['raceId', 'driverId', 'milliseconds']].merge(data_results.loc[:, ['raceId', 'driverId', 'constructorId']], how='left', on=('raceId', 'driverId'))
pt2_pitStops = pt2_pitStops.merge(data_races.loc[:, ['raceId', 'year']], on='raceId', how='left')
pt2_pitStops = pt2_pitStops.groupby(['constructorId', 'year'])['constructorId', 'year', 'milliseconds'].agg(['mean', 'count', 'sum'])
pt2_pitStops = pt2_pitStops.iloc[:, [0, 3, 7, 8]]
pt2_pitStops.index = pd.RangeIndex(len(pt2_pitStops.index))
pt2_pitStops.columns = ['constructorId', 'year', 'pitCounts', 'totalPitTime']
pt2_pitStops = pt2_pitStops.merge(data_constructors.loc[:, ['constructorId', 'constructorRef']], how='left', on='constructorId')

# All the stats for each driver in each race
# - Lap Count
# - Average Lap Time
# - Total Lap Time
# - Points
# - Average Pit Stop Time
# - Total Pit Stop Time
# - Year
pt3_stats = data_lapTimes.groupby(['raceId', 'driverId'])['raceId', 'driverId', 'milliseconds'].agg(['count', 'mean', 'sum'])
pt3_stats.index = pd.RangeIndex(len(pt3_stats.index))
pt3_stats = pt3_stats.iloc[:, [1, 4, 6, 7, 8]]
pt3_stats.columns = ['raceId', 'driverId', 'lapCounts', 'avgLapTime', 'totalLapTime']

temp_results = data_results.loc[:, ['raceId', 'driverId', 'points']]
temp_sprintResult = data_sprintResults.loc[:, ['raceId', 'driverId', 'points']]
temp_sprintResult.columns = ['raceId', 'driverId', 'sprintPoints']
temp_results = temp_results.merge(temp_sprintResult, on=('raceId', 'driverId'), how='left')
temp_results = temp_results.fillna(0)
temp_results['points'] = temp_results['points'] + temp_results['sprintPoints']

pt3_stats = pt3_stats.merge(temp_results.loc[:, ['raceId', 'driverId', 'points']], on=('raceId', 'driverId'), how='left')

temp_pitStops = data_pitStops.groupby(['raceId', 'driverId'])['raceId', 'driverId', 'milliseconds'].agg(['count', 'mean', 'sum'])
temp_pitStops.index = pd.RangeIndex(len(temp_pitStops.index))
temp_pitStops = temp_pitStops.iloc[:, [1, 4, 6, 7, 8]]
temp_pitStops.columns = ['raceId', 'driverId', 'pitCounts', 'avgPitTime', 'totalPitTime']
pt3_stats = pt3_stats.merge(temp_pitStops, on=('raceId', 'driverId'), how='left')

pt3_stats = pt3_stats.fillna(0)

pt3_stats = pt3_stats.merge(data_races.loc[:, ['raceId', 'year', 'circuitId', 'name']], on='raceId', how='left')
pt3_stats = pt3_stats.merge(data_drivers.loc[:, ['driverId', 'forename', 'surname']], on='driverId', how='left')

pd.set_option('display.expand_frame_repr', False)

#
pt1_lapTimes.to_xml("outputs/tables/pt1_lapTimes.xml")
pt2_pitStops.to_xml("outputs/tables/pt2_pitStops.xml")
pt3_stats.to_xml("outputs/tables/pt3_stats.xml")


pt3_stats.iloc[:, 2:10].describe().to_csv('outputs/analysis/descriptive_statistics.txt', sep=',', float_format='%.3f')
pt3_stats.iloc[:, 2:10].corr().to_csv('outputs/analysis/correlation_analysis.txt', sep=',', float_format='%.3f')

to_pdf("Correlation Analysis", pt3_stats.iloc[:, 2:10].corr(), "correlation_analysis")
to_pdf("Descriptive Statistics", pt3_stats.iloc[:, 2:9].describe(), "descriptive_statistics")


temp = pt3_stats.groupby(['raceId'])['raceId', 'pitCounts'].agg(['mean', 'sum'])
temp = temp.iloc[:, [0, 3]]
temp.columns = ['raceId', 'pitCounts']
temp.index = pd.RangeIndex(len(temp.index))
fig1, ax1 = plt.subplots()
ax1.bar(pt4_lapTimes.year, pt4_lapTimes.milliseconds)
ax1.set_xlabel('Years')
ax1.set_ylabel('Lap Times in Milliseconds')
ax1.set_title('Bar Chart')

fig2, ax2 = plt.subplots()
ax2.hist(temp.pitCounts, bins=30, color='green', alpha=0.5)
ax2.set_xlabel('Number of Pit Stops in Races')
ax2.set_ylabel('Frequency')
ax2.set_title('Histogram')

fig3 = plt.figure()
ax3 = fig3.add_subplot(111, projection='3d')
ax3.scatter(pt2_pitStops.constructorId, pt2_pitStops.year, pt2_pitStops.pitCounts, c=pt2_pitStops.pitCounts, cmap='coolwarm')
ax3.set_xlabel('Constructor IDs')
ax3.set_ylabel('Years')
ax3.set_zlabel('Pit Counts')
ax3.set_title('Scatter Plot')

# Show both plots
plt.show()