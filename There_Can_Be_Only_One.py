import requests

token: str = '2619421814940190'
api_url = 'https://superheroapi.com/api/'


# invalid_name_resp = {'response': 'error', 'error': 'character with given name not found'}

def get_intel_by_name(name):
    char_int = 0
    try:
        char_search = requests.get(api_url + token + '/search/' + name)
        char_obj = char_search.json()
        char_int = char_obj['results'][0]['powerstats']['intelligence']
    except KeyError:
        char_obj = char_search.json()
        print(char_obj['error'])
    return char_int


def get_intel_for_several():
    nmb_chars = int(input('Введите число героев для сравнения: '))
    names = []
    for i in range(0, nmb_chars):
        item = str(input('Введите имя героя для сравнения: '))
        names.append(item)
    char_vals = {}
    for name in names:
        char_int = int(get_intel_by_name(name))
        char_vals[name] = char_int
    return char_vals


def find_the_smartest(int_vals):
    max_int = 0
    max_name = ''
    for val in int_vals.items():
        if val[1] >= max_int:
            max_int = val[1]
            max_name = val[0]
    return max_name


int_dict = get_intel_for_several()
print(find_the_smartest(int_dict))
