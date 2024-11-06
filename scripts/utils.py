# Utilitários
import re


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


def remove_excess_parentheses(query, paren, excess):
    result = []
    count_removed = 0
    for char in query:
        if char == paren and count_removed < excess:
            count_removed += 1
            continue
        result.append(char)
    
    return ''.join(result)


def balance_parentheses(query):
    open_count = query.count("(")
    close_count = query.count(")")

    if open_count > close_count:
        excess_open = open_count - close_count
        query = remove_excess_parentheses(query, "(", excess_open)

    elif close_count > open_count:
        excess_close = close_count - open_count
        query = remove_excess_parentheses(query, ")", excess_close)
    if query == "":
        return None
    
    return query

def find_last_operation_occorency(expression, symbol):
    last_occorency_symbol = expression.rfind(symbol)

    if last_occorency_symbol == -1:
        return None, None, None
    
    expression_right = expression[last_occorency_symbol:]
    first_open_paren = expression_right.find("(")
    first_close_paren = expression_right.find(")")

    if first_open_paren == -1:
        termination_right = first_close_paren
    elif first_close_paren == -1:
        termination_right = first_open_paren
    else:
        termination_right = min(first_open_paren, first_close_paren)

    expression_main = balance_parentheses(expression_right[:termination_right].strip())

    expression_left = balance_parentheses(expression[:last_occorency_symbol].strip())
    expression_right = balance_parentheses(expression_right[termination_right:].strip())

    return expression_left, expression_main, expression_right

def split_expression(expression):
    left, main, right = find_last_operation_occorency(expression, "|X|")
    if main is not None:
        return left, main, right
    left, main, right = find_last_operation_occorency(expression, "π")
    if main is not None:
        return left, main, right
    left, main, right = find_last_operation_occorency(expression, "σ")
    if main is not None:
        return left, main, right
    main = expression[1:len(expression)-1]
    return None, main, None


def replace_sql_keywords(string):
    string = string.replace(';', "")
    keywords = ['select', 'from', 'join', 'on', 'where', 'and']
    
    for keyword in keywords:
        string = re.sub(rf'\b{keyword}\b', keyword.upper(), string, flags=re.IGNORECASE)

    string = string.replace('\n', " ")
    return string

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.pos = None

    def __repr__(self):
        return str(self.value)