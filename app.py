from ui import waitEnter

def getChatFunction(vectorstore_client):
    def chatFunction(user_input: str, k: int = 5):
        related_contents = vectorstore_client.query([user_input], k)
        documents = [f"Resultado {index+1}:\n {content}" for index, content in enumerate(related_contents['documents'][0])]

        if len(documents) <= 0:
            return "No se encontraron resultados"
        
        chat_response = f"Estos son los {len(documents)} resultados mas cercanos:\n\n" + "\n\n".join(documents)

        return chat_response
    
    return chatFunction

def getFileText(file_name: str):
    with open(file_name, 'r') as file:
        text = '\n'.join(file.readlines())

    clean_text = text
    while '\n\n\n' in clean_text:
        clean_text = clean_text.replace('\n\n', '\n')

    return clean_text