from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def hello_world():
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return 'Hello World from sudigitalCluster X Today in {} is huff!!!'.format(current_date)
# main driver function
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)
