
import discord
from PIL import Image
import requests
import io

ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. " #70 steps of brighness

LIMIT = 50

def rgb2gray(rgb):

    r, g, b = rgb[0], rgb[1], rgb[2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # url with image?
    pic_ext = ['.jpg','.png','.jpeg']
    for ext in pic_ext:
        if message.content.endswith(ext):
    
            # get the image from url
            r = requests.get(message.content)
            image_bytes = io.BytesIO(r.content)
            img = Image.open(image_bytes)

            print(img.size)

            # saves all pixels of img
            pix = img.load()

            xScale = int(img.size[0]/(LIMIT*1.5)) if img.size[0] > LIMIT else 1
            yScale = int(img.size[1]/LIMIT) if img.size[1] > LIMIT else 1
            
            final = ""

            # goes through the pixels of the img
            for y in range(img.size[1]):
                s = ""
            
                if (y%yScale == 0):
                    for x in range(img.size[0]):

                        if (x%xScale == 0):
                            # calc the gray value of the pixel
                            gray = int( rgb2gray( pix[x, y]) * 0.2734375 )

                            # finds the matching ascii char
                            s += ASCII_CHARS[gray]
                            if (xScale <= 2):
                                s += ASCII_CHARS[gray]
                            if (xScale == 1):
                                s += ASCII_CHARS[gray]

                    final += s+"\n"

            print(final)
            test = "2"

            # embedVar = discord.Embed(title="asd", description="Desc")
            # embedVar.add_field(name="asd", value=str(final[5]), inline=False)
            # await message.channel.send(embed=embedVar)


client.run('NzU0NDI2NTk4Njg5NjAzODA2.X10khQ.5bQPLBy_RqqZNBhDWEA73QLQPEs')