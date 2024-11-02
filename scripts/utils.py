# Utilitários

def get_query_vector(query):
    separators =   ["=", ">=", "<=", "<>", ",", "(", ")"]


    query = query.strip()
    words = query.upper().split()

    query_vector = []
    for word in words:

        word = word.strip()

        splited_words = [""]

        if not word in separators:
            for idx, letter in enumerate(word):
                if letter in separators:
                    if splited_words[-1] == "":
                        splited_words[-1] = letter
                    else:
                        splited_words.append(letter)

                    if len(word)-1 > idx:
                        splited_words.append("")
                        
                
                else:
                    splited_words[-1] += letter


        else:
            splited_words = [word]

        for i in splited_words:
            query_vector.append(i)

    return query_vector