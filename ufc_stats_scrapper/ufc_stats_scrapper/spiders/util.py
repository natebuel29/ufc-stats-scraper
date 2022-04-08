def normalize_results(results):
    normalize_list = list(map(str.strip, results))
    while "" in normalize_list:
        normalize_list.remove("")
    return normalize_list
