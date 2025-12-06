import uvicorn

from app.config import Config

config = Config()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=config.API_HOST,
        port=config.API_PORT,
        log_level="critical",
        reload=True,
    )
