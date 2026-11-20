import asyncio
import json

from fastmcp import Client
from langchain_core.tools import tool

from app.mcp.server import mcp as mcp_server
from app.rag.qa import answer_policy_question


@tool
async def search_hr_it_policies(
    question: str,
    category: str = "ALL"
) -> str:
    """
    Search company HR and IT policy documents.

    Use this tool for questions about company policies,
    leave rules, work from home, IT security and procedures.

    Args:
        question: The employee's policy-related question.
        category: ALL, HR or IT.

    Returns:
        Answer generated from retrieved policy documents
        along with their source references.
    """

    category = category.strip().upper()

    if category not in {"ALL", "HR", "IT"}:
        return json.dumps({
            "error": "Category must be ALL, HR or IT."
        })

    result = await asyncio.to_thread(
        answer_policy_question,
        question,
        None if category == "ALL" else category
    )

    return json.dumps(result, ensure_ascii=False)


@tool
async def get_employee_leave_balance(
    employee_id: str
) -> str:
    """
    Retrieve an employee's leave balance from PostgreSQL
    through the GoAified MCP server.

    Use this tool whenever an employee asks about their
    leave balance or another employee's leave balance.

    Args:
        employee_id: Employee ID, for example E102.

    Returns:
        Employee information and remaining leave days.
    """

    async with Client(mcp_server) as client:

        result = await client.call_tool(
            "get_employee_leave_balance",
            {
                "employee_id": employee_id
            }
        )

    if result.is_error:
        return json.dumps({
            "status": "error",
            "message": "Unable to retrieve employee information."
        })

    return json.dumps(
        result.structured_content,
        ensure_ascii=False
    )