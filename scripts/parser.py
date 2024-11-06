# VALIDAÇÃO DE SINTAXE

import re
import json
from utils import *


storage_tbls = json.load(open('scripts/tables.json'))
#-----------------------------------------------------------------------------

def get_num_match(word):
    count = sum(
        1 for subdict in storage_tbls.values()
        if isinstance(subdict, dict) and word.upper() in (key.upper() for key in subdict.keys())
    )

    return count


def is_valid_where(qry_where, alias):
    if qry_where  == "":
        return True, "ok"
    
    qry_where = get_query_vector(qry_where)

    
    operators = {
        "relational_operators"  :   {
            "characters" :["=", ">=", "<=", "<>", ">", "<", "="],
            "acepted_types" : ["INT", "FLOAT", "STRING", "DATE"],
            "return_type" : ["BOOL"]
        },

        "arithmetic_operators"   :   {
            "characters" : ["+", "-", "*", "/"],
            "acepted_types" : ["INT", "FLOAT", "STRING", "DATE"],
            "return_type" : ["INT", "FLOAT", "STRING", "DATE"]
        },

        "Logical_operators"    :   {
            "characters" : ["AND"],
            "acepted_types" : ["BOOL"],
            "return_type" : ["BOOL"]
        }

    }



    current_types       =   []
    current_operator    =   []


    for idx, word in enumerate(qry_where):

        if word == "(":
            continue

        if word == ")":
            acept_operator = current_types[-1] in operators[current_operator[-1]]["acepted_types"]
            acept_types = current_types[-1] == current_types[-2]
            if acept_operator and acept_types:
                if current_operator[-1] != "arithmetic_operators":
                    current_types.pop()
                    current_types.append(operators[current_operator[-1]]["return_type"])
                current_operator.pop()
            else:
                return False, f"Objeto {word} possui um tipo inválido!!!"   

        # operador -------------------------------------
        for operator_type in operators.keys():
            if word in operators[operator_type]["characters"]:
                current_operator.append(operator_type)
                continue    

        # tabelas.coluna -------------------------------

        if re.fullmatch(r"^[A-Z].*", word) or re.fullmatch(r"^\d+$", word):
            colum_type = ""
            

            aux_test_float = False
            aux_word_splited = word.split(".")
            if len(aux_word_splited) > 1:
                if re.fullmatch(r"^\d+$", aux_word_splited[0]):
                    colum_type = "FLOAT"

            if re.fullmatch(r"^\d+$", word):
                if colum_type == "":
                    colum_type = "INT"
                
            else:
                if "." in word:
                    tbl_alias = word.split(".")[0]
                    tbl_colum = word.split(".")[1]

                    # ---------------
                    # validando o alias
                    table_name = ""
                    exist_alias = False
                    for i in alias:
                        if i[0].upper() == tbl_alias.upper():
                            exist_alias = True
                            table_name = i[1]
                            table_columns_upper = {k.upper() for k in storage_tbls[i[1]].keys()}
                            if not tbl_colum.upper() in table_columns_upper:
                                return False, f"Coluna '{tbl_colum}' não encontrada na tabela {i[1]}!!!"
                            break
                    
                    if not exist_alias:
                        return False, f"Alias '{tbl_alias}' não definido na consulta!!!"

                    #--------------
                    # verificação de tipagem
                    colum_type = storage_tbls[table_name][tbl_colum]

                    if "VARCHAR(" in colum_type:
                        colum_type = "STRING"
                    elif "TINYINT" in colum_type:
                        colum_type = "INT"
                    elif "DATE" in colum_type:
                        colum_type = "DATE"
                    elif "DECIMAL(" in colum_type:
                        colum_type = "FLOAT"
                        
                else:
                    tbl_colum = word

                    num_match = 0

                    table_name = ""
                    for i in alias:
                        if tbl_colum in storage_tbls[1].keys():
                            table_name = i[1]
                            num_match += 1


                    if num_match > 1:
                        return False, f"Tabela da coluna '{tbl_colum}' não foi especificada!!!" 
                    elif num_match < 1:
                        return False, f"Tabela da coluna '{tbl_colum}' não existe entre as tabelas!!!" 
                    

                    colum_type = storage_tbls[table_name][tbl_colum]

                    if "VARCHAR(" in colum_type:
                        colum_type = "STRING"
                    elif "TINYINT" in colum_type:
                        colum_type = "INT"
                    elif "DATE" in colum_type:
                        colum_type = "DATE"
                    elif "DECIMAL(" in colum_type:
                        colum_type = "FLOAT"


            is_last_parenthesis = False
            if idx-1 >= 0:
                if qry_where[idx-1] == "(":
                    is_last_parenthesis = True
            
            if len(current_types) == 0 or is_last_parenthesis:
                current_types.append(colum_type)
            else:
                acept_operator = colum_type in operators[current_operator[-1]]["acepted_types"]
                acept_types = current_types[-1] == colum_type
                if acept_operator and acept_types:
                    if current_operator[-1] != "arithmetic_operators":
                        current_types.pop()
                        current_types.append(operators[current_operator[-1]]["return_type"])
                    current_operator.pop()
                else:
                    return False, f"Objeto {word} possui um tipo inválido!!!"

            continue
    
    if len(current_types)!= 1 and "BOOL" != current_types[-1]:
        return False, "Where espera um booleano!!!"
    
    return True, "ok"



