import os

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "api.app:app",
        host=os.environ["HOST"],
        port=int(os.environ["PORT"]),
        reload=True,
    )
