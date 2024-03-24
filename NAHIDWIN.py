import pygame
import sys
from googletrans import Translator
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

def translator_window():
    pygame.init()

    width, height = 400, 400

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Перекладач")

    font_size = 24
    font = pygame.font.Font(None, font_size)

    background = pygame.transform.scale(pygame.image.load("blue.jpg"), (width, height))

    intro_text = "?"
    user_input = ""
    translated_text = ""
    history = []
    max_input_length = 20
    scroll_offset = 0
    max_history_items = 5

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    translator = Translator()
                    translated_text = translator.translate(user_input, dest='en').text
                    print("Переклад:", translated_text)
                    history.append((user_input, translated_text))

                    if len(history) > 10:
                        history = history[-10:]
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.key == pygame.K_UP:
                    scroll_offset = min(scroll_offset + 1, max(0, len(history) - max_history_items))
                elif event.key == pygame.K_DOWN:
                    scroll_offset = max(scroll_offset - 1, 0)
                else:
                    user_input += event.unicode

        screen.blit(background, (0, 0))

        intro_surface = font.render(intro_text, True, (0, 0, 0))
        intro_rect = intro_surface.get_rect(center=(width // 2, height // 2 - 50))
        screen.blit(intro_surface, intro_rect)

        input_rect = pygame.Rect(width // 2 - 150, height // 2, 200, 30)
        pygame.draw.rect(screen, (255, 255, 255), input_rect)

        user_input_surface = font.render(user_input, True, (0, 0, 0))
        user_input_rect = user_input_surface.get_rect(topleft=input_rect.topleft)

        if user_input_rect.width > input_rect.width:
            lines = []
            current_line = ""
            for char in user_input:
                test_line = current_line + char
                if font.size(test_line)[0] < input_rect.width:
                    current_line += char
                else:
                    lines.append(current_line)
                    current_line = char
            lines.append(current_line)

            # Виводимо текст на екран
            line_spacing = font_size  # Відстань між рядками
            for i, line in enumerate(lines):
                line_surface = font.render(line, True, (0, 0, 0))
                line_rect = line_surface.get_rect(topleft=(input_rect.left, input_rect.top + i * line_spacing))
                screen.blit(line_surface, line_rect)
        else:
            screen.blit(user_input_surface, user_input_rect)

        history_rect = pygame.Rect(width // 2 - 150, height // 2 + 50, 200, max_history_items * 30)
        pygame.draw.rect(screen, (255, 255, 255), history_rect)

        for i, (original, translation) in enumerate(history[scroll_offset:scroll_offset + max_history_items]):
            history_item_surface = font.render(f"{original} -> {translation}", True, (0, 0, 0))
            history_item_rect = history_item_surface.get_rect(
                topleft=(history_rect.x, history_rect.y + i * 30)
            )
            screen.blit(history_item_surface, history_item_rect)

        pygame.display.flip()

        pygame.time.Clock().tick(60)

def open_translator_window():
    translator_window()

def open_search_window():
    def find_folder():
        folder_name = folder_name_entry.get()
        if not folder_name:
            messagebox.showerror("Помилка", "Введіть назву папки.")
            return

        found_folders = []
        for root, dirs, files in os.walk("/"):
            for dir_name in dirs:
                if folder_name.lower() in dir_name.lower():
                    found_folders.append(os.path.join(root, dir_name))

        if not found_folders:
            messagebox.showinfo("Інформація", f"Папка з назвою '{folder_name}' не знайдена.")
        else:
            messagebox.showinfo("Результат", f"Знайдено папку з назвою '{folder_name}':\n\n" + "\n".join(found_folders))

    def search_file(query_string, folder_path):
        subprocess.Popen(f'explorer /root,"search-ms:query={query_string}&crumb=folder:{folder_path}&"')

    search_window = tk.Tk()
    search_window.title("Пошук папки")

    folder_name_label = tk.Label(search_window, text="Введіть назву папки:")
    folder_name_label.pack(pady=5)

    folder_name_entry = tk.Entry(search_window, width=40)
    folder_name_entry.pack(pady=5)

    find_button = tk.Button(search_window, text="Знайти", command=find_folder)
    find_button.pack(pady=5)

#    search_button = tk.Button(search_window, text="Пошук файлу", command=lambda: search_file('file_name.png', r'C:\Users\your_name\Pictures'))
 #   search_button.pack(pady=5)

    search_window.mainloop()

# Створення головного вікна
root = tk.Tk()
root.title("Головне вікно")

translator_button = tk.Button(root, text="Перекладач", command=open_translator_window)
translator_button.pack()

search_button = tk.Button(root, text="Пошук", command=open_search_window)
search_button.pack()

root.mainloop()
