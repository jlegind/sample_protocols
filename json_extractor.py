def extract_values(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            print('is dict')
            for k, v in obj.items():
                print('in if loop')
                print(k, ':', v)
                if k == key:
                    print('IN append str ')
                    arr.append(v)

                elif isinstance(v, (dict, list)):
                    print('in dict/list loop')
                    extract(v, arr, key)
        elif isinstance(obj, list):
            print('in list loop')
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results