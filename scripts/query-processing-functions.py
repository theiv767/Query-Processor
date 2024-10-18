import re

def parser(query):
    # Ex: SELECT <field> from <table> where <field> = 10

    query = query.strip()
    if len(query) == 0:
        return False

    words = query.upper().split()
    
    state = "INITIAL"
    states = {
        "INITIAL":  [r"^SELECT$"],                                  # "SELECT"   
        
        "SELECT":   [r"^\*$",    r"^\*,\s*$",   r"^[A-Z].*"],       # "*", LABEL

        "FROM":     [r"^[A-Z].*"],                                  # LABEL

        "WHERE":    [r"^\($",    r"^[A-Z].*",   r"^\d+$"],          # "(", LABEL, NUMBER

        "LABEL":    [r"^,$", r"^FROM$", r"^WHERE$"],

        ",":        [r"^\*$",    r"^[A-Z].*"]

    }


    def is_valid_word(word, state):
        for i in states[state]:
            if re.fullmatch(i, word):
                return True    
        return False

    for word in words:
        if state not in states or not is_valid_word(word, state):
            return False  # Erro de sintaxe
        
        if word in states and (word != ["LABEL"]):
            state = word
        else:
            if word[-1] == ",":
                state = ","
            else:
                state = "LABEL"
            

    return True



# Exemplo de uso ------------------------------------------------------------------------------
query1 = "SELECT *, CAST FROM customers"

print(parser(query1)) 
