"""End-to-end test: start the server over stdio and talk to it with an MCP client."""

import sys

import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

EXPECTED_TOOLS = {
    "get-collection-overview",
    "get-review-stats",
    "find-notes",
    "find-cards",
    "add-or-update-notes",
    "suspend-cards",
    "unsuspend-cards",
}


@pytest.mark.asyncio
async def test_server_lists_tools_and_resources():
    params = StdioServerParameters(
        command=sys.executable, args=["-c", "from anki_mcp import main; main()"]
    )
    async with (
        stdio_client(params) as (read, write),
        ClientSession(read, write) as session,
    ):
        await session.initialize()

        tools = await session.list_tools()
        assert {t.name for t in tools.tools} == EXPECTED_TOOLS

        resources = await session.list_resources()
        uris = {str(r.uri) for r in resources.resources}
        assert "anki://docs/search-syntax" in uris

        doc = await session.read_resource("anki://docs/search-syntax")
        assert doc.contents[0].text
