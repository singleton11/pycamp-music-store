Swagger
=======

The main swagger file is ``artifacts/swagger.yaml``.

`Speca for swagger file <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md>`_

It's generated from several files which is stored in ``docs/swagger``.

Example of structure of this folder is:

.. code-block:: bash

  docs/swagger
  ├── api
  │   ├── auth
  │   │   ├── check_username.yaml
  │   │   ├── login.yaml
  │   │   ├── logout.yaml
  │   │   ├── password_change.yaml
  │   │   ├── password_reset_confirm.yaml
  │   │   ├── password_reset.yaml
  │   │   ├── register.yaml
  │   │   ├── user_avatar.yaml
  │   │   ├── user_location.yaml
  │   │   └── user.yaml
  │   ├── oauth
  │   │   ├── facebook.yaml
  │   │   └── google.yaml
  │   ├── models.yaml
  │   ├── parameters.yaml
  │   ├── paths.yaml
  │   └── responses.yaml
  └── main.yaml


Structure
---------

main.yaml
^^^^^^^^^

This file contains common structure and information of swagger file.

api/models.yaml
^^^^^^^^^^^^^^^

This file contains description of data models of API.

Example:

.. code-block:: yaml

  Location:
    title: Location
    description: Location coordinates
    type: object
    properties:
      lon:
        type: number
        description: Longitude
      lat:
        type: number
        description: Latitude
    required:
      - lon
      - lat


This example describes structure for this data (location coords):

.. code-block:: json

  {
    "lon": 29.993232,
    "lat": 56.213112    
  }


api/parameters.yaml
^^^^^^^^^^^^^^^^^^^

This file contains description of common parameters for requests.

.. code-block:: yaml

  # Body parameter
  OAuthData:
    name: OAuthData
    in: body
    required: true
    schema:
      $ref: 'definitions.yaml#/OAuthData'

  # Header parameter
  UserTimezone:
    name: User-Timezone
    in: header
    required: false
    type: string
    description: User's timezone


api/responses.yaml
^^^^^^^^^^^^^^^^^^

This file contains description of common responses of API methods.

.. code-block:: yaml

  BadRequest:
    description: Bad Request
    schema:
      $ref: 'definitions.yaml#/ErrorDetails'


  SuccessAuth:
    description: Successfully authenticated
    schema:
      $ref: "definitions.yaml#/TokenInfo"

api/paths.yaml
^^^^^^^^^^^^^^

This file contains references to description of endpoints.

Example:

.. code-block:: yaml

  # Auth endpoints
  /auth/register/:
    $ref: 'auth/register.yaml#'
  /auth/login/:
    $ref: 'auth/login.yaml#'
  /auth/logout/:
    $ref: 'auth/logout.yaml#'

  # OAuth endpoints
  /oauth/facebook/:
    $ref: 'oauth/facebook.yaml#'
  /oauth/google/:
    $ref: 'oauth/google.yaml#'


api/{folder_name}/
^^^^^^^^^^^^^^^^^^

Every folder should contain files describing endpoints.

api/{folder_name}/{endpoint_name}.yaml
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Every endpoint you want to include in swagger file should have own file.
Then you should connect endpoint and your file in paths.yaml.

Example (login method):

.. code-block:: yaml

  post:
    description: This endpoint is responsible for authentication
    operationId: AuthLogin
    tags:
      - auth
    parameters:
      - name: LoginData
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              description: User's email
            password:
              type: string
              format: password
              description: User's password
          required:
            - email
            - password
    responses:
      '200':
        $ref: "../responses.yaml#/SuccessAuth"
      '400':
        $ref: '../responses.yaml#/BadRequest'
    security: []


In order to display it in swagger file you should have this line in 
paths.yaml:

.. code-block:: yaml
  
  /auth/login/:
    $ref: 'auth/login.yaml#'

Working with swagger file
-------------------------

To build swagger file and watch your swagger file in browser you should run:

.. code-block:: bash

  make swagger


So you can edit swagger files and see result in real time in 
`your browser <http://127.0.0.1:8080/>`_
