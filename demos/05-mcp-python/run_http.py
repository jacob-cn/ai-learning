from notes_core import create_server

if __name__ == "__main__":
    mcp = create_server(host="0.0.0.0")
    try:
        mcp.run(transport="streamable-http")
    except KeyboardInterrupt:
        pass
