from guizero import App, PushButton, ButtonGroup, Box, TitleBox, TextBox, Text
from PIL import Image
import math, time, os.path

chars_ascii = "$@%&#oxcv+~;:-,`'.  " 
chars_uni = "\u2588\u2593\u2592\u2591. "

############# FUNCTION DEFS ###########################################

#checks a value in a selection and compares to some string value and returns based on comparison or returns a default
def check_val(selection, string_val, return_val, default_val):
   if selection.value == string_val:
      return return_val
   else:
      return default_val

#function to resize our image according to new width
def resize_image(image, new_width):
   width, height = image.size
   if width > height:
      ratio = (height / width)
   elif height > width:
      ratio = (width/height)
   else:
      ratio = 1
   new_height = int(new_width*ratio)
   resized_image = image.resize((new_width, new_height))
   return(resized_image)

#convert image to either 8-bit gray or 1-bit mode
def convert_mode(image, mode):
   grayscale_image = image.convert(mode)
   return(grayscale_image)

#convert pixels to character string (pass string of characters to it)
def pixels_to_characters(image, char_string):
   char_list = list(char_string)
   interval = (len(char_list))/256 #0-255 bits of color means 256
   pixels = image.getdata()
   characters = "".join([char_list[int(math.floor(pixel*interval))] for pixel in pixels])
   return(characters)

# primary method that will call the others
def convert_img(size, char, bit):
   #sets new width based on input size
   new_width = int(size.value)
   #sets chars, bit_mode to be used in 
   chars = check_val(char, "Unicode", chars_uni, chars_ascii)
   bit_mode = check_val(bit, "1-bit", "1", "L")
   
   #find path to image file, get base filename for later use
   path = app.select_file(filetypes=[["Image files", "*.gif *.png *.jpg"],["All files", "*.*"]])
   pathbasename = os.path.splitext(os.path.basename(path))[0]

   #open image file then call previously written functions on file
   image = Image.open(path)
   new_image_data = pixels_to_characters(convert_mode(resize_image(image, new_width), bit_mode), chars)

   #format textfile
   pixel_count = len(new_image_data)
   ascii_image = "\n".join(new_image_data[i:(i+new_width)] for i in range(0, pixel_count, new_width))

   #create timestamp for file and create new save filename
   t = (time.strftime("%Y_%m_%d-%H%M%S", time.localtime(time.time())))
   filename = pathbasename+"_"+t+".txt"
   
   #select a save location
   savelocation = app.select_folder(title="Select your save location for output text file", folder=".")

   #save file in output folder
   with open(os.path.join(savelocation, filename), "w", encoding="utf-8") as f:
       f.write(ascii_image)
    
   app.info("Output Confirmed", "Your output file is saved at \n" + savelocation)


################################## %%%%% A P P  F U N C T I O N A L I T Y %%%%% #####################################################

app = App(title="Text Art Image Converter", height=250, width=350) #all drawn pieces must be here
# needed: button to select file, selection of ascii char or unicode, selection of 8-bit or 1-bit, resize width
spacer = Box(app, width="fill", height=15)

width_title = TitleBox(app, text="Resize Width", width=300, height=60, layout="grid")
width_text = Text(width_title, text="Size in pixels to resize image: ", grid=[0,0,1,2], height=2)
width_resize = TextBox(width_title, text="300", grid=[2,0,1,2])

spacer = Box(app, width="fill", height=15)

choice_box = Box(app, layout="grid")
char_title_box = TitleBox(choice_box, text="Choose Characters: ", grid=[0,0,1,2])
spacer = Box(choice_box, width=10, height="fill", grid=[1,0,1,2])
char_choice = ButtonGroup(char_title_box, options=["ASCII", "Unicode"], height=4)

bit_title_box = TitleBox(choice_box, text="Choose Bit Depth: ", grid=[2,0,1,2])
bit_choice = ButtonGroup(bit_title_box, options=["8-bit", "1-bit"], height=4)

#must pass it through as the whole ButtonGroup so we can grab the values; otehrwise it fails
button = PushButton(app, command=convert_img, args=[width_resize, char_choice, bit_choice] , text="Convert Image to Text Art", width="fill", align="bottom")
button.bg = "blue"
button.text_color = "white"
button.text_size = 10

app.display() #last line
