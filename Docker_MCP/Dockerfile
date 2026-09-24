FROM python:3.11-slim

# Install uv and uvx
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory to /app
WORKDIR /app

# Pre-install DuckDuckGo so uvx does not download it at runtime.
RUN uv tool install duckduckgo-mcp-server

# Copy the project and install this repository's learning MCP package.
COPY . .
RUN pip install -r docker_mcp/requirements.txt
RUN pip install ./pypi_mcp

# The custom MCP server can only access this folder by default.
RUN mkdir /workspace
ENV MCP_WORKSPACE=/workspace

# Ensure the uv tools path is in the system PATH
ENV PATH="/root/.local/bin:${PATH}"

EXPOSE 8000

# Run the gateway.
CMD ["python", "-u", "app/server.py"]
