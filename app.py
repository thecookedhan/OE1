from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
  params = request.json
  start_time = time.perf_counter()

  # tu wywołamy algorytm genetyczny

  end_time = time.perf_counter()
  execution_time = end_time - start_time

  # przykładowe wyniki do zwrócenia przez funkcję
  mock_results = {
    "time" : f"{execution_time:.4f} s",
    "best_fitness" : 0.001,
    "chart_data" : [10, 8, 3, 1, 0.5, 0.001]
  }

  return jsonify(mock_results)

if __name__ == "__main__":
  app.run(debug=True)