def is_valid_rels(query):
    query = query.upper()
    storage_tbls = json.load(open('scripts/tables.json'))

    print(query)

    qry_select = query.split("FROM")[0]
    print(qry_select)
    qry_tables = "FROM"+query.split("FROM")[1]
    
    qry_where = ""
    if " WHERE " in query:
        qry_where = qry_tables.split("WHERE")[1]
        qry_tables = qry_tables.split("WHERE")[0]

    qry_select  = qry_select.strip()
    qry_tables  = qry_tables.strip()
    qry_where   = qry_where.strip()

    alias = []
    
    # Regex para capturar o padrão "FROM <tabela> <alias>" e "JOIN <tabela> <alias>"
    #pattern = r"\b(?:FROM|JOIN)\s+(\w+)\s+(\w+)"
    #matches = re.findall(pattern, qry_tables, re.IGNORECASE)
    
    # alias é uma tabela que, em cada posição, guarda (alias, tabela_correspondente)
    #alias = [(alias, table) for table, alias in matches]

    pattern = r"\b(?:FROM|JOIN)\s+(\w+)(?:\s+(\w+))?"
    matches = re.findall(pattern, qry_tables, re.IGNORECASE)

    # Constrói a lista de alias, usando o próprio nome da tabela como alias quando ele não é especificado
    alias = [(alias if alias else table, table) for table, alias in matches]



    for i in alias:
        if not i[1].upper() in {k.upper() for k in storage_tbls.keys()}:
            return False, f"Tabela '{i[1]}' não encontrada!!!"


    separators =   ["=", ">=", "<=", "<>", ",", "(", ")", "*"]


    qry_select = get_query_vector(qry_select)
    qry_select = qry_select[1:]
    for word in qry_select:
        if word in separators:
            continue

        if re.fullmatch(r"^[A-Z].*", word):
            if "." in word:
                tbl_alias = word.split(".")[0]
                tbl_colum = word.split(".")[1]

                exist_alias = False
                for i in alias:
                    if i[0].upper() == tbl_alias.upper():
                        exist_alias = True
                        table_columns_upper = {k.upper() for k in storage_tbls[i[1]].keys()}
                        if not tbl_colum.upper() in table_columns_upper:
                            return False, f"Coluna '{tbl_colum}' não encontrada na tabela {i[1]}!!!"
                        
                if not exist_alias:
                    return False, f"Alias '{tbl_alias}' não definido na consulta!!!"
                
            else:
                tbl_colum = word
                num_match = get_num_match(word)

                if num_match > 1:
                    return False, f"Tabela da coluna '{tbl_colum}' não foi especificada!!!"  



    # ADICIONAR VALIDAÇÃO DE WHERE ---------------------------------------
    if qry_where != "":
        valid_where, msg = is_valid_where(qry_where, alias)            
        if not valid_where:
            return valid_where, msg



    return True, "ok"




        
        

    



    



