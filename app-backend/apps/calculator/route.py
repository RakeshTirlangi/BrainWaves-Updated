# from fastapi import APIRouter
# import base64
# from io import BytesIO
# from apps.calculator.utils import process_image
# from schema import ImageInfo
# from PIL import Image

# router = APIRouter()

# @router.post('')
# async def run(data: ImageInfo):
#     image_data = base64.b64decode(data.image.split(",")[1])  # Assumes data:image/png;base64,<data>
#     image_bytes = BytesIO(image_data)
#     image = Image.open(image_bytes)
#     responses = process_image(image, dict_of_vars=data.dict_of_vars)
#     data = []
#     for response in responses:
#         data.append(response)
#     print('response in route: ', response)
#     return {"message": "Image processed", "data": data, "status": "success"}



from fastapi import APIRouter
import base64
from io import BytesIO
from apps.calculator.utils import process_image
from schema import ImageInfo
from PIL import Image
#import pillow_avif  # Pillow AVIF plugin to handle AVIF format

router = APIRouter()

@router.post('')
async def run(data: ImageInfo):
    # Extract base64 image data from the input (Assumes data:image/avif;base64,<data>)
    image_data = base64.b64decode(data.image.split(",")[1])  
    image_bytes = BytesIO(image_data)

    # Open the image, specifically handling AVIF format
    image = Image.open(image_bytes)

    # Process the image using a utility function
    responses = process_image(image, dict_of_vars=data.dict_of_vars)

    # Collect the responses into a list
    data = []
    for response in responses:
        data.append(response)
    
    print('response in route: ', response)
    
    return {"message": "Image processed", "data": data, "status": "success"}
