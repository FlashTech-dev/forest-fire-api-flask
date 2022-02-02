from flask import Flask, render_template
app = Flask(__name__, template_folder='template')



@app.route('/')
def hello_world():
    return render_template("forest_fire.html")

if __name__ == '__main__':
    app.run(debug=True)