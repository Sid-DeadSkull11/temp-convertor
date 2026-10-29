from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return '''
    <h3>Temperature Converter</h3>
    <form action="/result">
        <input name="temp" type="number" step="any" placeholder="Enter temperature" required><br><br>
        <input type="radio" name="type" value="c_to_f" checked> Celsius to Fahrenheit<br>
        <input type="radio" name="type" value="f_to_c"> Fahrenheit to Celsius<br><br>
        <button>Convert</button>
    </form>
    '''

@app.route("/result")
def result():
    try:
        calc_type = request.args.get("type")
        temp_val = float(request.args.get("temp"))

        if calc_type == "c_to_f":
            converted = (temp_val * 9/5) + 32
            output = f"{temp_val}°C is equal to {converted:.2f}°F"
        elif calc_type == "f_to_c":
            converted = (temp_val - 32) * 5/9
            output = f"{temp_val}°F is equal to {converted:.2f}°C"
        else:
            return "<h3>Error</h3>Invalid operation variant selected.<br><br><a href='/'>Back</a>"

        return f"<h3>Result</h3>{output}<br><br><a href='/'>Back</a>"
    except (ValueError, TypeError):
        return "<h3>Error</h3>Invalid input parameters.<br><br><a href='/'>Back</a>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)