from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load pre-trained model and tokenizer
model_name = "gpt2-large"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)


def generate_response1(image_description):
    input_text = f"Based on this image description: '{image_description}', provide a creative and thoughtful response."

    input_ids = tokenizer.encode(input_text, return_tensors='pt')

    output = model.generate(
        input_ids,
        max_length=150,  # Reasonable length for a concise response
        num_return_sequences=1,
        temperature=0.7,  # Balances creativity and coherence
        top_p=0.9,  # Nucleus sampling
        top_k=50,  # Limits the number of next word predictions
        repetition_penalty=1.2,  # Avoids repetition
        do_sample=True,  # Enables sampling for more diverse output
        early_stopping=True  # Stops when the model thinks it's done
    )

    # Decode the output
    response = tokenizer.decode(output[0], skip_special_tokens=True)

    # Post-process the response
    response = response.strip()

    # Optionally, take only the first sentence for clarity
    if "." in response:
        response = response.split(".")[0] + "."

    return response
