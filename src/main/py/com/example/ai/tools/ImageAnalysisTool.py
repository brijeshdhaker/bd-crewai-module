import os
from PIL import Image
import base64
import io
from groq import Groq
import logging
import json

from crewai.tools import tool
from openai import OpenAI


# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('logs/image_tool.log')
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

class ImageAnalysisTool:
    """Tool to analyse an image and generate markdown based on analysis
    Parameters:
      - query: a json string containing the following fields:
        - check (str): The check to be performed.
        - image_name (str): The name of the image to analyse
    Returns:
        str:  a string in json format confrims if features are found, 
        the confidence in the result and rationale for the result
              or an informative message if no answer is found.
    """

    @staticmethod
    def _resize_and_encode_image(image_path:str,max_image_size:int=1024):
        """
        Loads an image, resizes it to a maximum dimension of 2048 while maintaining aspect ratio, 
        and converts it to base64 encoding.
    
        Args:
            image_path: Path to the image file.
    
        Returns:
            Base64 encoded string of the resized image.
        """
        try:
            with Image.open(image_path) as img:
                width, height = img.size
    
                # Calculate the maximum dimension to maintain aspect ratio
                if width > height:
                    max_size = (max_image_size, int(2048 * (height / width)))
                else:
                    max_size = (int(2048 * (width / height)), max_image_size)
    
                # Resize the image
                img = img.resize(max_size, Image.LANCZOS)
    
                # Convert the image to bytes
                buffered = io.BytesIO()
                img.save(buffered, format="JPEG")
                img_bytes = buffered.getvalue()
    
                # Encode the image in base64
                base64_encoded_image = base64.b64encode(img_bytes).decode('utf-8')
    
                return base64_encoded_image
    
        except Exception as e:
            print(f"Error processing image: {e}")
            return None

    @staticmethod
    def _get_image_markdown(image_name:str="test_image.png",max_image_size:int=1024):
        groq_api_key=os.getenv("GROQ_API_KEY","dev-key-please-change")
        groq_vision_model=os.getenv("GROQ_VISION_MODEL","llama-3.2-11b-vision-preview")
        image_dir="./data/images"
        vision_prompt="Provide a detailed analysis of the image in markdown format"

        client = Groq(api_key=groq_api_key)

        image_path=str(os.path.join(image_dir,image_name))
        base64_image = ImageAnalysisTool._resize_and_encode_image(image_path)


        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"{vision_prompt}"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            model=f"{groq_vision_model}",
        )

        image_markdown=chat_completion.choices[0].message.content
        logger.info(f"image markdown: {image_markdown}")
        return image_markdown


    @tool("Compare an image with a textual description and provide a comparison")
    def analyse_image(query: str):
    """Tool to analyse an image and generate markdown based on analysis
    Parameters:
      - query: a json string containing the following fields:
        - check (str): The check to be performed.
        - image_name (str): The name of the image to analyse
    Returns:
        str:  a string in json format confrims if features are found, 
        the confidence in the result and rationale for the result
              or an informative message if no answer is found.
    """
    logger.info(f"query: {query}")  
    payload=json.loads(query)
    try:
      image_name=payload.get("image_name")
      check=payload.get("check")
    except e:
      logger.debug(f"query parameter {query} not in expected format")
    
    groq_api_key=os.getenv("GROQ_API_KEY","dev-key-please-change")
    groq_model_name=os.getenv("GROQ_MODEL","llama3-8b-8192")

    
    client = Groq(api_key=groq_api_key)
    image_markdown=ImageAnalysisTool._get_image_markdown(image_name)
  
    chat_completion = client.chat.completions.create(
        messages=[
            {
                'role': 'system',
                'content': '''you are a reviewer of documents and images. Who summarizes documents in JSON.  The JSON should include
                {
                  [
                  "question": {
                        "query:"string",
                        "answer": "string",
                        "confidence_score": "number (0-1)"
                        "rationale": "string"
                        # Include additional fields as required
                      }
                    ]
                }
                '''
            },
            {
                'role': 'user',
                'content': f'based on {image_markdown} confirm {check}. This is the only question to be answered'
           }
        ],

        # The language model which will generate the completion.
        model=f"{groq_model_name}",
        temperature=0.5,
        response_format={"type": "json_object"},
        max_tokens=1024,
        top_p=1,
        stop=None,
        stream=False,

    )
    result=chat_completion.choices[0].message.content

    return result