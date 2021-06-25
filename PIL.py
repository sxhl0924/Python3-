import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
# read image and convert to RGB
image=Image.open("readonly/msi_recruitment.gif")
image=image.convert('RGB')

# add font to images and change the color channel

intensity = [0.1, 0.5, 0.9]
images = []
fnt = ImageFont.truetype('readonly/fanwood-webfont.ttf', 75)

for s in intensity:
    #draw the font image
    font_bg =Image.new('RGB', (image.width, 50), color = 'black')
    font_img = ImageDraw.Draw(font_bg)
    font_img.text = ((0,0), "channel 0, intensity {}".format(s), font=fnt, fill="#FFFFFF")
    # create a blank image
    image_font = Image.new('RGB', (image.width, image.height + 50), color = "white")
    #combine the font image and original image
    image_font.paste(image,(0,0))
    image_font.paste(font_bg,(0, image.height))
    # change the color channel of the txt
    r, g, b = image_font.split()
    varied_r = r.point(lambda i: i*s)
    varied_img = Image.merge('RGB', [varied_r, g, b])
    images.append(varied_img)

for s in intensity:
    font_bg =Image.new('RGB', (image.width, 50), color = 'black')
    font_img = ImageDraw.Draw(font_bg)
    font_img.text = ((0,0), "channel 1, intensity {}".format(s), font=fnt, fill="#FFFFFF")
    image_font = Image.new('RGB', (image.width, image.height + 50), color = "white")
    image_font.paste(image,(0,0))
    image_font.paste(font_bg,(0, image.height))
    r, g, b = image_font.split()
    varied_g = g.point(lambda i: i*s)
    varied_img = Image.merge('RGB', [r, varied_g, b])
    images.append(varied_img)


for s in intensity:
    font_bg =Image.new('RGB', (image.width, 50), color = 'black')
    font_img = ImageDraw.Draw(font_bg)
    font_img.text = ((0,0), "channel 2, intensity {}".format(s), font=fnt, fill="#FFFFFF")
    image_font = Image.new('RGB', (image.width, image.height + 50), color = "white")
    image_font.paste(image,(0,0))
    image_font.paste(font_bg,(0, image.height))
    r, g, b = image_font.split()
    varied_b = b.point(lambda i: i*s)
    varied_img = Image.merge('RGB', [r, g, varied_b])
    images.append(varied_img)

# create a contact sheet from different brightnesses
first_image=images[0]
contact_sheet=PIL.Image.new(first_image.mode, (first_image.width*3,first_image.height*3))
x=0
y=0

for img in images:
    # Lets paste the current image into the contact sheet
    contact_sheet.paste(img, (x, y) )
    # Now we update our X position. If it is going to be the width of the image, then we set it to 0
    # and update Y as well to point to the next "line" of the contact sheet.
    if x+first_image.width == contact_sheet.width:
        x=0
        y=y+first_image.height
    else:
        x=x+first_image.width

# resize and display the contact sheet
contact_sheet = contact_sheet.resize((int(contact_sheet.width/2),int(contact_sheet.height/2) ))
display(contact_sheet)
