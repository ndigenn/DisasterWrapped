from flask import Flask, request

app = Flask(__name__)

@app.route('/process_text', methods=['POST'])
def process_text():
    import subprocess
    # Add your Python script logic here
    # Execute the script and get the output
    output = subprocess.check_output(['python3', 'script.py']).decode('utf-8')
    return output


if __name__ == '__main__':

    app.run(debug=True)
