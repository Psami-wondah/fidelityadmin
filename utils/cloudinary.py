import cloudinary
import cloudinary.uploader
import cloudinary.api
from utils import config


cloudinary.config(
    cloud_name=config.CLOUDINARY_CLOUD_NAME,
    api_key=config.CLOUDINARY_API_KEY,
    api_secret=config.CLOUDINARY_API_SECRET,
)


async def upload_image(image):
    upload_data = cloudinary.uploader.upload(image)
    return upload_data["url"]