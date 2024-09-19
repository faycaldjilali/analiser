
def get_prompt_1(text):
    return (
        f"Extract following detailed information from the text:\n"
        f"Synthèse des éléments pertinents :\n"
        f"2.Actions à prendre par SEF (Stores et Fermetures) :\n"
        f"Text:\n{text}"
    )

def get_prompt_2(text):
    return (
        f"From the following text, generate a numbered list of To-Do items:\n\n"
        f"Text:\n{text}\n\n"
        f"To-Do List:\n1. "
    )