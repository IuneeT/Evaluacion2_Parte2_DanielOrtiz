import urllib.parse
import requests

main_danielortiz = "https://www.mapquestapi.com/directions/v2/route?"
llave_danielortiz = "xVNwqRU7H3CeMwIsoSsNFCeugoVsI2e1"

eficiencia_combustible = {
    "City Car": 20,  # Km por litro
    "Sedan": 15,    # Km por litro
    "SUV": 12       # Km por litro
}

precio_bencina = 1400  # Precio por litro de bencina en CLP

while True:
    origen_danielortiz = input("Ubicacion de origen: ")
    if origen_danielortiz in ["quit", "q", "salir", "ok", "OK"]:
        break
    destino_danielortiz = input("Ubicacion de destino: ")
    if destino_danielortiz in ["quit", "q"]:
        break

    url = main_danielortiz + urllib.parse.urlencode({"key": llave_danielortiz, "from": origen_danielortiz, "to": destino_danielortiz})

    print("URL: " + url)

    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]

    if json_status == 0:
        print("API Status: " + str(json_status) + " = A successful route call.\n")
        print("===================================")
        print("Direccion desde " + origen_danielortiz + " hasta " + destino_danielortiz)
        print("Duracion del viaje: " + json_data["route"]["formattedTime"])
        distance_miles = json_data["route"]["distance"]
        distance_kilometers = distance_miles * 1.60934
        print("kilometros: " + str(distance_kilometers))
        tipo_vehiculo = input("Tipo de vehículo (City Car, Sedan, SUV): ")

        if tipo_vehiculo in eficiencia_combustible:
            eficiencia_vehiculo = eficiencia_combustible[tipo_vehiculo]

            # Calcular el consumo de combustible
            consumo_combustible = distance_kilometers / eficiencia_vehiculo
            print("Consumo de combustible: " + "{:.2f}".format(consumo_combustible) + " litros")

            # Calcular el costo de la bencina
            costo_bencina = consumo_combustible * precio_bencina
            print("Costo de la bencina: $" + "{:.2f}".format(costo_bencina) + " CLP")
        else:
            print("Tipo de vehículo no válido. Inténtalo nuevamente.")

        print("=============================================")
        print("Instrucciones de manejo:")
        for each in json_data["route"]["legs"][0]["maneuvers"]:
            print(each["narrative"] + " (" + "{:.2f}".format(each["distance"] * 1.61) + " km)")
        print("=============================================\n")
