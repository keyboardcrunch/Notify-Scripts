from __future__ import unicode_literals

# Settings
teams_hook = "https://outlook.office.com/webhook/"
dashboard = "https://mydashboard/"

"""
Requirements:
    pymsteams module installed
    python2 or 3

Notes:
    --ops is for sending general messages
    --threat is for sending a title and a python dict or json string (See example 2 below). The dict will be printed in order.

Examples:
    ./teams_notify.py --ops "Message title" "General message to send to the channel."

    ./teams_notify.py --threat "Threat message title" "{'ThreatName': 'Mimikatz','Hostname':'win10pro'}"

"""

def ThreatNotify(title, payload):
    import json
    from collections import OrderedDict

    # Clean json string decode of the payload into an ordered dict for the teams fact card
    jp = json.JSONDecoder(object_pairs_hook=OrderedDict).decode(payload)

    # Build Teams card
    teams = pymsteams.connectorcard(teams_hook)
    teams.title(title)
    teams.summary("A new threat event has been raised")
    details = pymsteams.cardsection()
    details.title("Threat Details:")
    for n, v in jp.items():
        details.addFact(n, v)
    teams.addLinkButton("Open Dashboard", dashboard)
    teams.addSection(details)
    teams.send()
   

def OpsNotify(title, message):
    teams = pymsteams.connectorcard(teams_hook)
    teams.title(title)
    teams.text(message)
    teams.send()


if __name__ in "__main__":
    import argparse
    try:
        import pymsteams
    except:
        print("Error importing pymsteams")
        quit()

    parser = argparse.ArgumentParser(description="MS Teams notification sender.")
    parser.add_argument('--threat', action="store_true", help="Send a threat notification with a message title and payload")
    parser.add_argument('--ops', action="store_true", help="Send a operational notification with a message title and body")
    parser.add_argument('args', nargs=2, help="Requires two arguments, 'title' and 'message' or a python dict/json payload '{'hostname': 'box1', 'timestamp': 'xxxx'}' ")
    result = parser.parse_args()

    if result.threat:
        ThreatNotify(result.args[0], result.args[1])
    elif result.ops:
        OpsNotify(result.args[0], result.args[1])
    else:
        print("Mistakes have been made.")
