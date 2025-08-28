from langchain_core.messages import SystemMessage, HumanMessage


def quality_to_DQDL(quality_data_session, llm_instance):

    system_prompt = """
You are a converter that transforms session-defined data model into AWS Glue Data Quality Definition Language (DQDL) format.

Given a JSON object containing data quality checks in the form:
- Each check includes:
  - `type`: "sql" or "text"
  - `description`: A human-readable explanation
  - `query`: [optional] A SQL statement that returns a single numeric value
  - A comparison threshold such as `mustBeLessThan`, `mustBeGreaterThan`, or `mustBeEqualTo`

Your task is to:
1. Convert each check into a corresponding DQDL rule using AWS Glue's declarative syntax.
2. Use `Rules:` section syntax in DQDL.
3. Generate a valid DQDL YAML file.
4. Set rule names based on the description (converted to lowercase and underscores).
5. Map thresholds to the proper `eval:` clause using `ASSERT <metric> <comparator> <value>`.

Output only the DQDL result (no extra explanation).

Example Input:
{
  "quality": [
    {
      "type": "sql",
      "description": "The maximum duration between two orders should be less that 3600 seconds",
      "query": "SELECT MAX(duration) AS max_duration \nFROM (\n  SELECT EXTRACT(EPOCH FROM (order_timestamp - LAG(order_timestamp) OVER (ORDER BY order_timestamp))) AS duration \n  FROM orders\n)\n",
      "mustBeLessThan": 3600
    },
    {
      "type": "sql",
      "description": "Row Count",
      "query": "SELECT count(*) as row_count\nFROM orders\n",
      "mustBeGreaterThan": 5
    }
  ]
}

Expected Output (DQDL):
Rules:
  - Name: max_duration_between_orders
    Description: The maximum duration between two orders should be less that 3600 seconds
    SqlQuery: >
      SELECT MAX(duration) AS max_duration
      FROM (
        SELECT EXTRACT(EPOCH FROM (order_timestamp - LAG(order_timestamp) OVER (ORDER BY order_timestamp))) AS duration
        FROM orders
      )
    Eval: ASSERT max_duration < 3600

  - Name: row_count
    Description: Row Count
    SqlQuery: >
      SELECT count(*) as row_count
      FROM orders
    Eval: ASSERT row_count > 5

"""

    message = [SystemMessage(content=system_prompt), HumanMessage(content=quality_data_session)]
    dqdl_data = llm_instance.invoke(message)

    return dqdl_data