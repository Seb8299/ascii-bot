import discord
from PIL import Image
import requests
import io
import json
import re


config_file = open("config.json", "r").read()
config = json.loads(config_file)
token = config["token"]

ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^'´. " #70 steps of brighness

def rgb2gray(rgb):

    r, g, b = rgb[0], rgb[1], rgb[2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

client = discord.Client()



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    print("got message!")

    # url with image?
    x = re.search("^\/paint \w+(\.jpg|\.jpeg|\.png)$", message)

    if not x:
        return

    # split the url from comand
    substring = message.content.split()[1]

    # get the image from url
    r = requests.get(substring)
    image_bytes = io.BytesIO(r.content)
    img = Image.open(image_bytes)

    attempt = 100

    while True:  
        WIDTH_LIMIT = attempt

        WIDTH_LIMIT = int(WIDTH_LIMIT/2)    
        HEIGHT_LIMIT = int((WIDTH_LIMIT * img.size[1]) / img.size[0])

        WIDTH_LIMIT *= 2
        
        attempt -= 0.5

        if(WIDTH_LIMIT*HEIGHT_LIMIT+HEIGHT_LIMIT < 2000):
            break

    # saves all pixels of img
    pix = img.load()
    
    # calc range of gray
    minG = 265
    maxG = 0

    for y in range(HEIGHT_LIMIT):
    
        for x in range(WIDTH_LIMIT):

            gray = rgb2gray( pix[x*(img.size[0]/WIDTH_LIMIT), y*(img.size[1]/HEIGHT_LIMIT)] )

            if (gray > maxG):
                maxG = gray

            if (gray < minG):
                minG = gray

    final = ""

    # goes through the pixels of the img
    for y in range(HEIGHT_LIMIT):
        row = ""
    
        for x in range(WIDTH_LIMIT):

            # calc the gray value of the pixel
            gray = rgb2gray( pix[x*(img.size[0]/WIDTH_LIMIT), y*(img.size[1]/HEIGHT_LIMIT)] )
            
            letter = int(translate(gray, minG, maxG, 0, 69))

            # finds the matching ascii char
            row += ASCII_CHARS[letter]

        final += row+"\n"

    print("("+str(WIDTH_LIMIT)+", "+str(HEIGHT_LIMIT)+")")
    print(len(final))

    # print(final)

    # generate embed and send
    embed=discord.Embed(title="Atful Artist", url="https://github.com/Seb8299/ascii-bot", description="Convert an Image to ASCII Art", color=0x42d400)
    embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
    embed.set_thumbnail(url="https://images0.gerstaecker.de/out/pictures/generated/1500_1500/pboxx-pixelboxx-2538173/Lavinia+Stempel%2C+Mystischer+Baum.jpg")
    embed.add_field(name="("+str(WIDTH_LIMIT)+", "+str(HEIGHT_LIMIT)+")", value="```" + final + "```", inline=False)
    
    try:
        await message.channel.send(embed=embed)
    except:
        pass

    try:
        await message.channel.send("```" + final + "```")
    except:
        pass
        
        
        

client.run(token)