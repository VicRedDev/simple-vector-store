
from ui import menu, chat, clearConsole, lineJump, waitEnter
from app import getChatFunction, getFileText
from lister import lister
from vectorstore import VectorStore, getTextPieces, textPiecesToContents
vectorstore_client = VectorStore()
chatFunction = getChatFunction(vectorstore_client)

mode = 'menu'
while True:
    if mode == 'menu':
        mode = menu([
            'chat',
            'sync',
            'exit',
        ])

    if mode == 'chat':
        chat(chatFunction, 'bye', True)

    if mode == 'sync':
        text_file_name = menu(['cancel'] + lister('documents', '.txt'))
        if text_file_name == 'cancel':
            mode = 'menu'
            continue

        clearConsole()
        print(f"Obteniendo el texto {text_file_name}")
        
        text_file = f"documents/{text_file_name}"
        text = getFileText(text_file)

        clearConsole()
        print(f"Dividiendo el texto en piezas")
        text_pieces = getTextPieces(text)

        clearConsole()
        print(f"Procesando las {len(text_pieces)} piezas del texto")
        text_contents = textPiecesToContents(text_pieces, text_file_name)

        clearConsole()
        print(f"Sincronizando las piezas procesadas a la base de datos")
        vectorstore_client.upsert(text_contents)

        clearConsole()
        print(f"Se sincronizaron {len(text_pieces)} piezas del texto {text_file_name}")

        lineJump()
        waitEnter()
    
    if mode == 'exit':
        break

    mode = 'menu'

quit()