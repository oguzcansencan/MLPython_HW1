import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from fpdf import FPDF

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

# race-based average lap times for each driver
pt1_lapTimes = data_lapTimes.groupby(['raceId', 'driverId'])['raceId', 'driverId', 'milliseconds'].mean()
pt1_lapTimes.index = pd.RangeIndex(len(pt1_lapTimes.index))
pt1_lapTimes = pt1_lapTimes.merge(data_races, left_on='raceId', right_on='raceId').loc[:, ['raceId', 'driverId', 'milliseconds', 'year']]
# yearly average lap times for each driver
pt2_lapTimes = pt1_lapTimes.groupby(['driverId', 'year'])['driverId', 'year', 'milliseconds'].agg(['count', 'mean'])
pt2_lapTimes.index = pd.RangeIndex(len(pt2_lapTimes.index))
pt2_lapTimes = pt2_lapTimes.iloc[:, [1, 3, 4, 5]]
pt2_lapTimes.columns = ['driverId', 'year', 'count', 'milliseconds']

# Total PitStop Time and Count for each driver in each race
pt3_pitStops = data_pitStops.groupby(['raceId', 'driverId'])['raceId', 'driverId', 'milliseconds'].agg(['sum', 'count', 'mean'])
pt3_pitStops.index = pd.RangeIndex(len(pt3_pitStops.index))
pt3_pitStops = pt3_pitStops.iloc[:, [2, 5, 6, 7]]
pt3_pitStops.columns = ['raceId', 'driverId', 'sum', 'count']
# Total PitStop Time and count for each constructor in each year
pt4_pitStops = pt3_pitStops.merge(data_results.loc[:, ['raceId', 'driverId', 'constructorId']], left_on=('raceId', 'driverId'), right_on=('raceId', 'driverId'))
pt4_pitStops = pt4_pitStops.merge(data_races.loc[:, ['raceId', 'year']], left_on='raceId', right_on='raceId')
pt4_pitStops = pt4_pitStops.groupby(['constructorId', 'year'])['constructorId', 'year', 'sum', 'count'].agg(['sum', 'mean'])
pt4_pitStops.index = pd.RangeIndex(len(pt4_pitStops.index))
pt4_pitStops = pt4_pitStops.iloc[:, [1, 3, 4, 6]]
pt4_pitStops.columns = ['constructorId', 'year', 'sum', 'count']
pt4_pitStops = pt4_pitStops.merge(data_constructors.loc[:, ['constructorId', 'constructorRef']], left_on='constructorId', right_on='constructorId')

# All the stats for each driver in each race
# - Lap Count
# - Average Lap Time
# - Total Lap Time
# - Points
# - Average Pit Stop Time
# - Total Pit Stop Time
# - Year
pt5_stats = data_lapTimes.groupby(['raceId', 'driverId'])['raceId', 'driverId', 'milliseconds'].agg(['count', 'mean', 'sum'])
pt5_stats.index = pd.RangeIndex(len(pt5_stats.index))
pt5_stats = pt5_stats.iloc[:, [1, 4, 6, 7, 8]]
pt5_stats.columns = ['raceId', 'driverId', 'lapCounts', 'avgLapTime', 'totalLapTime']

temp_results = data_results.loc[:, ['raceId', 'driverId', 'points']]
temp_sprintResult = data_sprintResults.loc[:, ['raceId', 'driverId', 'points']]
temp_sprintResult.columns = ['raceId', 'driverId', 'sprintPoints']
temp_results = temp_results.merge(temp_sprintResult, on=('raceId', 'driverId'), how='left')
temp_results = temp_results.fillna(0)
temp_results['points'] = temp_results['points'] + temp_results['sprintPoints']

pt5_stats = pt5_stats.merge(temp_results.loc[:, ['raceId', 'driverId', 'points']], on=('raceId', 'driverId'), how='left')

temp_pitStops = data_pitStops.groupby(['raceId', 'driverId'])['raceId', 'driverId', 'milliseconds'].agg(['count', 'mean', 'sum'])
temp_pitStops.index = pd.RangeIndex(len(temp_pitStops.index))
temp_pitStops = temp_pitStops.iloc[:, [1, 4, 6, 7, 8]]
temp_pitStops.columns = ['raceId', 'driverId', 'pitCounts', 'avgPitTime', 'totalPitTime']
pt5_stats = pt5_stats.merge(temp_pitStops, on=('raceId', 'driverId'), how='left')

pt5_stats = pt5_stats.fillna(0)

pt5_stats = pt5_stats.merge(data_races.loc[:, ['raceId', 'year', 'circuitId', 'name']], on='raceId', how='left')
pt5_stats = pt5_stats.merge(data_drivers.loc[:, ['driverId', 'forename', 'surname']], on='driverId', how='left')

pd.set_option('display.expand_frame_repr', False)

#
pt1_lapTimes.to_xml("outputs/tables/pt1_lapTimes.xml")
pt2_lapTimes.to_xml("outputs/tables/pt2_lapTimes.xml")
pt3_pitStops.to_xml("outputs/tables/pt3_pitStops.xml")
pt4_pitStops.to_xml("outputs/tables/pt4_pitStops.xml")
pt5_stats.to_xml("outputs/tables/pt5_stats.xml")


pt5_stats.iloc[:, 2:10].describe().to_csv('outputs/analysis/descriptive_statistics.txt', sep=',', float_format='%.3f')
pt5_stats.iloc[:, 2:10].corr().to_csv('outputs/analysis/correlation_analysis.txt', sep=',', float_format='%.3f')

to_pdf("Correlation Analysis", pt5_stats.iloc[:, 2:10].corr(), "correlation_analysis")
to_pdf("Descriptive Statistics", pt5_stats.iloc[:, 2:9].describe(), "descriptive_statistics")