from flask import Flask, render_template, request, jsonify
import numpy as np
import math
import os

app = Flask(__name__)

world_arr = np.load("static/world_arr.npy")

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/rate", methods=['POST', 'GET'])
def rateRoute():
    route = request.get_json()
    
    num_wps = len(route)
    avg_density = round(getAverageDensity(route), 2)
    total_dist = round(getTotalDistance(route), 2)
    avg_dist_between_wps = round(total_dist / num_wps, 2)
    
    rating = {
        "num_wps": num_wps,
        "avg_density": avg_density,
        "total_dist": total_dist,
        "avg_dist_between_wps": avg_dist_between_wps
    }
    
    return jsonify(rating)

def getDensity(x, y, z):
    x -= 192
    y -= 30
    z -= 192
    density = np.sum(world_arr[x - 1 : x + 2, z - 1 : z + 2, y + 1 : y + 5])
    density -= np.sum(world_arr[x, z, y + 1 : y + 3])
    return density

def getAverageDensity(route):
    total_density = 0
    for wp in route:
        total_density += getDensity(wp["x"], wp["y"], wp["z"])
    avg_density = total_density / len(route)
    return avg_density

def getDistance(x1, y1, z1, x2, y2, z2):
    dist = math.sqrt(math.pow(x2 - x1, 2) +
                math.pow(y2 - y1, 2) +
                math.pow(z2 - z1, 2)* 1.0)
    return dist

def getTotalDistance(route):
    total_dist = 0
    for i, wp1 in enumerate(route):
        wp2 = route[(i + 1) % len(route)]
        total_dist += getDistance(wp1["x"], wp1["y"], wp1["z"], wp2["x"], wp2["y"], wp2["z"])
    return total_dist


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
