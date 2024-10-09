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
        
        "SELECT":   [r"^\*$",    r"^[A-Z].*"],                      # "*", LABEL

        "FROM":     [r"^[A-Z].*"],                                  # LABEL

        "WHERE":    [r"^\($",     r"^[A-Z].*",     r"^\d+$"],       # "(", LABEL, NUMBER

        "LABEL":    [r"^SELECT$", r"^FROM$", r"^WHERE$"]

    }


    def is_valid_word(word, state):
        for i in states[state]:
            if re.fullmatch(i, word):
                return True    
        return False

    for word in words:
        if state not in states or not is_valid_word(word, state):
            return False  # Erro de sintaxe
        state = word

    return True



# Exemplo de uso ------------------------------------------------------------------------------
query1 = "SELECT * FROM customers WHERE country = 'USA'"

print(parser(query1)) 