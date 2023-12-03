# %%
import requests
from IPython.display import Image, display
import os


def get_unsplash(amount_of_images,search_query):#search query must be a string of the preferred topic, i.e "Gaza" , "Sports"
# %%
 url = "https://api.unsplash.com/photos/random"

# My personal API-Key
 api_key = "yxTqVe8SO0J4Bc8ThfY9wwnZolR3qCNzSU42bzbRCWs"

# %%

 parameter={
    "client_id":api_key,
    "count":amount_of_images,
    "query":search_query
 }
 
 response = requests.get(url, params=parameter)
 data = response.json()
 print(data)



# %%
#important to get the name of the photograph and the url, because unsplash wants you to credit the photograph and themselves when using an image
 def display_images(images_data):
  for foto in images_data:
    foto_url = foto["urls"]["regular"]
    print(foto["user"]["name"])
    print(foto_url)
    display(Image(url=foto_url))

 display_images(data)

# %%
#save_image has to be modified to a common save space. Or just exported to the frontend
 #def save_image(image,name_to_save):
  #save_folder="/workspaces/data-app/notebooks/saved_images_unsplash"#has to be changed to the new directory
  #filepath = os.path.join(save_folder, name_to_save)
  #image_url = image["urls"]["regular"]#url of chosen image
  #image_response = requests.get(image_url)#download
  #with open(filepath,"wb") as file:
   #  file.write(image_response.content)

 #save_image(data[0],"test_save.jpg")#save first image

    


