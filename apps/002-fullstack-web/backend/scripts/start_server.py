import os
import sys

import uvicorn


def main() -> None:
    sys.path.insert(0, ".")

    # Hugging Face always expects 7860
    port = 7860

    import contextlib

    # Optional override for local dev or other platforms
    env_port = os.environ.get("PORT")
    if env_port:
        with contextlib.suppress(ValueError):
            port = int(env_port)

    print(f"Starting server on port {port}")

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
    )


if __name__ == "__main__":
    main()
