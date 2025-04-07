import os
import openai

# Set your OpenAI API key via the OPENAI_API_KEY environment variable.
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    print("Please set the OPENAI_API_KEY environment variable.")
    exit(1)

def generate_text(prompt, context=""):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # using gpt-3.5-turbo model for interactive narrative
        messages=[
            {"role": "system", "content": "You are an interactive text adventure game narrating an exciting fantasy world."},
            {"role": "user", "content": context + "\nUser: " + prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def generate_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512"
    )
    image_url = response['data'][0]['url']
    return image_url

def main():
    # Starting narrative context
    context = "The adventure begins in a mysterious realm full of magic and wonder."
    print("Welcome to the OpenAI Text Adventure Game!")
    print("Type commands (e.g., 'look around', 'go north').")
    print("Type 'image <description>' to generate an image.")
    print("Type 'quit' to exit.")

    while True:
        command = input("\n> ").strip()
        if command.lower() == "quit":
            print("Goodbye!")
            break

        # If the command starts with "image ", generate an image.
        if command.lower().startswith("image "):
            img_prompt = command[6:].strip()
            print(f"Generating image for: {img_prompt}")
            try:
                img_url = generate_image(img_prompt)
                print("Image URL:", img_url)
            except Exception as e:
                print("Error generating image:", e)
        else:
            try:
                # Generate narrative response
                narrative = generate_text(command, context)
                print(narrative)
                # Append to context for evolving narrative
                context += "\nUser: " + command + "\n" + narrative
            except Exception as e:
                print("Error generating narrative:", e)

if __name__ == "__main__":
    main() 