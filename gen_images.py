from google import genai
from dotenv import load_dotenv
import os
def generate_image(text, name, folder="static/images"):
    load_dotenv()
    URI  = os.getenv("NEO4J_URI")
    USER = os.getenv("NEO4J_USER")
    PWD  = os.getenv("NEO4J_PASSWORD")
    api_k = os.getenv("API_KEY")
    client = genai.Client(api_key=api_k)

    # TODO(developer): Update and un-comment below line
    output_file = folder+name+".png"


    image = client.models.generate_images(
        model="imagen-4.0-generate-preview-06-06",
        prompt=text,
        config = {"number_of_images": 1}
    )

    image.generated_images[0].image.save(output_file)

    print(f"Created output image using {len(image.generated_images[0].image.image_bytes)} bytes")
    return "/"+output_file
    # Example response:
    # Created output image using 1234567 bytes

def clear_folder(folder_path = 'static/images'):
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist.")
        return

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

    print(f"All files in '{folder_path}' have been deleted.")