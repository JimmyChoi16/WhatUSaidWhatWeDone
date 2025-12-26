from app import create_app

app = create_app()

if __name__ == "__main__":
    # Change the backend host and port here if needed
    app.run(host="0.0.0.0", port=5050, debug=True)
