import json
from openai import OpenAI
import urllib.request, datetime, os
from PIL import Image, ImageDraw, ImageFont
import textwrap
from dotenv import load_dotenv

# load dotenv
load_dotenv()


## RECIEVING FACT OF THE DAY

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a knowledge assistant. You can answer questions about any topic."},
        {"role": "user", "content": "Tell me a random fact of the day, based on information you found in the internet. I want to learn something new and it is important that I have a valid source, so be 100% sure to tell only true and reliable facts. Don't tell me the source as link, rather tell me the provider (Organisation, Magazine, Websitename, etc.). Give me the fact and its source in JSON format like this: {\"fact\": \"Here is the fact\", \"source\": \"Here is the source\"}. Be sure that you don't include any other information in the response."},
    ]
)
assistant_reply = json.loads(response.choices[0].message.content)

print(assistant_reply)
fact = assistant_reply['fact']
source = assistant_reply['source']  


## RECIEVING BACKGROUND-PICTURE

response = client.images.generate(
  model = "dall-e-3",
  prompt=f"{fact}. Generate a picture which suits to that fact. Dont add any text on the picture and avoid symbols.",
  size="1024x1024",
  quality="standard",
  n=1
)
image_url = response.data[0].url
print(image_url)

now = datetime.datetime.now()
now = now.strftime("%Y-%m-%d-%H%M%S")

MYDIR = ("imageOfTheDay")
CHECK_FOLDER = os.path.isdir(MYDIR)
if not CHECK_FOLDER:
    os.makedirs(MYDIR)
    print("Created folder : ", MYDIR)

picture = urllib.request.urlretrieve(image_url, f"imageOfTheDay/{now}.png")


## ADD CONTENT TO PICTURE

# Make picture less transparent
image = Image.open(f"imageOfTheDay/{now}.png")
image.putalpha(127)

# Add fact to picture
draw = ImageDraw.Draw(image)
font_path = "/System/Library/Fonts/Helvetica.ttc"
font = ImageFont.truetype(font_path, 36)
text_color = (255, 255, 255) 
text_position = (image.width // 2, image.height // 2) 
max_text_width = 0.8 * image.width 
wrapper = textwrap.TextWrapper(width=30) 
text = wrapper.fill(fact)
draw.text(text_position, text, fill=text_color, font=font, anchor="mm",align="center")

#Add source to picture
additional_font_size = 24 
additional_font = ImageFont.truetype(font_path, additional_font_size)
additional_text_color = (128, 128, 128) 
additional_text_position = (20, image.height - 40) 
draw.text(additional_text_position, f"Source: {source}", fill=additional_text_color, font=additional_font)

# Save picture
image.save(f"imageOfTheDay/{now}.png")