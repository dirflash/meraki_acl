"""Proof of concept that updates the ACLs on a Meraki MS Switch from a CSV file

    This script backs up the current ACLs and then updates them with ACLs from:
        ./acl_push/acl/push.csv.
    The CSV file should have the following headers:
        Comment,Policy,IP Version,Protocol,Source CIDR,Source Port,Destination CIDR,Destination Port,Vlan

    Questions about the Network Switch ACL API:
    https://developer.cisco.com/meraki/api-v1/update-network-switch-access-control-lists/

    Questions about the Meraki Python SDK:
    https://github.com/meraki/dashboard-api-python/tree/main
"""

import datetime
import os

import meraki  # pylint: disable=import-error
from tabulate import tabulate

from utils import preferences as pref

API_KEY = pref.MERAKI_API_KEY
NETWORK_NAME = pref.NETWORK_NAME  # Replace with the name of your network
ACL_PUSH_DIR = "./acl_push"

new_acls: dict[str, list] = {"rules": []}

dashboard = meraki.DashboardAPI(API_KEY)

# Get Org ID
get_org_id = dashboard.organizations.getOrganizations()
org_id = get_org_id[0]["id"]

# Get Network IDs
get_network_id = dashboard.organizations.getOrganizationNetworks(org_id)
network_dict = {item["id"]: item["name"] for item in get_network_id}

if NETWORK_NAME in network_dict.values():
    network_id = next(id for id, name in network_dict.items() if name == NETWORK_NAME)
    print(f"Network ID for {NETWORK_NAME} is {network_id} in Org ID {org_id}")

    # Get Switch ACL
    get_switch_acls = dashboard.switch.getNetworkSwitchAccessControlLists(network_id)

    # get current date and time with format yyyy-mm-dd_hh-mm-ss
    now = datetime.datetime.now()
    date_time = now.strftime("%Y-%m-%d_%H-%M-%S")

    # create filename for backup
    acl_backup_filename = f"./acl_backup/{NETWORK_NAME}_acls_backup_{date_time}.json"

    # Create json file with ACLs
    try:
        with open(acl_backup_filename, "w", encoding="UTF-8") as outfile:
            print(f"Writing ACLs to {acl_backup_filename}")
            outfile.write(str(get_switch_acls))
    except IOError as e:
        print(e)

    # Create csv file for ACLs
    ACL_CSV_FILENAME = f"./acl_csv_backup/{NETWORK_NAME}_acls_backup_{date_time}.csv"
    ACL_CSV_HEADER1 = "Comment,Policy,IP Version,Protocol,Source CIDR,Source Port,"
    ACL_CSV_HEADER2 = "Destination CIDR,Destination Port,Vlan\n"
    ACL_CSV_HEADER = ACL_CSV_HEADER1 + ACL_CSV_HEADER2

    try:
        with open(
            ACL_CSV_FILENAME,
            "w",
            encoding="UTF-8",
        ) as outfile:
            outfile.write(ACL_CSV_HEADER)
    except IOError as e:
        print(e)

    rules = get_switch_acls["rules"]

    acl_table = []

    for acl in rules:
        acl_table.append(
            [
                acl["comment"],
                acl["policy"],
                acl["ipVersion"],
                acl["protocol"],
                acl["srcCidr"],
                acl["srcPort"],
                acl["dstCidr"],
                acl["dstPort"],
                acl["vlan"],
            ]
        )

        acl_csv_line = (
            f'{acl["comment"]},{acl["policy"]},{acl["ipVersion"]},{acl["protocol"]},'
            f'{acl["srcCidr"]},{acl["srcPort"]},{acl["dstCidr"]},{acl["dstPort"]},'
            f'{acl["vlan"]}\n'
        )

        # Append csv file for ACLs
        try:
            with open(
                ACL_CSV_FILENAME,
                "a",
                encoding="UTF-8",
            ) as outfile:
                outfile.write(acl_csv_line)
        except IOError as e:
            print(e)

    print(
        tabulate(
            acl_table,
            headers=[
                "Comment",
                "Policy",
                "IP Version",
                "Protocol",
                "Source CIDR",
                "Source Port",
                "Destination CIDR",
                "Destination Port",
                "Vlan",
            ],
        )
    )
    print("\n")

print("Backup files created.\n")

# Check if acl_push file exists in ./acl_push
acl_push_files = os.listdir(ACL_PUSH_DIR)
# Number of files in acl_push_files
print(f"Number of files in {ACL_PUSH_DIR}: {len(acl_push_files)}")
if acl_push_files:
    print(f"Files in {ACL_PUSH_DIR}:")
    for file in acl_push_files:
        if file == "acl_push.csv":
            print(f"  {file} file exists.")
            # Read acl_push.csv file
            with open(f"{ACL_PUSH_DIR}/{file}", "r", encoding="UTF-8") as infile:
                acl_push_csv = infile.read()
                # delete header line
                acl_push_csv = acl_push_csv.splitlines()[1:]
                acl_push_csv = "\n".join(acl_push_csv)
            for line in acl_push_csv.splitlines():
                acl_list = []
                # add each item delimited by ',' in line to a list
                acl_list.append(line.split(","))
                # convert acl_list to dict
                acl_dict = dict(
                    zip(
                        [
                            "comment",
                            "policy",
                            "ipVersion",
                            "protocol",
                            "srcCidr",
                            "srcPort",
                            "dstCidr",
                            "dstPort",
                            "vlan",
                        ],
                        acl_list[0],
                    )
                )
                if acl_dict["comment"] != "Default rule":
                    new_acls["rules"].append(acl_dict)
            # Write acl_push.json file
            with open("./json_push/acl_push.json", "w", encoding="UTF-8") as outfile:
                outfile.write(str(new_acls))
        else:
            print(f"  {file} file does not exist.")
else:
    print(f"No files in {ACL_PUSH_DIR}")

if os.path.exists("./acl_push/acl_push.csv"):
    print("Ready to go.")

# Push ACLs to network
try:
    post_switch_acls = dashboard.switch.updateNetworkSwitchAccessControlLists(
        network_id, new_acls["rules"]
    )
except meraki.exceptions.APIError as e:
    print(e)

print(post_switch_acls)
