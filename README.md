# Meraki MS ACL

This is a proof of concept that updates the ACLs on a Meraki MS Switch from a CSV file. This script backs up the current ACLs and then updates them with ACLs from a CSV file located at ./acl_push/acl/push.csv.

- Technology stack: Python and the Meraki SDK.
- Status: Beta. I wrote this script in a few hours to share with a customer an example of what could be accomplished with the Meraki API.

## Installation

Clone the repo

Create a 'meraki_acl' folder on your machine.

Download the repo, using either the git method, or the non-get method described below.

### Using git

Download and launch ![git](https://git-scm.com/downloads)
Using git, navigate to the 'meraki_acl' folder you created on your machine.
Clone the project, using the following command.

```bash
git clone https://github.com/dirflash/meraki_acl.git
```

### Non-git method - Download the repo from GitHub

In the repo, click on 'Code' and 'Download Zip'.

![](https://github.com/dirflash/meraki_acl/assets/10964629/fe7bfc15-fe76-4f52-9ffa-1ef41c9f6af3)

Extract the zip into the 'meraki_acl' folder on your machine

Go to your project folder

```bash
cd meraki_acl
```

Set up a Python venv
First make sure that you have Python 3 installed on your machine. We will then be using venv to create an isolated environment with only the necessary packages.

Install virtualenv via pip

```bash
pip install virtualenv
```

Create the venv

```bash
python3 -m venv .venv
```

Activate your venv

Windows machines

```bash
source .venv/Scripts/activate
```

Non-Windows machines

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

Create a preferences.py file in the utils folder. Add your Meraki dashboard API key and the Network Name to receive the updated ACLs.

![preferences.py](https://github.com/dirflash/meraki_acl/assets/10964629/a08b5dcb-0134-49fd-8818-1880433e4e1b)

Update the acl_push.csv file in the acl_push folder with the access control entries that should be pushed to your network. An example
of this file is found at acl_push/acl_push.csv.

Options for each entry:

- Policy (required) = Deny or Allow
- IP Version (required) = Any, IPv4, or IPv6
- Protocol (required) = TCP, UDP, or Any
- Source (required) = CIDR formatted IP address or subnet, or Any
- Scr port (required) = port number or Any
- Destination (required) = CIDR formatted IP address or subnet, or Any
- Dst port (required) = port number or Any
- Vlan (required) = Vlan number or Any
- Comment = Freeform description of the ACL entry

Run the Python Script

Windows machines

```bash
python3 meracl
```

Non-Windows machines

```bash
python3 meracl.py
```

## Additional information

Meraki Network Switch ACL API documentation:
https://developer.cisco.com/meraki/api-v1/update-network-switch-access-control-lists/

Meraki Python SDK documentation:
https://github.com/meraki/dashboard-api-python/tree/main
