# OTIMIZADOR DE CONSULTA

def extract_projections(sql_query):
    start = sql_query.find("SELECT") + len("SELECT")
    end = sql_query.find("FROM")
    projections = sql_query[start:end].strip()
    return projections.split(", ")

def extract_conditions(sql_query):
    where_part = sql_query.upper().find("WHERE") + len("WHERE")
    conditions = sql_query[where_part:].strip()
    return conditions

def extract_tables_and_joins(sql_query):
    from_part = sql_query.find("FROM") + len("FROM")
    where_part = sql_query.find("WHERE")
    
    if where_part != -1:
        join_section = sql_query[from_part:where_part].strip()
    else:
        join_section = sql_query[from_part:].strip()

    if "JOIN" in join_section:
        first_join_pos = join_section.find("JOIN")
        table = join_section[:first_join_pos].strip()
    else:
        table = join_section.strip()

    join_clauses = []
    tables = [table]
    join_keywords = join_section.split("JOIN")[1:]
    
    for keyword in join_keywords:
        join_clause = keyword.strip()
        partes_join = join_clause.split("ON")
        table = partes_join[0].strip()
        clause = partes_join[1].strip()
        tables.append(table)
        join_clauses.append(clause)

    return tables, join_clauses


def apply_reduce_tuplas(table, conditions):
    conditions_extract = conditions.split("^")

    sql_reduce = []

    for condition in conditions_extract:
        table_condition = condition.split('.')[0].strip()
        rule = condition.split('.')[1].strip()
        if table_condition.upper() == table.upper():
            sql_reduce.append(rule)

    if len(sql_reduce) == 0:
        return table

    return f"(σ {' ^'.join(sql_reduce)} ({table}))"


def encontrar_elemento_mais_interno(texto):
    inicio = texto.rfind('(')
    
    if inicio == -1:
        return None
    
    fim = texto.find(')', inicio)
    
    if fim == -1:
        return None
    
    return texto[inicio + 1:fim]


def get_campos_relacionados(tableInput, camposSelect, joinClauses):
    table = ""

    if "σ" in tableInput and "π" not in tableInput:
        table = encontrar_elemento_mais_interno(tableInput)
    else:
        table = tableInput

    campos_relacionados = []

    for campo in camposSelect:
        table_compare, campo_compare = get_table_campo(campo)

        if table.upper() == table_compare.upper():
            campos_relacionados.append(campo_compare)

    for clauses in joinClauses:
        clauses = clauses.split("=")
        left = clauses[0].strip()
        right = clauses[1].strip()

        table_left, campo_left = get_table_campo(left)
        table_right, campo_right = get_table_campo(right)

        if table.upper() == table_left.upper():
            campos_relacionados.append(campo_left)

        if table.upper() == table_right.upper():
            campos_relacionados.append(campo_right)

    return campos_relacionados


def get_table_campo(elemento):
    elemento_extract = elemento.split('.')
    if len(elemento_extract) == 1:
        return elemento, None
    
    table = elemento_extract[0].strip()
    campo = elemento_extract[1].strip()

    return table, campo


def apply_reduce_campos(table, campos):

    if len(campos) == 0:
        return table
    
    tableOut = f"({table})"

    if "σ" in table:
        tableOut = table

    
    return f"(π {', '.join(campos)} {tableOut})"



def convert_sql_to_algebra(sql_query):
    global position_counter
    position_counter = 1
    # Extraindo projeções
    projections = extract_projections(sql_query)
    projection_clause = "π " + ", ".join(projections)

    # Extraindo condições
    conditions = extract_conditions(sql_query)
    conditions = conditions.replace("AND", "^")
    selection_clause = f"σ {conditions}"

    # Extraindo tabelas e joins
    tables, join_conditions = extract_tables_and_joins(sql_query)

    juncao = ""

    for index, (table, join) in enumerate(zip(tables, join_conditions)):
        tableBeforeJoin = table if len(juncao) == 0 else juncao
        tableAfterJoin = tables[index+1]

        tableBeforeJoin = apply_reduce_tuplas(tableBeforeJoin, conditions)
        tableAfterJoin = apply_reduce_tuplas(tableAfterJoin, conditions)

        campos_before = get_campos_relacionados(tableBeforeJoin, projections, join_conditions)
        campos_after = get_campos_relacionados(tableAfterJoin, projections, join_conditions)

        tableBeforeJoin = apply_reduce_campos(tableBeforeJoin, campos_before)
        tableAfterJoin = apply_reduce_campos(tableAfterJoin, campos_after)

        juncao = f"({tableBeforeJoin} |X| {join} {tableAfterJoin})"
        
    # # Montando a álgebra relacional final
    algebra_relational = f"{projection_clause}({juncao})"
    
    return algebra_relational


print( convert_sql_to_algebra("select tf.NUMERO from TELEFONE tf") )