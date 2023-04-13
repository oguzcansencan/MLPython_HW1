import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

#
file_constructors = pd.read_csv("resources/constructors.csv")
file_drivers = pd.read_csv("resources/drivers.csv")
file_driverStandings = pd.read_csv("resources/driver_standings.csv")
file_lapTimes = pd.read_csv("resources/lap_times.csv")
file_pitStops = pd.read_csv("resources/pit_stops.csv")
file_races = pd.read_csv("resources/races.csv")
file_results = pd.read_csv("resources/results.csv")

#
file_constructors.to_xml("outputs/raw/constructors.xml")
file_drivers.to_xml("outputs/raw/drivers.xml")
file_driverStandings.to_xml("outputs/raw/driver_standings.xml")
file_lapTimes.to_xml("outputs/raw/lap_times.xml")
file_pitStops.to_xml("outputs/raw/pit_stops.xml")
file_races.to_xml("outputs/raw/races.xml")
file_results.to_xml("outputs/raw/results.xml")

#
file_constructors.to_json("outputs/raw/constructors.json")
file_drivers.to_json("outputs/raw/drivers.json")
file_driverStandings.to_json("outputs/raw/driver_standings.json")
file_lapTimes.to_json("outputs/raw/lap_times.json")
file_pitStops.to_json("outputs/raw/pit_stops.json")
file_races.to_json("outputs/raw/races.json")
file_results.to_json("outputs/raw/results.json")

#
data_constructors = pd.read_json("outputs/raw/constructors.json")
data_drivers = pd.read_json("outputs/raw/drivers.json")
data_driverStandings = pd.read_json("outputs/raw/driver_standings.json")
data_lapTimes = pd.read_json("outputs/raw/lap_times.json")
data_pitStops = pd.read_json("outputs/raw/pit_stops.json")
data_races = pd.read_json("outputs/raw/races.json", convert_dates=False)
data_results = pd.read_json("outputs/raw/results.json")

#
data_constructors = data_constructors.replace("\\N", None)
data_drivers = data_drivers.replace("\\N", None)
data_driverStandings = data_driverStandings.replace("\\N", None)
data_lapTimes = data_lapTimes.replace("\\N", None)
data_pitStops = data_pitStops.replace("\\N", None)
data_races = data_races.replace("\\N", None)
data_results = data_results.replace("\\N", None)

#
data_constructors.isnull().sum()
data_drivers.isnull().sum()
data_driverStandings.isnull().sum()
data_lapTimes.isnull().sum()
data_pitStops.isnull().sum()
data_races.isnull().sum()
data_results.isnull().sum()

#
# pitstop milliseconds (pit stopes per year for each constructors)
# laptimes milliseconds (lap times per year for each constructors)

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

#
data_constructors.to_json("outputs/pre-processed/constructors.json")
data_drivers.to_json("outputs/pre-processed/drivers.json")
data_driverStandings.to_json("outputs/pre-processed/driver_standings.json")
data_lapTimes.to_json("outputs/pre-processed/lap_times.json")
data_pitStops.to_json("outputs/pre-processed/pit_stops.json")
data_races.to_json("outputs/pre-processed/races.json")
data_results.to_json("outputs/pre-processed/results.json")
