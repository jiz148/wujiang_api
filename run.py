# add system path
import sys
import os
project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_path)
from wujiang_api_backend.api import app


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)

