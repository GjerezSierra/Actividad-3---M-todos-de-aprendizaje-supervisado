import pandas as pd
from sklearn.linear_model import LinearRegression

# Cargar los conjuntos de datos
dataconexion_path = "C:/Users/jerez/OneDrive - cabv3151/Desktop/Actividad3/dataset/dataconexion.csv"
datademanda_path = "C:/Users/jerez/OneDrive - cabv3151/Desktop/Actividad3/dataset/datademanda.csv"

dataconexion_df = pd.read_csv(dataconexion_path)
datademanda_df = pd.read_csv(datademanda_path)

# Eliminar espacios en blanco alrededor de los nombres de las estaciones
dataconexion_df['EstacionOrigen'] = dataconexion_df['EstacionOrigen'].str.strip()
dataconexion_df['EstacionDestino'] = dataconexion_df['EstacionDestino'].str.strip()
datademanda_df['Estacion'] = datademanda_df['Estacion'].str.strip()

# Solicitar al usuario la estación de origen y destino
inicio = input("Ingrese la estación de origen: ")
destino = input("Ingrese la estación de destino: ")

# Filtrar las horas disponibles en la ruta seleccionada desde datademanda.csv
horas_disponibles = datademanda_df[(datademanda_df['Estacion'] == inicio)]['Hora'].unique()

if len(horas_disponibles) == 0:
    print(f"No hay datos disponibles para la ruta seleccionada de {inicio} a {destino}.")
else:
    # Mostrar las horas disponibles al usuario
    print("Horas disponibles en la estación de inicio:")
    for hora in horas_disponibles:
        print(hora)

    # Pedir al usuario que registre la hora
    hora_elegida = input("Por favor, seleccione una hora de las disponibles: ")

    # Calcular la distancia total del viaje desde dataconexion.csv
    distancia_total = dataconexion_df[(dataconexion_df['EstacionOrigen'] == inicio) & (dataconexion_df['EstacionDestino'] == destino)]['Distancia'].sum()

    # Calcular el tiempo estimado de viaje utilizando un modelo de regresión desde dataconexion.csv
    X = datademanda_df[(datademanda_df['Estacion'] == inicio) & (datademanda_df['Hora'] == hora_elegida)]['CantidadPasajeros']
    model = LinearRegression()
    model.fit(X.values.reshape(-1, 1), dataconexion_df[(dataconexion_df['EstacionOrigen'] == inicio) & (dataconexion_df['EstacionDestino'] == destino)]['TiempoEstimadoViaje'])
    tiempo_estimado = model.predict([[X.mean()]])[0]

    # Recomendar la mejor hora para viajar (usando la hora con la menor cantidad estimada de pasajeros) desde datademanda.csv
    mejor_hora_recomendada = datademanda_df[(datademanda_df['Estacion'] == inicio)].groupby('Hora')['CantidadPasajeros'].mean().idxmin()

    # Calcular la cantidad estimada de pasajeros en la estación de inicio a la hora elegida
    cantidad_estimada_pasajeros = datademanda_df[(datademanda_df['Estacion'] == inicio) & (datademanda_df['Hora'] == hora_elegida)]['CantidadPasajeros'].mean()

    # Mostrar la información al usuario
    print(f"Tiempo estimado del viaje entre {inicio} y {destino}: {tiempo_estimado} minutos")
    print(f"Distancia total entre {inicio} y {destino}: {distancia_total} kilómetros")
    print(f"Recomendación de la mejor hora para viajar: {mejor_hora_recomendada}")
    print(f"Cantidad estimada de pasajeros en la estación de inicio a las {hora_elegida}: {cantidad_estimada_pasajeros}")
