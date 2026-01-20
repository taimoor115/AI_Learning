from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Generate a caption for this image"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://images.pexels.com/photos/270632/pexels-photo-270632.jpeg?_gl=1*7l3yo9*_ga*MzU2MzYzNjE2LjE3Njg4OTU5NDg.*_ga_8JE65Q40S6*czE3Njg4OTU5NDgkbzEkZzEkdDE3Njg4OTU5NzkkajI5JGwwJGgw"
                    },
                },
            ],
        }
    ],
)


print("🐱‍🚀 Image caption generated successfully.")
print(response.choices[0].message.content)
