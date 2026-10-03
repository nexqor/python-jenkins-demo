from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Python application deployed using Jenkins!"

@app.route("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    app.run(host="15.252.182.8", port=8000)
