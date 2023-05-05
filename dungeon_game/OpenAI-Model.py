import openai
import json

# set up the OpenAI API key
openai.api_key = "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"

# set up the GPT-3 model
model_engine = "text-davinci-002"
temperature = 0.5
max_tokens = 100

while True:
    # get user input
    user_input = input("Please enter some text (or type 'exit' to quit): ")
    # check if the user wants to exit
    if user_input == "exit":
        break


    text = ""

    # generate text
    response = openai.Completion.create(
        engine=model_engine,
        prompt=user_input+text,
        temperature=temperature,
        max_tokens=max_tokens
    )

    # extract the generated text from the API response
    generated_text = response.choices[0].text.strip()

    # print the generated text
    print("Generated text:")
    print(generated_text)
    text = generated_text
