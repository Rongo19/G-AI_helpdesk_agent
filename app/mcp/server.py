import re
import time
import psycopg
from psycopg.rows import dict_row
from fastmcp import FastMCP

from app.config import settings


# Initialize MCP server
mcp = FastMCP("GoAified Employee Database")


@mcp.tool
def get_employee_leave_balance(employee_id: str) -> dict:

    start = time.perf_counter()

    print("[MCP] Tool execution started", flush=True)

    employee_id = employee_id.strip().upper()

    if not re.fullmatch(r"E\d{3}", employee_id):
        return {
            "status": "error",
            "message": "Invalid employee ID format."
        }

    print("[MCP] Connecting to PostgreSQL...", flush=True)

    try:
        with psycopg.connect(
            settings.database_url,
            row_factory=dict_row,
            connect_timeout=5
        ) as connection:

            print(
                f"[MCP] Database connected in "
                f"{time.perf_counter() - start:.2f}s",
                flush=True
            )

            with connection.cursor() as cursor:

                query_start = time.perf_counter()

                cursor.execute(
                    """
                    SELECT
                        employee_id,
                        full_name,
                        department,
                        annual_leave_days,
                        used_leave_days,
                        remaining_leave_days
                    FROM employee_leave_balances
                    WHERE employee_id = %s
                    """,
                    (employee_id,)
                )

                employee = cursor.fetchone()

                print(
                    f"[MCP] Query completed in "
                    f"{time.perf_counter() - query_start:.2f}s",
                    flush=True
                )

    except psycopg.Error as error:
        raise RuntimeError(
            "Unable to retrieve employee information."
        ) from error

    print(
        f"[MCP] Total execution time: "
        f"{time.perf_counter() - start:.2f}s",
        flush=True
    )

    if employee is None:
        return {
            "status": "not_found",
            "message": f"No employee found with ID {employee_id}."
        }

    return {
        "status": "success",
        "employee": dict(employee)
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")