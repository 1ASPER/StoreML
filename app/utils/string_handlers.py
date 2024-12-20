import re

def get_year_of_exp(experience_str):
    
    if "без опыта" in experience_str.lower():
        return 0

    match = re.search(r"(\d+)-(\d+)", experience_str)
    if match:
        return int(match.group(1))
    
    match_more_than = re.search(r"более (\d+)", experience_str)
    if match_more_than:
        return int(match_more_than.group(1)) 

    if "лет" in experience_str:
        return int(re.search(r"\d+", experience_str).group(0))

    return None


def parse_salary(salary_str):
    if not salary_str:
        return {
            "salary_from": None,
            "salary_to": None,
            "currency": None,
            "is_net": None  # True - "на руки", False - "до вычета налогов"
        }

    salary_str = salary_str.text

    salary_str = salary_str.replace("\u202f", "").strip()

    is_net = "на руки" in salary_str
    is_gross = "до вычета налогов" in salary_str

    currency_match = re.search(r"[\₽\$€₸Br]", salary_str)
    currency = currency_match.group(0) if currency_match else None

    range_match = re.search(r"(\d+)[^\d]*(\d+)?", salary_str)
    if "от" in salary_str:
        salary_from = int(range_match.group(1))
        salary_to = None
    elif "–" in salary_str or "—" in salary_str:
        salary_from = int(range_match.group(1))
        salary_to = int(range_match.group(2))
    else:
        salary_from = salary_to = int(range_match.group(1))

    if salary_to is None:
        salary_to = salary_from

    return {
        "salary_from": salary_from,
        "salary_to": salary_to,
        "currency": currency,
        "is_net": is_net  # True - "на руки", False - "до вычета налогов"
    }