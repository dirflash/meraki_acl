# Meraki MS ACL

This is a proof of concept that updates the ACLs on a Meraki MS Switch from a CSV file. This script backs up the current ACLs and then updates them with ACLs from a CSV file located at ./acl_push/acl/push.csv.

- Technology stack: Python and the Meraki SDK.
- Status: Beta. I wrote this script in a few hours to share with a customer an example of what could be accomplished with the Meraki API.

## Installation

Clone the repo

```bash
git clone https://github.com/dirflash/meraki_acl.git
```

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

Update the acl_push.csv file in the acl_push folder with the access control entries that should be pushed to your network.

Run the Python Script

```python3 meracl.py

```
