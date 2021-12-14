
import discord
from requests.api import request
import os
import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from discord.ext import commands



chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

path = "C://Users/Vince/AppData/Local/Programs/Python/chromedriver.exe" 
script = " "
client = discord.Client()

@client.event
async def on_ready():
    print('Captain Teemo on duty!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if "!list" in message.content:
        await message.channel.send("Here is a list of current commands: ")
        await message.channel.send("!aram 'insert champion' -> grabs a build for aram\n!ranked 'insert champion' -> grabs a build for ranked\n!data 'summoner name' -> grabs data on summoner")

    if "!aram" in message.content:
        await message.channel.send(randomScript())
        champion = message.content[6:]
       # chrome_options = Options()
      #  chrome_options.add_argument("--start-maximized")
       # chrome_options.add_argument("--headless") 
        driver=webdriver.Chrome(options=chrome_options,executable_path=path)
        driver.get('https://app.mobalytics.gg/lol/champions/'+champion+'/aram-builds')
        driver.set_window_size(1920, 1080)
        time.sleep(1)
        driver.get_screenshot_as_file('screenshot.png')
        await message.channel.send(file=discord.File('screenshot.png'))
        os.remove('screenshot.png')
        driver.quit()

    if "!ranked" in message.content:
        await message.channel.send(randomScript())
        champion = message.content[8:]
        #chrome_options = Options()
        #chrome_options.add_argument("--start-maximized")
        #chrome_options.add_argument("--headless") 
        driver=webdriver.Chrome(options=chrome_options,executable_path=path)
        driver.get('https://blitz.gg/lol/champions/'+champion)
        driver.set_window_size(1920, 1080)
        time.sleep(1)
        driver.get_screenshot_as_file('screenshot.png')
        await message.channel.send(file=discord.File('screenshot.png'))
        os.remove('screenshot.png')
        driver.quit()
        
    if "!data" in message.content:
        await message.channel.send(randomScript())
        sumName = message.content[6:]
        responseJSON = requestSummonerData(sumName)
        ID = responseJSON['id']
        responseJSON2 = requestRankedData(ID)
        await message.channel.send("Summoner Name: " + responseJSON2[0]['summonerName'])
        await message.channel.send("Rank: " + responseJSON2[0]['tier'] +" "+ responseJSON2[0]['rank'] )
        await message.channel.send("LP: " + str(responseJSON2[0]['leaguePoints']))
        await message.channel.send("Wins: " + str(responseJSON2[0]['wins']))
        await message.channel.send("Losses: " + str(responseJSON2[0]['losses']))
        
        
def randomScript():
    randNum = random.randrange(1, 5)
    if(randNum == 1):
        script = "Yes, sir!"
    if(randNum == 2):
        script = "I'll scout ahead!"
    if(randNum == 3):
        script = "Reporting in."
    if(randNum == 4):
        script =  "Swiftly!"
    if(randNum == 5):
        script = "Never underestimate the power of the Scout's code."
    return script

def requestSummonerData(summonerName):
    URL = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+summonerName+"?api_key="+config.API
    response = requests.get(URL)
    return response.json()

def requestRankedData(ID):
    URL = "https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/"+ID+"?api_key="+config.API
    response = requests.get(URL)
    return response.json()

client.run(client.env.TOKEN)