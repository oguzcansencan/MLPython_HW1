import pandas as pd

file_constructors = pd.read_csv("resources/constructors.csv")
file_drivers = pd.read_csv("resources/drivers.csv")
file_driverStandings = pd.read_csv("resources/driver_standings.csv")
file_lapTimes = pd.read_csv("resources/lap_times.csv")
file_races = pd.read_csv("resources/races.csv")
file_results = pd.read_csv("resources/results.csv")

file_constructors.to_xml("outputs/raw/constructors.xml")
file_drivers.to_xml("outputs/raw/drivers.xml")
file_driverStandings.to_xml("outputs/raw/driver_standings.xml")
file_lapTimes.to_xml("outputs/raw/lap_times.xml")
file_races.to_xml("outputs/raw/races.xml")
file_results.to_xml("outputs/raw/results.xml")

file_constructors.to_json("outputs/raw/constructors.json")
file_drivers.to_json("outputs/raw/drivers.json")
file_driverStandings.to_json("outputs/raw/driver_standings.json")
file_lapTimes.to_json("outputs/raw/lap_times.json")
file_races.to_json("outputs/raw/races.json")
file_results.to_json("outputs/raw/results.json")
