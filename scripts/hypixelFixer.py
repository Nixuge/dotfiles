#!/bin/python3

import os


PATH = "/home/nix/.local/share/multimc/instances/HiveDL/.minecraft/saves/"

SERVER_NAME = "Hypixel"

GAME_MODES = {
    "rm": ["default"], #SPECIAL: to delete the map
    "Bedwars": [
        "SoloDuo",
        "TrioQuartet",
        "4v4",
        "40v40_Castle",
    ],
    "Lobby": ["default"],
    "Skywars": [
        "Solo",
        "Duo",
        "Ranked",
        "Mega"
    ],
    "MurderMystery": ["default"],
    "Arcade": [ #PARTY GAMES: TODO
        "HoleInTheWall",
        "Football",
        "BountyHunters",
        "PixelPainters",
        "CaptureTheWool",
        "DragonWars",
        "GalaxyWars",
        "ThrowOut",
        "CreeperAttack",
        "FarmHunt",
        "Zombie",
        "HideAndSeek",
        "HypixelSays",
        "MiniWalls",
        "BlockingDead"
    ],
    "Pit": ["default"],
}



def listFiles(path):
    files = []
    for file in os.listdir(path):
        filepath = path + file
        if os.path.isdir(filepath): continue
        
        files.append(filepath)
    files.sort(key=os.path.getmtime)

    #dirty fix
    for file in list(files):
        if f"{SERVER_NAME}-" in os.path.basename(file):
            files.remove(file)
            
    return files

def renameLatestFile():
    input()
    try: file = listFiles(PATH)[-1]
    except Exception as e: 
        print(e)
        return
    
    print(f"Old filename: {os.path.basename(file)}")
    
    # newName = input("New filename: ")
    # if newName == "": return
    # if newName == "rm":
    #     os.system(f"rm '{file}'")
    #     return
    # if "[D" in newName: return
    
    newName = getFileNameFromQuestions()

    if newName == "rm":
        os.system(f"rm '{file}'")
        return
    
    os.system(f"mv '{file}' '{PATH}{newName}.zip'")

    print(f"Changed filename to {newName}")



def getFileNameFromQuestions():
    print("====Choose a game mode====")
    gameMode = grabValFromDictOrList(GAME_MODES)
    gameSubModeList = GAME_MODES.get(gameMode)
    gameSubMode = ""
    if not gameSubModeList == ['default']:
        print("====Choose a game submode====")
        gameSubMode = "-" + grabValFromDictOrList(gameSubModeList)
    
    if gameMode == "rm": return "rm"
    mapName = input("==Enter a map name: ")
    #mapName = mapName.capitalize()
    filename = f"{SERVER_NAME}-{gameMode}{gameSubMode}-{mapName}"
    
    return filename



def grabValFromDictOrList(dict):
    i=1
    numberedDict = {}
    for val in dict:
        numberedDict[str(i)] = val
        print(f"{i}: {val}")
        i+=1
    choiceIndex = input("==choice: ")
    choice = numberedDict.get(choiceIndex)
    if not choice:
        return grabValFromDictOrList(dict)
    return choice




while True:
    renameLatestFile()
    print("=====================")



