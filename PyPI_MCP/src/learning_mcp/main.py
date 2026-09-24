from learning_mcp.tools import mcp
import learning_mcp.prompts  # Registers prompt definitions with mcp.
import learning_mcp.resources  # Registers resource definitions with mcp.

def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
