import os
import sys
import cloudpassage
from json2html import *

session = cloudpassage.HaloSession(sys.argv[1], sys.argv[2], api_host=sys.argv[3])
policy = cloudpassage.ConfigurationPolicy(session, endpoint_version=2)
policies = policy.list_all(template=False, retired=False)
request = cloudpassage.HttpHelper(session)

# Get all APA policies
results_table = []
for pol in policies:
    incl_string = ""
    excl_string = ""

    if pol["assignment"]:
        for excl in pol["assignment"]["excl"]:
            excl_string += f'{excl["name"]}: {excl["value"][0] if isinstance(excl["value"], list) else excl["value"]};' + " "

        for incl in pol["assignment"]["incl"]:
            incl_string += f'{incl["name"]}: {incl["value"][0] if isinstance(incl["value"], list) else incl["value"]};' + " "

    policy_response = request.get(f"/v2/policies/{pol['policy_id']}")
    policy_detail = {}
    for detail in policy_response.values():
        policy_detail = detail

    used_by = ""

    for usedby in policy_detail["used_by"]:
        used_by += f'id: {usedby["id"]}, name: {usedby["name"]};' + " "

    results_table.append({
        "Policy Name": pol["name"],
        "Status": pol["status"],
        "Target Asset Type": pol.get("target_type"),
        "Target Platform": pol["platform"],
        "Assignments": incl_string,
        "Exclusions": excl_string,
        "Used By": used_by
    })

with open("apa_policies.html", "w") as file:
    file.write(json2html.convert(json = results_table))