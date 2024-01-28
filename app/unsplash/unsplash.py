import requests

def get_unsplash(amount_of_images, search_query):  # search query must be a string of the preferred topic, i.e "Gaza" , "Sports"
    url = "https://api.unsplash.com/photos/random"

    # My personal API-Key TODO: Remove this and add it to the .env file
    api_key = "yxTqVe8SO0J4Bc8ThfY9wwnZolR3qCNzSU42bzbRCWs"
    parameter = {"client_id": api_key, "count": amount_of_images, "query": search_query}

    response = requests.get(url, params=parameter)
    data = response.json()
    print(data[0]["urls"]["regular"])

    list_of_urls=[]

    for picture in data:
        url=picture["urls"]["regular"]
        list_of_urls.append(url)
    return list_of_urls

#pictures_data=get_unsplash(3, search_query="soccer")

# def save_image(image,name_to_save):
#         save_folder="/workspaces/data-app/app/unsplash/saved_images"
#         filepath = os.path.join(save_folder, name_to_save)
#         image_url = image["urls"]["regular"]#url of chosen image
#         image_response = requests.get(image_url)#download
#         with open(filepath,"wb") as file:
#             file.write(image_response.content)

# save_image(pictures_data[0],"test_save.jpg")#save first image