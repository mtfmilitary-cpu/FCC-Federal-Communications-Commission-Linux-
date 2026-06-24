import gzip
import json
import os
from flask import Flask, render_template, request

app = Flask(__name__)

def load_global_data():
    """Reads the compressed world JSON dataset entirely offline."""
    json_path = os.path.join(app.root_path, 'static', 'locations.json.gz')
    try:
        with gzip.open(json_path, 'rt', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/phonetic')
def phonetic():
    military_alphabet = {
        "A": "Alpha", "B": "Bravo", "C": "Charlie", "D": "Delta", 
        "E": "Echo", "F": "Foxtrot", "G": "Golf", "H": "Hotel",
        "I": "India", "J": "Juliet", "K": "Kilo", "L": "Lima",
        "M": "Mike", "N": "November", "O": "Oscar", "P": "Papa",
        "Q": "Quebec", "R": "Romeo", "S": "Sierra", "T": "Tango",
        "U": "Uniform", "V": "Victor", "W": "Whiskey", "X": "X-ray",
        "Y": "Yankee", "Z": "Zulu"
    }
    return render_template('phonetic.html', alphabet=military_alphabet)

@app.route('/morse')
def morse():
    morse_alphabet = {
        "A": "• —", "B": "— • • •", "C": "— • — •", "D": "— • •", 
        "E": "•", "F": "• • — •", "G": "— — •", "H": "• • • •",
        "I": "• •", "J": "• — — —", "K": "— • —", "L": "• — • •",
        "M": "— —", "N": "— •", "O": "— — —", "P": "• — — •",
        "Q": "— — • —", "R": "• — •", "S": "• • •", "T": "—",
        "U": "• • —", "V": "• • • —", "W": "• — —", "X": "— • • —",
        "Y": "— • — —", "Z": "— — • •",
        "1": "• — — — —", "2": "• • — — —", "3": "• • • — —",
        "4": "• • • • —", "5": "• • • • •", "6": "— • • • •",
        "7": "— — • • •", "8": "— — — • •", "9": "— — — — •",
        "0": "— — — — —"
    }
    return render_template('morse.html', morse=morse_alphabet)

@app.route('/regions')
def regions():
    all_data = load_global_data()
    selected_country = request.args.get('country')
    
    if selected_country:
        country_info = next((c for c in all_data if c['name'] == selected_country), None)
        return render_template('country_detail.html', country=country_info)
    
    country_list = sorted([c['name'] for c in all_data])
    return render_template('regions.html', countries=country_list)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
