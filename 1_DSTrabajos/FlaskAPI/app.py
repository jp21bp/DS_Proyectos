from flask import Flask, request
import numpy as np
import os, pickle, json
from flasgger import Swagger, swag_from

app = Flask(__name__)
swagger = Swagger(app)

def load_modelo():
    print(os.getcwd())
    fname = 'model_file.p'
    with open(fname, 'rb') as file:
        data = pickle.load(file)
        modelo = data['model']
    return modelo

@swag_from({
    'tags': ['Operaciones de Modelos'],
    'parameters': [
        {
            'name': 'arreglos',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'arrayssss': {
                        'type': 'array',
                        # 'items': {  # Solo necesario para 2d nested arrs
                        #     'type': 'array',
                        #     'items': {'type': 'integer'}
                        # },
                        'example': [1,2,3,4]
                    }
                },
                'required': ['arrayssss']
            }
        },
        {
            'name': 'a',
            'in': 'header',
            'required': False,
            'description': 'Arreglo',
            'type' : 'array',
            'items':{
                'type': 'number'
            },
            'collectionFormat': 'multi'  # Permite ?a=1&a=2&a=3
        },
        {
            'name': 'b',
            'in': 'query',
            'type': 'number',
            'required': False,
            'description': 'Segundo número'
        }
    ],
    'responses': {
        200: {
            'description': 'Suma calculada correctamente',
            'examples': {
                'application/json': {'resultado': 15}
            }
        },
        400: {
            'description': 'Parámetros inválidos'
        }
    }
})
@app.route('/predecir', methods=['POST'])
def predecir():
    """
    ---
    """
    print('AQUI')
    data = request.get_json(force=True)
    print(data)
    arrays = data.get('arrayssss')
    print(arrays)
    x = arrays
    # x = request.args.getlist('a', type=float)
    # print(x)
    x_in = np.array(x).reshape(1,-1)
    modelo = load_modelo()
    prediccion = modelo.predict(x_in)[0]
    respuesta = json.dumps({'respuesta': prediccion})
    return respuesta, 200




### Codigo de abajo trabaja con curl regular
# @app.route('/predecir2', methods=['GET'])
# def predecir2():
#     """
#     ---
#     """
#     print('AQUI')
#     if request.is_json:
#         print('OTRO')
#     request_json = request.get_json()
#     print('DOS')
#     x = request_json['input'] 
#     print(x)
#     x_in = np.array(x).reshape(1,-1)
#     modelo = load_modelo()
#     prediccion = modelo.predict(x_in)[0]
#     respuesta = json.dumps({'respuesta': prediccion})
#     return respuesta, 200


if __name__ == '__main__':
    app.run(debug=True)