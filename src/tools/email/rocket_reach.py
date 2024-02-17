#
from pprint import pprint
import requests
import pandas as pd


#
def rocket_reach_by_linkedin_url(linkedin_profile_url):
    url = "https://api.rocketreach.co/v2/api/person/lookup"
    api_key = "12321abkc58718cccadb979ac48799a024b87998"
    headers = {"Api-Key": api_key}
    params = {"li_url": linkedin_profile_url}
    response = requests.get(url, headers=headers, params=params)
    return response.json()

#print(rocket_reach_by_linkedin_url("https://www.linkedin.com/in/charlotte-mcintosh-4545a7a1"))
#
def process_data(data, domain):
    try:
        for email_data in data["emails"]:
            if domain in email_data["email"]:
                if "A" in email_data["grade"]:
                    return email_data["email"]
        for email_data in data["emails"]:
            if email_data["email"] == data["current_work_email"]:
                if "A" in email_data["grade"]:
                    return email_data["email"]
        for email_data in data["emails"]:
            if "A" in email_data["grade"]:
                return email_data["email"]
        return False
    except:
        return False


#
def get_true_rocket_reach():
    df = pd.read_csv("emails.csv")

    for index, row in df.iterrows():
        if row["email"] in ["A", "A-"]:
            url = row["LinkedIn"]
            domain = row["Domain"]
            ema = rocket_reach_by_linkedin_url(url)
            pprint(ema["emails"])
            email = process_data(ema, domain)

            if email:
                df.at[index, "email"] = email
            else:
                print(f"No email found for {url}")
                df.at[index, "email"] = False
    df.to_csv("emails.csv", index=False)
