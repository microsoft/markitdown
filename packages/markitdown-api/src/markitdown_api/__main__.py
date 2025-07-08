from markitdown_api.app import app

def main():
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
