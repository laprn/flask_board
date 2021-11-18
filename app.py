from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Flask board\n url title\n /posts/objectId First Post\n'

if __name__ == '__main__':
    app.run()