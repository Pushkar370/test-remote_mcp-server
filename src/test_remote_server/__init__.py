def main():
    from main import mcp
    mcp.run(transport="http", host="0.0.0.0", port=8000)