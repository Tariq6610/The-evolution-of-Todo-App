import os

import uvicorn


def main() -> None:
    # Get the port from environment variable, default to 8000 if not set
    port_str: str = os.environ.get("PORT", "8000")

    # Convert the port to integer
    try:
        port: int = int(port_str)
    except ValueError:
        print(f"Invalid PORT value: '{port_str}'. Using default port 8000.")
        port = 8000

    print(f"Starting server on port {port}")

    # Run the uvicorn server
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=port,
        reload=False,  # Disable reload in production
    )


if __name__ == "__main__":
    main()
