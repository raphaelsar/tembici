#!/bin/sh
import os
from app import app
PORT = os.environ.get('PORT') or 5000

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(PORT))
