from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return '''
    <h3>Temperature Converter (Push 1)</h3>
    <form action="/result">
        <label>Convert Celsius to Fahrenheit:</label><br><br>
        <input name="celsius" type="number" step="any" placeholder="Temperature in °C" required>
        <button>Convert</button>
    </form>
    '''

@app.route("/result")
def result():
    try:
        celsius = float(request.args.get("celsius"))
        fahrenheit = (celsius * 9/5) + 32
        return f"<h3>Result</h3>{celsius}°C is equal to {fahrenheit:.2f}°F<br><br><a href='/'>Back</a>"
    except (ValueError, TypeError):
        return "<h3>Error</h3>Invalid input value.<br><br><a href='/'>Back</a>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)