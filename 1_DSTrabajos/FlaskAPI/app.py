from flask import Flask, request
import numpy as np
import os, pickle, json
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

def load_modelo():
    print(os.getcwd())
    fname = 'model_file.p'
    with open(fname, 'rb') as file:
        data = pickle.load(file)
        modelo = data['model']
    return modelo

@app.route('/predecir', methods=['GET'])
def predecir():
    """
    ---
    parameters:
        - name: input
          in: query
          description: arreglo para modelo
          schema:
            type: object
            properties:
              array:
                type: array
              example:
                array : [7, 0.27, 0.36, 20.7, 0.045, 45, 170]
    responses:
      200:
        description: Success
      400: 
        description: Failed
    """
    print('AQUI')
    if request.is_json:
        print('OTRO')
    request_json = request.get_json()
    print('DOS')
    x = request_json['input']
    # x = request.form.get('input')
    print(x)
    x_in = np.array(x).reshape(1,-1)
    modelo = load_modelo()
    prediccion = modelo.predict(x_in)[0]
    respuesta = json.dumps({'respuesta': prediccion})
    return respuesta, 200


if __name__ == '__main__':
    app.run(debug=True)