from vertexai.preview import generative_models
import vertexai
from PIL import Image
from io import BytesIO
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "intern-api-use.json"

vertexai.init(project="your-project-id", location="us-central1")

model = generative_models.ImageGenerationModel.from_pretrained("imagen@001")

response = model.generate(
    prompt="A cthulu-inspired horror environment",
    max_output_tokens=1024,
    temperature=0.7,
    candidate_count=1,
    image_size="512x512"
)

image_bytes = response.images[0].image_bytes
image = Image.open(BytesIO(image_bytes))
image.save("imagen_result.png")
image.show()
