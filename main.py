from flask import Flask, request, render_template, redirect, url_for
import json

# Initialize Flask app
app = Flask(__name__)

# Initialize the data storage
DATA_FILE = "fitness_data.json"

def load_data():
    """Load fitness data from a file."""
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_data(data):
    """Save fitness data to a file."""
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/')
def index():
    """Home page to display options."""
    return render_template('index.html')

@app.route('/log', methods=['GET', 'POST'])
def log_activity():
    """Log daily fitness activities."""
    data = load_data()

    if request.method == 'POST':
        date = request.form['date']
        steps = int(request.form['steps'])
        calories = float(request.form['calories'])
        water = float(request.form['water'])

        if date not in data:
            data[date] = {"steps": 0, "calories": 0, "water": 0}

        data[date]["steps"] += steps
        data[date]["calories"] += calories
        data[date]["water"] += water

        save_data(data)
        return redirect(url_for('index'))

    return render_template('log_activity.html')

@app.route('/progress', methods=['GET', 'POST'])
def view_progress():
    """View fitness progress for a specific date or all time."""
    data = load_data()
    progress = None

    if request.method == 'POST':
        date = request.form['date']

        if date == 'all':
            if not data:
                progress = "No data available."
            else:
                total_steps = sum(entry["steps"] for entry in data.values())
                total_calories = sum(entry["calories"] for entry in data.values())
                total_water = sum(entry["water"] for entry in data.values())

                progress = {
                    "type": "all",
                    "total_steps": total_steps,
                    "total_calories": total_calories,
                    "total_water": total_water
                }
        elif date in data:
            progress = {
                "type": "date",
                "date": date,
                "steps": data[date]['steps'],
                "calories": data[date]['calories'],
                "water": data[date]['water']
            }
        else:
            progress = "No data found for the specified date."

    return render_template('view_progress.html', progress=progress)

if __name__ == "__main__":
    app.run(debug=True)


# http://127.0.0.1:5000