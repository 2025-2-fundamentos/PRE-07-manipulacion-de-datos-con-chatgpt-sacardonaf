#Leo los archivos de la carpeta files/input
import os
input_files = os.listdir("files/input/")

#Calcule el promedio de las columnas "hours-logged" y "miles-logged" en la 
#tabla "timesheet", agrupando los resultados por cada conductor (driverId).
import pandas as pd
timesheet = pd.read_csv("files/input/timesheet.csv")
avg_timesheet = timesheet.groupby("driverId")[["hours-logged", "miles-logged"]].mean().reset_index()
avg_timesheet.columns = ["driverId", "avg_hours_logged", "avg_miles_logged"]

#Cree una tabla llamada "timesheet_with_means" basada en la tabla "timesheet", 
# agregando una columna con el promedio de "hours-logged" para cada conductor 
# (driverId).
timesheet_with_means = timesheet.merge(avg_timesheet[["driverId", "avg_hours_logged"]], on="driverId", how="left")
timesheet_with_means = timesheet_with_means.rename(columns={"avg_hours_logged": "mean_hours_logged"})
timesheet_with_means = timesheet_with_means[["driverId", "hours-logged", "miles-logged", "mean_hours_logged"]]
timesheet_with_means = timesheet_with_means.sort_values(by=["driverId"])

#Cree una tabla llamada "timesheet_below" a partir de "timesheet_with_means", filtrando los registros donde "hours-logged" sea menor que "mean_hours-logged".
timesheet_below = timesheet_with_means[timesheet_with_means["hours-logged"] < timesheet_with_means["mean_hours_logged"]]
timesheet_below = timesheet_below.reset_index(drop=True)
timesheet_below = timesheet_below[["driverId", "hours-logged", "miles-logged", "mean_hours_logged"]]
timesheet_below = timesheet_below.sort_values(by=["driverId"])
timesheet_below = timesheet_below.reset_index(drop=True)

#Cree una tabla llamada "sum_timesheet" agrupando la tabla "timesheet" por driverId y calculando la suma de las columnas "hours-logged" y "miles-logged".
sum_timesheet = timesheet.groupby("driverId")[["hours-logged", "miles-logged"]].sum().reset_index()
sum_timesheet.columns = ["driverId", "total_hours_logged", "total_miles_logged"]
sum_timesheet = sum_timesheet.sort_values(by="driverId").reset_index(drop=True)
sum_timesheet = sum_timesheet[["driverId", "total_hours_logged", "total_miles_logged"]]

#Crea una tabla llamada "min_max_timesheet" a partir de la tabla "timesheet", agrupando los datos por driverId y calculando el valor mínimo y máximo de la columna "hours-logged".
min_max_timesheet = timesheet.groupby("driverId")["hours-logged"].agg(["min", "max"]).reset_index()
min_max_timesheet = min_max_timesheet.rename(columns={"min": "min_hours_logged", "max": "max_hours_logged"})
min_max_timesheet = min_max_timesheet[["driverId", "min_hours_logged", "max_hours_logged"]]
min_max_timesheet = min_max_timesheet.sort_values(by="driverId").reset_index(drop=True)
min_max_timesheet = min_max_timesheet[["driverId", "min_hours_logged", "max_hours_logged"]]

#Crea una tabla llamada "summary" combinando las tablas "sum_timesheet" y "drivers" mediante la clave driverId. De la tabla "drivers", incluye únicamente las columnas "driverId" y "name".
drivers = pd.read_csv("files/input/drivers.csv")
summary = sum_timesheet.merge(drivers[["driverId", "name"]], on="driverId", how="left")
summary = summary[["driverId", "name", "total_hours_logged", "total_miles_logged"]]
summary = summary.sort_values(by="driverId").reset_index(drop=True)
summary = summary[["driverId", "name", "total_hours_logged", "total_miles_logged"]]
summary.to_csv("files/output/summary.csv", index=False)

# Guarda la tabla "summary" en un archivo CSV con el nombre "summary.csv" en la carpeta "files/output".
summary.to_csv("files/output/summary.csv", index=False)

#Crea una tabla llamada "top10" con los 10 conductores que tienen la mayor cantidad de millas registradas, ordenando los datos en forma descendente por la columna "miles-logged".
top10 = sum_timesheet.merge(drivers[["driverId", "name"]], on="driverId", how="left")
top10 = top10[["driverId", "name", "total_hours_logged", "total_miles_logged"]]
top10 = top10.sort_values(by="total_miles_logged", ascending=False).head(10).reset_index(drop=True)
top10 = top10[["driverId", "name", "total_hours_logged", "total_miles_logged"]]
top10.to_csv("files/output/top10.csv", index=False)

# Crea un gráfico de barras horizontales utilizando los datos de la tabla "top10", donde el eje y represente los nombres de los conductores y el eje x la cantidad de millas registradas. Asegúrate de que los conductores con más millas estén en la parte superior del gráfico.
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
plt.barh(top10["name"], top10["total_miles_logged"], color='skyblue')
plt.xlabel("Total Miles Logged")
plt.ylabel("Driver Name")
plt.title("Top 10 Drivers by Total Miles Logged")
plt.gca().invert_yaxis()  # Invertir el eje y para que el conductor con más millas esté en la parte superior
plt.tight_layout()
plt.savefig("files/plots/top10_drivers.png")

# Guarda el gráfico en un archivo PNG con el nombre "top10_drivers.png" en la carpeta "files/plots".
plt.savefig("files/plots/top10_drivers.png")
