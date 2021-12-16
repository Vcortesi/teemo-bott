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

PATH = "C://Users/Vince/AppData/Local/Programs/Python/chromedriver.exe"
client = discord.Client() 
script = " "

# onReady def
@client.event
async def on_ready():
    print('Captain Teemo on duty!')

# All of the commands the bot listens for
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Shows the user a list of available commands
    if "!list" in message.content:
        await message.channel.send("Here is a list of current commands: ")
        await message.channel.send("!aram 'insert champion' -> grabs a build for aram\n!ranked 'insert champion' -> grabs a build for ranked\n!data 'summoner name' -> grabs data on summoner")

    # Grabs a screenshot of aram builds for a specified champion
    if "!aram" in message.content:
        await message.channel.send(randomScript())
        champion = message.content[6:]
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        driver.get('https://app.mobalytics.gg/lol/champions/'+champion+'/aram-builds')
        driver.set_window_size(1920, 1080)
        time.sleep(1)
        driver.get_screenshot_as_file('screenshot.png')
        await message.channel.send(file=discord.File('screenshot.png'))
        os.remove('screenshot.png')
        driver.quit()

    # Grabs a screenshot of ranked builds for a specified champion
    if "!ranked" in message.content:
        await message.channel.send(randomScript())
        champion = message.content[8:]
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        driver.get('https://probuildstats.com/champion/'+champion)
        driver.set_window_size(1920, 1080)
        time.sleep(2)
        driver.find_element_by_class_name('champion-page_top-bar')
        driver.get_screenshot_as_file('screenshot.png')
        await message.channel.send(file=discord.File('screenshot.png'))
        os.remove('screenshot.png')
        driver.quit()
    
    # Grabs a screenshot of counters for a specified champion
    if "!counter" in message.content:
        await message.channel.send(randomScript())
        champion = message.content[8:]
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        driver.get('https://u.gg/lol/champions/'+champion+'/counter')
        driver.set_window_size(1920, 1080)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        driver.get_screenshot_as_file('screenshot.png')
        await message.channel.send(file=discord.File('screenshot.png'))
        os.remove('screenshot.png')
        driver.quit()

    # Uses call definitions to give the user data    
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

# Randomly selects a prompt the bot will say on commands       
def randomScript():
    randNum = random.randrange(1, 5)
    if(randNum == 1):
        script = "'''Yes, sir!"
    if(randNum == 2):
        script = "'''I'll scout ahead!"
    if(randNum == 3):
        script = "'''Reporting in."
    if(randNum == 4):
        script =  "'''Swiftly!"
    if(randNum == 5):
        script = "'''Never underestimate the power of the Scout's code."
    return script

# Grabs JSON from Riot's API
async def requestSummonerData(summonerName):
    URL = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+summonerName+"?api_key="+os.environ.get('API')
    response = requests.get(URL)
    return response.json()

# Grabs JSON from Riot's API
async def requestRankedData(ID):
    URL = "https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/"+ID+"?api_key="+os.environ.get('API')
    response = requests.get(URL)
    return response.json()

client.run(os.environ.get('TOKEN'))