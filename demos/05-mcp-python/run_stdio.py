from notes_core import create_server

if __name__ == "__main__":
    mcp = create_server()
    try:
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        pass