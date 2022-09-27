
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api

from dotenv import load_dotenv
load_dotenv()  
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")
CLOUDINARY_API_KEY= os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_CLOUD_NAME= os.getenv("CLOUDINARY_CLOUD_NAME")

cloudinary.config(
cloud_name = CLOUDINARY_CLOUD_NAME,
api_key = CLOUDINARY_API_KEY,
api_secret = CLOUDINARY_API_SECRET,
secure= True
)

def uploadImage(img, name):
  cloudinary.uploader.upload(img, public_id=name, unique_filename = False, overwrite=True)

  # Build the URL for the image and save it in the variable 'srcURL'
  srcURL = cloudinary.CloudinaryImage(name).build_url()

  # Log the image URL to the console. 
  # Copy this URL in a browser tab to generate the image on the fly.
  return srcURL


