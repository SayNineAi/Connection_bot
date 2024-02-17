import pandas as pd
from src.tools.utils.helper_functions import check_word, process_string
from itertools import combinations

EMAILVARIATIONS = [
    "firstname1.lastname1@domain",
    "firstname1lastname1@domain",
    "lastname1.firstname1@domain",
    "lastname1firstname1@domain",
    "firstname1.lastname0@domain",
    "firstname1lastname0@domain",
    "lastname0.firstname1@domain",
    "lastname0firstname1@domain",
    "firstname0.lastname1@domain",
    "firstname0lastname1@domain",
    "lastname1.firstname0@domain",
    "lastname1firstname0@domain",
    "firstname1-lastname1@domain",
    "lastname1-firstname1@domain",
    "firstname1_lastname1@domain",
    "lastname1_firstname1@domain",
    "firstname1@domain",
    "lastname1@domain",
    "firstname1-lastname0@domain",
    "lastname0-firstname1@domain",
    "firstname1_lastname0@domain",
    "lastname0_firstname1@domain",
    "firstname0-lastname1@domain",
    "lastname1-firstname0@domain",
    "firstname0_lastname1@domain",
    "lastname1_firstname0@domain",
    "firstname0.lastname0@domain",
    "firstname0lastname0@domain",
    "lastname0.firstname0@domain",
    "lastname0firstname0@domain",
    "firstname0-lastname0@domain",
    "firstname0_lastname0@domain",
    "lastname0-firstname0@domain",
    "lastname0_firstname0@domain",
]


def create_variant(combo, domain: str, index: int) -> str:
    firstname = combo[0]
    lastname = combo[-1]
    first = False
    second = False
    email_pattern = EMAILVARIATIONS[index]
    if "firstname1" in email_pattern:
        email_pattern = email_pattern.replace("firstname1", firstname)
        first = True
    if "lastname1" in email_pattern:
        email_pattern = email_pattern.replace("lastname1", lastname)
        second = True
    if "firstname0" in email_pattern and not first:
        email_pattern = email_pattern.replace("firstname0", firstname[0])
    if "lastname0" in email_pattern and not second:
        email_pattern = email_pattern.replace("lastname0", lastname[0])
    email_pattern = email_pattern.replace("domain", domain)
    return email_pattern.lower()


#
class EmailVariation:
    def __init__(self, data: pd.DataFrame):
        self.data: pd.DataFrame = data
        self.emails: dict = {}
        self.max_len = 0

    def create_variations(self):
        for index, row in self.data.iterrows():
            if pd.isna(row["domain"]):
                continue
            if pd.isna(row["full_name"]):
                continue
            names = check_word(row['full_name'])
            names = process_string(names)
            names = names.split()
            finish_names = []
            for name in names:
                name = check_word(name)
                name = process_string(name)
                if name:
                    finish_names.append(name)
            # print(finish_names)
            # Get all possible 2-name combinations
            email_variants = []
            domain = row["domain"]
            if len(finish_names) == 1:
                email_variants.append(f"{finish_names[0]}@{domain}")
            else:
                name_combos = combinations(finish_names, 2)
                for combo in name_combos:
                    for i in range(len(EMAILVARIATIONS)):
                        email_variants.append(
                            create_variant(
                                combo=combo,
                                domain=domain,
                                index=i,
                            )
                        )
            if len(email_variants) > self.max_len:
                self.max_len = len(email_variants)
            self.emails[index] = {"email": email_variants, "found": False, "domain": row['domain']}
        return self.emails, self.max_len


#
class EmailVariationOld:
    def __init__(self, data):
        self.data = data
        self.emails = {}

    def create_variations(self):
        for index, row in self.data.iterrows():
            if pd.isna(row["domain"]):
                continue
            if pd.isna(row["surname"]):
                continue
            if pd.isna(row["name"]):
                continue
            self.emails[index] = [
                f'{row["name"]}.{row["surname"]}@{row["domain"]}'.lower(),
                f'{row["name"]}.{row["surname"][0]}@{row["domain"]}'.lower(),
                f'{row["name"]}{row["surname"][0]}@{row["domain"]}'.lower(),
                f'{row["name"][0]}{row["surname"]}@{row["domain"]}'.lower(),
                f'{row["name"]}@{row["domain"]}'.lower(),
                f'{row["surname"]}@{row["domain"]}'.lower(),
                f'{row["name"][0]}.{row["surname"][0]}@{row["domain"]}'.lower(),
                f'{row["name"]}{row["surname"]}@{row["domain"]}'.lower(),
                f'{row["name"][0]}.{row["surname"]}@{row["domain"]}'.lower(),
            ]
        return self.emails