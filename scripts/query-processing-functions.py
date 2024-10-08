def parser(query):
    query = query.strip()
    if len(query) == 0:
        return False

    words = query.upper().split()
    
    state = "INITIAL"
    states = {
        "INITIAL": ["SELECT"],
        "SELECT": ["FROM", "WHERE", "GROUP BY", "HAVING", "ORDER BY"],
        "FROM": ["WHERE", "GROUP BY", "HAVING", "ORDER BY"],
        "WHERE": ["GROUP BY", "HAVING", "ORDER BY"],
        "GROUP BY": ["HAVING", "ORDER BY"],
        "HAVING": ["ORDER BY"],
        "ORDER BY": []
    }

    for word in words:
        if state not in states or word not in states[state]:
            return False  # Erro de sintaxe
        state = word

    return state == "ORDER BY"  # Assumimos que "ORDER BY" é o último estado válido

# Exemplo de uso
query1 = "SELECT * FROM customers WHERE country = 'USA'"

print(parser(query1)) 