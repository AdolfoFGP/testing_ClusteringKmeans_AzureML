from django.http import HttpResponse
from django.shortcuts import render
import urllib.request
import json
from . import settings
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def prediction_form(request):
    if request.method == 'POST':
        # Obtener los datos del formulario enviado por el usuario
        CulmenLength = float(request.POST['CulmenLength'])
        CulmenDepth = float(request.POST['CulmenDepth'])
        FlipperLength = int(request.POST['FlipperLength'])
        BodyMass = int(request.POST['BodyMass'])

        # Crear el objeto de datos para la solicitud al endpoint
        data = {
            "Inputs": {
                "input1": [
                    {
                        "CulmenLength": CulmenLength,
                        "CulmenDepth": CulmenDepth,
                        "FlipperLength": FlipperLength,
                        "BodyMass": BodyMass

                    }
                ]
            },
            "GlobalParameters": {}
        }

        # Convertir los datos a formato JSON
        body = str.encode(json.dumps(data))

        # URL y clave de API proporcionadas por Azure ML
        url = 'http://76fc89bd-7ce0-4472-a7ce-168851022868.brazilsouth.azurecontainer.io/score'
        api_key = settings.get_azure_api_key()  # Reemplaza con tu clave de API

                # Configurar las cabeceras de la solicitud
        headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key)}

        # Realizar la solicitud al endpoint de Azure ML
        req = urllib.request.Request(url, body, headers)

        try:
            response = urllib.request.urlopen(req)
            result = response.read().decode('utf-8')

            # Procesar la respuesta JSON obtenida
            prediction = json.loads(result)

            # Renderizar la página de resultados con la predicción obtenida
            return render(request, 'prediction_result.html', {'prediction': prediction})

        except urllib.error.HTTPError as error:
            # Manejar errores de solicitud
            error_message = f"The request failed with status code: {error.code}"
            return render(request, 'error.html', {'error_message': error_message})

    else:
        # Renderizar la página del formulario
        return render(request, 'prediction_form.html')






