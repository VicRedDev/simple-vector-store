import os
import sys
from config import SCAPE_KEYWORD

def menu(options: list[str]) -> str:
    while True:
        clearConsole()
        print('Selecciona una opcion')
        lineJump()

        for index, option in enumerate(options):
            print(f"{index}) {option}")

        lineJump()
        user_input = str(input('Tu eleccion: ')).lstrip()
        lineJump()

        if user_input in options:
            return user_input
        try:
            int_user_input = int(user_input)
            if 0 <= int_user_input < len(options):
                return options[int_user_input]
            else:
                print('Tu eleccion es invalida')
                lineJump()
                waitEnter()

        except:
            print('Tu eleccion es invalida')
            lineJump()
            waitEnter()

def lineJump(lines: int = 1):
    for i in range(lines):
        print()

def clearConsole():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    lineJump(5)

def waitEnter():
    enter = input('Presiona ENTER para continuar...')
    lineJump()

def chat(chatFunction: callable, exit_keyword: str = SCAPE_KEYWORD, find_exit_keyword: bool = True):
    while True:
        clearConsole()
        print('Describe lo que quieras buscar')
        lineJump()

        user_input = str(input('Su descripcion: ')).lstrip()
        lineJump()
        if exit_keyword.lower() == user_input.lower() or (find_exit_keyword and (exit_keyword.lower() in user_input.lower())):
            break

        chat_response = chatFunction(user_input)
        print(chat_response)
        lineJump()

        waitEnter()

def showProgressPercent(total: int, processed: int):
    percent = 100/total*processed
    print(f"{percent}%")

def _formatSeconds(seconds: float):
    safe_seconds = max(0.0, seconds)
    minutes = int(safe_seconds // 60)
    remaining_seconds = safe_seconds % 60
    return f"{minutes:02d}:{remaining_seconds:05.2f}"

def showEmbeddingProgress(total: int, processed: int, avg_time_seconds: float, eta_seconds: float, bar_length: int = 30):
    if total <= 0:
        return

    progress = min(max(processed / total, 0), 1)
    missing_percent = (1 - progress) * 100
    filled = int(bar_length * progress)
    bar = f"[{'=' * filled}{'-' * (bar_length - filled)}]"

    message = (
        f"\r{bar} Falta: {missing_percent:6.2f}%"
        f" | Total: {total}"
        f" | Procesados: {processed}"
        f" | Promedio: {_formatSeconds(avg_time_seconds)}"
        f" | ETA: {_formatSeconds(eta_seconds)}"
    )
    sys.stdout.write(message)
    sys.stdout.flush()

    if processed >= total:
        print()