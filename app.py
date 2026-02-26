from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
  data = request.json
  start_time = time.time()

  # tu wywołamy algorytm genetyczny

  end_time = time.time()
  execution_time = round(end_time - start_time, 4)

  # przykładowe wyniki do zwrócenia przez funkcję
  mock_results = {
    "status" : "success",
    "time" : execution_time,
    "best_fitness" : 0.001,
    "chart_data" : [10, 8, 3, 1, 0.5, 0.001]
  }

  return jsonify(mock_results)

if __name__ == "__main__":
  app.run(debug=True)
