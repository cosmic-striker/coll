from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    print("Starting minimal Flask test server...")
    try:
        app.run(host='127.0.0.1', port=8000, debug=False, use_reloader=False)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
