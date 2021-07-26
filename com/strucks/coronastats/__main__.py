#!/usr/bin/env python3

import connexion
from flask_cors import CORS

from com.strucks.coronastats import encoder


def main():
    app = connexion.App(__name__, specification_dir='openapi/')
    CORS(app.app)
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'coronabackend'},
                pythonic_params=True)

    app.run(port=5010)


if __name__ == '__main__':
    main()
