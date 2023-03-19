import requests
from lxml import html
import discord
import matplotlib.pyplot as plt
import datetime

import config

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)
dates = []
downloads = []



def getNumber():
    # URL de la page à accéder
    url = "https://extensions.gnome.org/extension/5805/disk-usage/"
    # Récupération du contenu de la page
    response = requests.get(url)
    content = response.content
    # Extraction de l'élément à partir de son xpath
    tree = html.fromstring(content)
    element = tree.xpath('/html/body/div[2]/div/div[2]/div[1]/span[3]')[0]
    texte = element.text
    # Affichage du texte extrait
    print(texte)
    # Get the current date
    date = datetime.datetime.now().strftime("%d/%m")
    # Open the file in read mode to check for existing date
    with open('data.txt', 'r') as file:
        # Check if the current date is already in the file
        if any(line.startswith(date) for line in file):
            # Open the file in read mode to get existing content
            with open('data.txt', 'r') as file:
                # Read the contents of the file into a list of lines
                lines = file.readlines()
            # Open the file in write mode to update the content
            with open('data.txt', 'w') as file:
                # Iterate through the lines and update the line with the current date and content
                for line in lines:
                    if line.startswith(date):
                        file.write(date + " " + texte + "\n")
                    else:
                        file.write(line)
        else:
            # Open the file in append mode to add new text
            with open('data.txt', 'a') as file:
                # Append the text and date to the file on a new line
                file.write(texte + " " + date + "\n")
    with open("data.txt", "r") as f:
        lines = f.readlines()

    unique_lines = []
    for line in lines:
        if line not in unique_lines:
            unique_lines.append(line)

    with open("data_graph.txt", "w") as f:
        for line in lines:
            if line in unique_lines:
                f.write(line)
                unique_lines.remove(line)

    return texte

# define a function to send the PNG file
async def send_image(channel):
    # open the PNG file and read the data
    with open('graph.png', 'rb') as f:
        image_data = f.read()
    # send the PNG file to the channel
    await channel.send(file=discord.File(image_data, 'graph.png'))

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        print(client.user)
        return
    if message.content.startswith('graph'):
        async with message.channel.typing():
            getNumber()
            # Open the data file and read the data
            with open('data_graph.txt', 'r') as file:
                for line in file:
                    # Split the line into the number and date
                    parts = line.split()
                    number = int(parts[0])
                    date = datetime.datetime.strptime(parts[2], "%d/%m").date()
                    # Add the data to the lists
                    dates.append(date)
                    downloads.append(number)
            # Create the bar graph
            plt.plot(dates, downloads)
            # Add labels to the graph
            plt.title('Total number of downloads per day')
            plt.xlabel('Date')
            plt.ylabel('Total number of downloads')
            # Save the graph as a PNG file
            plt.savefig('graph.png')
            with open('graph.png', 'rb') as f:
                picture = discord.File(f)
                await message.channel.send(file=picture)
    if message.content.startswith('data' or 'Data'):
        async with message.channel.typing():
            print(message.content)
            response = getNumber()
            await message.channel.send(response)
            print(response)
    if message.content.startswith('shutdown'):
        print(message.content)
        await message.channel.send("shutting down...")
        keep_going=False
    if message.content.startswith('WhoAmI'):
        async with message.typing():
            await message.channel.send('You are {}'.format(message.author.name))


client.run(config.discord_token)



