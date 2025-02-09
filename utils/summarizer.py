from groq import Groq

def summarize_text(text, language, api_key, max_tokens=4000):
    """
    Summarize text in the given language using Groq API.
    Split the text into chunks if it exceeds the token limit.
    """
    try:
        # Initialize Groq client
        client = Groq(api_key=api_key)

        # Split the text into chunks based on max_tokens
        chunks = [text[i:i + max_tokens] for i in range(0, len(text), max_tokens)]

        summaries = []
        for chunk in chunks:
            # Generate summary for each chunk
            response = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[
                    {"role": "system", "content": f"You are an AI that summarizes text in {language}."},
                    {"role": "user", "content": f"Summarize this text in {language} in bullet points:\n{chunk}"}
                ]
            )
            summaries.append(response.choices[0].message.content)

        # Combine all summaries into a final summary
        final_summary = "\n".join(summaries)
        return final_summary
    except Exception as e:
        raise Exception(f"Error summarizing text: {e}")

def extract_recipe(text, language, api_key, max_tokens=4000):
    """
    Extract recipe (ingredients and steps) from the given text using Groq API.
    Split the text into chunks if it exceeds the token limit.
    """
    try:
        # Initialize Groq client
        client = Groq(api_key=api_key)

        # Split the text into chunks based on max_tokens
        chunks = [text[i:i + max_tokens] for i in range(0, len(text), max_tokens)]

        recipes = []
        for chunk in chunks:
            # Generate recipe for each chunk
            response = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[
                    {"role": "system", "content": f"You are an AI that extracts and translates recipes to {language}. Maintain the same measurements and quantities but translate all text including ingredient names and instructions to {language}."},
                    {"role": "user", "content": f"""First extract the recipe from the text, then translate everything to {language}.
                    Format the output exactly as follows:

                    **Ingredientes:** (or equivalent in {language})
                    - List ingredients in {language}

                    **Preparación:** (or equivalent in {language})
                    1. Step 1
                    2. Step 2

                    Text to process:
                    {chunk}"""}
                ]
            )
            recipes.append(response.choices[0].message.content)

        # Combine all recipes into a final recipe
        final_recipe = "\n\n".join(recipes)
        return final_recipe
    except Exception as e:
        raise Exception(f"Error extracting recipe: {e}")