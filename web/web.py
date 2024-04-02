from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')

def read_abc_file():
    try:
        with open('./output.abc', 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"The file ./output.abc does not exist.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def index():
    # abcContent = read_abc_file()
    return render_template('index.html', name = "X:1\nK:D\nDD AA|BBA2|\n")

if __name__ == '__main__':
    app.run(debug=True)
