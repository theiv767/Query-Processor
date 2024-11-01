# VALIDAÇÃO DE SINTAXE

import re

def parser(query):
    # Ex: SELECT <field> from <table> where <field> = 10

    query = query.strip()
    if len(query) == 0:
        return False

    words = query.upper().split()
    
    state = "INITIAL"
    states = {
        "INITIAL":  {
            "MIDDLE":   [],
            "END":      [r"^SELECT$"]

        },
        
        "SELECT":   {
            "MIDDLE":   [r"^,$", r"^[A-Z]+,$", r"^\*,$"],  
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

    print(words)
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
         

    return True, "Sintax válida!"


