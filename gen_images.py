from google import genai
from dotenv import load_dotenv
import os
def generate_image(text):
    load_dotenv()
    URI  = os.getenv("NEO4J_URI")
    USER = os.getenv("NEO4J_USER")
    PWD  = os.getenv("NEO4J_PASSWORD")
    api_k = os.getenv("API_KEY")
    client = genai.Client(api_key=api_k)

    # TODO(developer): Update and un-comment below line
    output_file = "example.png"

    image = client.models.generate_images(
        model="imagen-4.0-generate-preview-06-06",
        prompt=text,
        config = {"number_of_images": 1}
    )

    image.generated_images[0].image.save(output_file)

    print(f"Created output image using {len(image.generated_images[0].image.image_bytes)} bytes")
    # Example response:
    # Created output image using 1234567 bytes