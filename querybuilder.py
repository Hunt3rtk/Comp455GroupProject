def build_query_string(columns, search_term, order_by_column, limit):
    query_string = f"SELECT {columns}\n"
    query_string += f"FROM books\n"
    query_string += "WHERE ("
    if isinstance(columns, str):
        query_string += f"\"{columns}\" LIKE '%{search_term}%'"
    else:
        query_string += " OR ".join(
            [f"\"{column}\" LIKE '%{search_term}%'" for column in columns]
        )
    query_string += ")\n"
    query_string += f'ORDER BY "{order_by_column}"\n'
    query_string += f"LIMIT {limit}"
    return query_string


query = build_query_string("all", "Harry", "title", 10)
print(query)
