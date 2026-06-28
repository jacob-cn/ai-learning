from pathlib import Path
from mcp.server.fastmcp import FastMCP

def create_server(*, host: str = "127.0.0.1") -> FastMCP:
    """Factory function — builds an identical server instance every time."""
    mcp = FastMCP("notes-server", host=host)
    notes_dir = Path(__file__).parent / "notes"

    @mcp.tool()
    def list_notes() -> str:
        """List all available note files."""
        files = list(notes_dir.glob("*.md"))
        if not files:
            return "No notes found."
        return "\n".join(f.name for f in files)

    @mcp.tool()
    def read_note(filename: str) -> str:
        """Read the full content of a specific note file by name.

        Args:
            filename: The name of the note file, e.g. 'android_tips.md'

        Example:
            read_note('android_tips.md')
        """
        if not filename:
            return "Error: Filename cannot be empty."
        file_path = notes_dir / filename
        if not file_path.exists():
            return f"Error: '{filename}' not found."
        return file_path.read_text(encoding="utf-8")

    @mcp.tool()
    def search_notes(keyword: str) -> str:
        """Search for a keyword across all notes and return matching lines.

        Args:
            keyword: The word or phrase to search for
        """
        results = []
        for file_path in notes_dir.glob("*.md"):
            text = file_path.read_text(encoding="utf-8")
            for line_num, line in enumerate(text.splitlines(), 1):
                if keyword.lower() in line.lower():
                    results.append(f"{file_path.name}:{line_num}: {line.strip()}")
        if not results:
            return f"No matches found for '{keyword}'."
        return "\n".join(results)

    return mcp