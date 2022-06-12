from levenshtein_automata.automata import AFN


def create_levenshtein_automata(string: str, distance: int):
    """
    Cria um automato de levenshtein para `string` com distância `distance`.
    """
    afn = AFN(start_state=(0, 0))

    for chars_processed, char in enumerate(string):
        for total_errors in range(distance + 1):
            # Caracter correto - Transição horizontal
            afn.add_transition((chars_processed, total_errors), char, (chars_processed + 1, total_errors))
            if total_errors < distance:
                # Inserção - Transição vertical
                afn.add_transition((chars_processed, total_errors), AFN.ANY, (chars_processed, total_errors + 1))
                # Remoção - Transição diagonal
                afn.add_transition(
                    (chars_processed, total_errors), AFN.EPSILON, (chars_processed + 1, total_errors + 1)
                )
                # Substituição - Transição diagonal
                afn.add_transition((chars_processed, total_errors), AFN.ANY, (chars_processed + 1, total_errors + 1))

    # Conecta as transições finais
    for total_errors in range(distance + 1):
        if total_errors < distance:
            afn.add_transition((len(string), total_errors), AFN.ANY, (len(string), total_errors + 1))

        afn.add_final_state((len(string), total_errors))

    return afn


def get_valid_strings(string: str, distance: int, haystack: list):
    """
    Cria um automato de levenshtein para `string` com tamanho `distance` e retorna todas as strings validas que
    estão em `haystack`.
    """
    automata = create_levenshtein_automata(string, distance)
    return [(index, item) for index, item in enumerate(haystack) if automata.validate_string(item)]


def replace_strings(strings: list[str], *, distance: int):
    """
    Cria um automato de levenshtein para `string` com tamanho `distance`. Procura por strings válidas em `strings` e
    substitui todas as ocorrencias das strings válidas em `strings` por uma string válida arbitrária.
    """
    seen = []
    for i, string in enumerate(strings):
        if (i, string) not in seen:
            valid_strings = get_valid_strings(string, distance, strings)

            for j, _ in valid_strings:
                strings[j] = string
            seen.extend(valid_strings)

    return strings
