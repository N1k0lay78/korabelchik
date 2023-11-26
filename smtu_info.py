faculty_short = {
    "fcpt": "ФЦПТ",
    "fmp": "ФМП",
    "fkio": "ФКиО",
    "fkeia": "ФКЭиА",
    "feigo": "ФЕНГО",
    "ief": "ИЭФ",
}

faculty_long = {
    "fcpt": "Факультет цифровых промышленных технологий",
    "fmp": "Факультет морского приборостроения",
    "fkio": "Факультет кораблестроения и океанотехники",
    "fkeia": "Факультет корабельной энергетики и автоматики",
    "feigo": "Факультет естественнонаучного и гуманитарного образования",
    "ief": "Инженерно-экономический факультет",
}

faculty_is_technical = {
    "fcpt": True,
    "fmp": True,
    "fkio": True,
    "fkeia": True,
    "feigo": False,
    "ief": False,
}

faculty_id = {
    "fcpt": 1,
    "fmp": 2,
    "fkio": 3,
    "fkeia": 4,
    "feigo": 5,
    "ief": 6,
}

faculty_keys = ["fcpt", "fmp", "fkio", "fkeia", "feigo", "ief"]
faculty_longs_keys = [
    "Факультет цифровых промышленных технологий",
    "Факультет морского приборостроения",
    "Факультет кораблестроения и океанотехники",
    "Факультет корабельной энергетики и автоматики",
    "Факультет естественнонаучного и гуманитарного образования",
    "Инженерно-экономический факультет",
]

def get_faculties():
    return faculty_keys


def get_faculty(id):
    return faculty_keys[id - 1]


def get_faculty_longs_keys(id):
    return faculty_longs_keys[id - 1]


def get_faculty_short(faculty):
    return faculty_short[faculty]


def get_faculty_long(faculty):
    return faculty_long[faculty]


def get_faculty_is_technical(faculty):
    return faculty_is_technical[faculty]


def get_faculty_id(faculty):
    return faculty_id[faculty]
