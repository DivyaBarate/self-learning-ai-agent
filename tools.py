import ast
import operator
import requests
import re
from datetime import datetime

# =========================
# Calculator Tool
# =========================

def calculate(expression):

    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod
    }


    def solve(node):

        if isinstance(node, ast.Constant):

            if isinstance(node.value, (int, float)):

                return node.value

            raise ValueError("Invalid number")


        if isinstance(node, ast.BinOp):

            left = solve(node.left)

            right = solve(node.right)

            operation = operators.get(type(node.op))

            if operation is None:

                raise ValueError("Invalid operator")

            return operation(left, right)


        if isinstance(node, ast.UnaryOp):

            value = solve(node.operand)

            if isinstance(node.op, ast.USub):

                return -value

            if isinstance(node.op, ast.UAdd):

                return value

            raise ValueError("Invalid operation")


        raise ValueError("Invalid expression")


    tree = ast.parse(expression, mode="eval")

    return solve(tree.body)


# =========================
# Date and Time Tool
# =========================

def get_current_datetime():

    now = datetime.now()

    date = now.strftime("%d-%m-%Y")

    time = now.strftime("%I:%M:%S %p")

    return f"Date: {date}, Time: {time}"


# =========================
# Web Search Tool
# =========================

def web_search(query):

    url = "https://en.wikipedia.org/w/api.php"

    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srlimit": 1,
        "format": "json"
    }

    headers = {
        "User-Agent": "Self-Learning-AI-Agent/1.0"
    }

    try:

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        results = data.get("query", {}).get("search", [])

        if results:

            result = results[0]

            title = result.get("title", query)

            excerpt = result.get("snippet", "")

            # Remove HTML tags
            excerpt = re.sub(
                r"<[^>]+>",
                "",
                excerpt
            )

            return (
                f"Title: {title}\n"
                f"Information: {excerpt}"
            )

        return "No information found for this topic."

    except requests.exceptions.RequestException as e:

        return f"Web search error: {e}"

    except Exception as e:

        return f"Web search error: {e}"