def parser(query):
    # Ex: SELECT <field> from <table> where <field> = 10

    select_regex = r"SELECT\s+(.*?)\s+FROM\s+(\w+)(?:\s+JOIN\s+(\w+)\s+ON\s+.*?)*"
    where_regex = r"WHERE\s+(.*)"
    
    match = re.search(select_regex, query, re.IGNORECASE)
    if not match:
        return False, "Teste inicial"

    query = query.strip()
    if len(query) == 0:
        return False

    words = get_query_vector(query)
    
    state = "INITIAL"
    states = {
        "INITIAL":  {
            "MIDDLE":   [],
            "END":      [r"^SELECT$"]

        },
        
        "SELECT":   {
            "MIDDLE":   [r"^,$"],  
            "END":      [r"^\*$", r"^[A-Z].*"]                       
        },

        "FROM":     {
            "MIDDLE":   [],
            "END":      [r"^[A-Z].*"]           
        },

        "WHERE":    {
            "MIDDLE":   [r"^=$", r"^>=$", r"^<=$", r"^>$", r"^<$", r"^AND$", r"^OR$", r"^\($"],
            "END":      [r"^[A-Z].*", r"^\d+$", r"^\)$"] 
        },

        "JOIN":     {
            "MIDDLE":   [],
            "END":      [r"^[A-Z].*"]           
        },

        "ON":       {
            "MIDDLE":   [r"^=$", r"^>=$", r"^<=$", r"^>$", r"^<$", r"^AND$", r"^OR$"],
            "END":      [r"^[A-Z].*", r"^\d+$"] 
        }
    }


    def is_valid_word(word, state):
        for i in states[state]["MIDDLE"]:
            if re.fullmatch(i, word):
                return True, False
        
        for i in states[state]["END"]:
            if re.fullmatch(i, word):
                return True, True    


        return False, False


    num_open_parenthesis = 0
    num_comparations = 0

    for idx_word, word in enumerate(words):
        if words[idx_word] in list(states.keys()):
            state = word
            continue
        

        if word == "(":
            num_open_parenthesis += 1
        if word == ")":
            if num_open_parenthesis < 1:
                return False, f"Parêntesis aberto incorretamente!!!"
            num_open_parenthesis -= 1


        valid_word, end_word = is_valid_word(word, state)
        if state not in list(states.keys()) or not valid_word:
            return False, f"palavra '{word}' inválida!!!"  # Erro de sintaxe



        #-----------------------------------------------------------
        # testando palavra anterior
        if words[idx_word-1] in list(states.keys()):
            state_prev_word = True
            end_prev_word = False
        else:
            state_prev_word = False
            _, end_prev_word = is_valid_word(words[idx_word-1], state)

        
        comparators =   ["=", ">=", "<=", "<>"]
        operators   =   ["AND", "OR"]
        if end_word:
            if end_prev_word:
                if not word == ")":
                    if not state in ["FROM", "JOIN"]:
                        return False, f"A palavra {words[idx_word-1]} não espera {word}"
                    else:
                        if words[idx_word-2] != state:
                            return False, f"A palavra {words[idx_word-1]} não espera {word}"            
            
            if words[idx_word-1] in comparators:
                num_comparations -= 1      
        else:
            if not end_prev_word or state_prev_word:
                
                # tratando casos específicos de "("
                if not (state_prev_word and word == "("):
                    if not (words[idx_word-1] in operators and word == "("):
                        return False, f"A palavra {words[idx_word-1]} não espera {word}"
            
            if word in comparators:
                num_comparations += 1        


        #---------------------------------------------------------------------------------------------------
        # Testa se está finalizando a consulta ou o estado
        if (idx_word + 1 >= len(words))  or  ( words[idx_word+1] in list(states.keys()) ):
            if not end_word:
                return False, f"{state} não pode ser terminado com {word}!!!"
            else:
                if num_comparations >= 1:
                    return False, f"Erro de comparação no {state}!!!"
                pass

            if num_open_parenthesis != 0:
                return False, f"Parêntesis ficaram abertos!!!"


    valid_rels, msg_rels = is_valid_rels(query)
    if not valid_rels:
        return False, msg_rels
    

    return True, "Sintax válida!"

print( parser("select ed.IDENDERECO, ed.BAIRRO from ENDERECO ed where ed.IDENDERECO = 1") )