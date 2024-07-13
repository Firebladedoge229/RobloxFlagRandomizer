import re
import sys
import random
import requests
import argparse
from json import dumps as json
from colorama import just_fix_windows_console

just_fix_windows_console()

regex = r"\[.*?\]\s*"

PCDesktopClient = "https://clientsettings.roblox.com/v2/settings/application/PCDesktopClient"
FVariables = "https://raw.githubusercontent.com/MaximumADHD/Roblox-Client-Tracker/roblox/FVariables.txt"

def getAmount(text, type):
    while True:
        lines = input("\033[38;2;52;235;143m" + text + ": \033[0m")
        if type == "text":
            try:
                lines = lines
                return lines
            except Exception:
                print("Invalid Text")
        elif type == "int":
            try:
                lines = round(int(lines))
                return lines
            except Exception:
                print("Invalid Integer")

def getArguments():
    parser = argparse.ArgumentParser(description="funny little random flag generator")
    parser.add_argument("--min", dest="minimum", type=int, help="minimum flag integer")
    parser.add_argument("--max", dest="maximum", type=int, help="maximum flag integer")
    parser.add_argument("--text", dest="flagText", type=str, help="flag text")
    parser.add_argument("--flags", dest="flagInt", type=int, help="flags to generate")
    return parser.parse_args()

arguments = getArguments()

if not all(vars(arguments).values()):
    minimum = arguments.minimum or getAmount("minimum for flag", "int")
    maximum = arguments.maximum or getAmount("maximum for flag", "int")
    flagText = arguments.flagText or getAmount("text for flag", "text")
    flagInt = arguments.flagInt or getAmount("flags to generate", "int")
else:
    minimum = arguments.minimum
    maximum = arguments.maximum
    flagText = arguments.flagText
    flagInt = arguments.flagInt

dictionary = {}
PCDesktopClient = requests.get(PCDesktopClient).json()["applicationSettings"]
FVariables = requests.get(FVariables).text.split("\n")

dictionary.update(PCDesktopClient)

dictionary = list(dictionary.items())
dictionary = dict(random.sample(dictionary, flagInt))

for line in dictionary:
    if line.strip():
        global flag
        flag = line
        if "[" in line:
            flag = re.sub(regex, "", line.strip())
        tempFlag = flag
        if tempFlag.startswith("DF") or tempFlag.startswith("SF"):
            tempFlag = tempFlag[1:]
        if tempFlag.startswith("FFlag"):
            dictionary[flag] = random.choice([True, False])
        if tempFlag.startswith("FInt") or tempFlag.startswith("FLog"):
            dictionary[flag] = random.randint(minimum, maximum)
        if tempFlag.startswith("FString"):
            dictionary[flag] = flagText

for key in dictionary:
    if isinstance(dictionary[key], str) and dictionary[key].lower() in ["true", "false"]:
        dictionary[key] = dictionary[key].lower() == "true"

items = json(dictionary, indent=2)
items = f"\033[38;2;52;235;143m{{\033[0m{items.strip()[1:-1]}\033[38;2;52;235;143m}}\033[0m"
print(items)
sys.exit()
