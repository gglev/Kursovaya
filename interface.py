import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from steganography import Steganography
import os

class ModernSteganographyGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("StegoLab • Стеганография с шифрованием")
        self.root.geometry("1000x850")
        self.root.configure(bg='#000000')
        
        self.dark_theme = True
        self.setup_themes()
        
        self.steganography = Steganography()
        self.current_password = None
        self.setup_ui()
    
    def setup_themes(self):
        # Темная тема
        self.dark_theme_colors = {
            'bg': '#0a0a0a',
            'card_bg': '#1a1a1a',
            'accent': '#ff3366',
            'accent_hover': '#ff5588',
            'text_primary': '#ffffff',
            'text_secondary': '#888888',
            'border': '#333333',
            'success': '#00d4aa',
            'warning': '#ffaa00',
            'error': '#ff4444',
            'glass_effect': 'rgba(255,255,255,0.05)'
        }
        
        # Светлая тема
        self.light_theme_colors = {
            'bg': '#f8f9fa',
            'card_bg': '#ffffff',
            'accent': '#ff3366',
            'accent_hover': '#ff5588',
            'text_primary': '#2c2c2c',
            'text_secondary': '#666666',
            'border': '#e0e0e0',
            'success': '#00a085',
            'warning': '#cc8800',
            'error': '#cc3333',
            'glass_effect': 'rgba(0,0,0,0.03)'
        }
    
    def get_color(self, color_name):
        theme = self.dark_theme_colors if self.dark_theme else self.light_theme_colors
        return theme[color_name]
    
    def setup_ui(self):
        # Хедер
        header_frame = tk.Frame(self.root, bg=self.get_color('bg'), height=80)
        header_frame.pack(fill='x', padx=30, pady=20)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="StegoLab", bg=self.get_color('bg'),
                              fg=self.get_color('text_primary'), font=('SF Pro Display', 24, 'bold'))
        title_label.pack(side='left')
        
        subtitle_label = tk.Label(header_frame, text="Стеганография с AES-256 шифрованием", 
                                 bg=self.get_color('bg'), fg=self.get_color('accent'),
                                 font=('SF Pro Display', 11))
        subtitle_label.pack(side='left', padx=(10, 0))
        
        # Основной контент
        main_container = tk.Frame(self.root, bg=self.get_color('bg'))
        main_container.pack(fill='both', expand=True, padx=30, pady=(0, 30))
        
        # Две колонки
        left_column = tk.Frame(main_container, bg=self.get_color('bg'))
        left_column.pack(side='left', fill='both', expand=True, padx=(0, 15))
        
        right_column = tk.Frame(main_container, bg=self.get_color('bg'))
        right_column.pack(side='right', fill='both', expand=True, padx=(15, 0))
        
        # Левая колонка
        self.setup_input_section(left_column)
        self.setup_password_section(left_column)
        self.setup_control_section(left_column)
        
        # Правая колонка
        self.setup_info_section(right_column)
        self.setup_result_section(right_column)
        
        self.apply_theme()
    
    def setup_input_section(self, parent):
        # Карточка изображения
        image_card = tk.Frame(parent, bg=self.get_color('card_bg'), relief='flat',
                             highlightbackground=self.get_color('border'), highlightthickness=1)
        image_card.pack(fill='x', pady=(0, 15))
        
        tk.Label(image_card, text="📸 ИСХОДНОЕ ИЗОБРАЖЕНИЕ", bg=self.get_color('card_bg'),
                fg=self.get_color('text_primary'), font=('SF Pro Display', 12, 'bold')).pack(anchor='w', padx=20, pady=(20, 10))
        
        content_frame = tk.Frame(image_card, bg=self.get_color('card_bg'))
        content_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Поле пути
        path_frame = tk.Frame(content_frame, bg=self.get_color('card_bg'))
        path_frame.pack(fill='x', pady=5)
        
        self.image_path = tk.StringVar()
        path_entry = tk.Entry(path_frame, textvariable=self.image_path, 
                             bg=self.get_color('card_bg'), fg=self.get_color('text_primary'),
                             font=('SF Pro Text', 10), relief='flat', highlightthickness=1,
                             highlightbackground=self.get_color('border'), highlightcolor=self.get_color('accent'),
                             insertbackground=self.get_color('text_primary'), width=40)
        path_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        browse_btn = tk.Button(path_frame, text="ОБЗОР", command=self.browse_image,
                              bg=self.get_color('accent'), fg='white', font=('SF Pro Display', 10, 'bold'),
                              border=0, relief='flat', cursor='hand2', padx=15, pady=8)
        browse_btn.pack(side='right')
        
        # Форматы файлов
        format_label = tk.Label(content_frame, text="Поддерживаемые форматы: PNG, BMP, JPG", 
                               bg=self.get_color('card_bg'), fg=self.get_color('text_secondary'),
                               font=('SF Pro Text', 9))
        format_label.pack(anchor='w', pady=(5, 0))
    
    def setup_password_section(self, parent):
        # Карточка пароля
        password_card = tk.Frame(parent, bg=self.get_color('card_bg'), relief='flat',
                                highlightbackground=self.get_color('border'), highlightthickness=1)
        password_card.pack(fill='x', pady=(0, 15))
        
        tk.Label(password_card, text="🔐 НАСТРОЙКИ БЕЗОПАСНОСТИ", bg=self.get_color('card_bg'),
                fg=self.get_color('text_primary'), font=('SF Pro Display', 12, 'bold')).pack(anchor='w', padx=20, pady=(20, 10))
        
        content_frame = tk.Frame(password_card, bg=self.get_color('card_bg'))
        content_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Поле пароля
        password_frame = tk.Frame(content_frame, bg=self.get_color('card_bg'))
        password_frame.pack(fill='x', pady=5)
        
        tk.Label(password_frame, text="Пароль:", bg=self.get_color('card_bg'),
                fg=self.get_color('text_primary'), font=('SF Pro Text', 10)).pack(side='left')
        
        self.password_var = tk.StringVar()
        # ВАЖНО: сохраняем поле ввода как атрибут класса
        self.password_entry = tk.Entry(password_frame, textvariable=self.password_var, show="*",
                                     bg=self.get_color('card_bg'), fg=self.get_color('text_primary'),
                                     font=('SF Pro Text', 10), relief='flat', highlightthickness=1,
                                     highlightbackground=self.get_color('border'), highlightcolor=self.get_color('accent'),
                                     insertbackground=self.get_color('text_primary'), width=30)
        self.password_entry.pack(side='left', padx=(10, 20))
        
        # Чекбокс для отображения пароля
        self.show_password_var = tk.BooleanVar(value=False)
        self.show_password_cb = tk.Checkbutton(password_frame, text="Показать пароль", 
                                             variable=self.show_password_var,
                                             bg=self.get_color('card_bg'), fg=self.get_color('text_primary'),
                                             font=('SF Pro Text', 9), 
                                             command=self.toggle_password_visibility)
        self.show_password_cb.pack(side='left')
        
        # Информация о шифровании
        info_label = tk.Label(content_frame, text="Шифрование: AES-256\nХеширование: SHA-256", 
                             bg=self.get_color('card_bg'), fg=self.get_color('text_secondary'),
                             font=('SF Pro Text', 9), justify='left')
        info_label.pack(anchor='w', pady=(10, 0))
    
    def toggle_password_visibility(self):
        """Переключение видимости пароля"""
        if hasattr(self, 'password_entry'):
            if self.show_password_var.get():
                self.password_entry.config(show="")
                self.show_password_cb.config(text="Скрыть пароль")
            else:
                self.password_entry.config(show="*")
                self.show_password_cb.config(text="Показать пароль")
    
    def setup_control_section(self, parent):
        control_card = tk.Frame(parent, bg=self.get_color('card_bg'), relief='flat',
                               highlightbackground=self.get_color('border'), highlightthickness=1)
        control_card.pack(fill='x', pady=(0, 15))
        
        tk.Label(control_card, text="⚙️ ДЕЙСТВИЯ", bg=self.get_color('card_bg'),
                fg=self.get_color('text_primary'), font=('SF Pro Display', 12, 'bold')).pack(anchor='w', padx=20, pady=(20, 10))
        
        content_frame = tk.Frame(control_card, bg=self.get_color('card_bg'))
        content_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Кнопки
        btn_frame = tk.Frame(content_frame, bg=self.get_color('card_bg'))
        btn_frame.pack(fill='x', pady=10)
        
        embed_btn = tk.Button(btn_frame, text="🔼 ВСТРОИТЬ СООБЩЕНИЕ", command=self.embed_message,
                             bg=self.get_color('accent'), fg='white', font=('SF Pro Display', 11, 'bold'),
                             border=0, relief='flat', cursor='hand2', padx=20, pady=12)
        embed_btn.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        extract_btn = tk.Button(btn_frame, text="🔽 ИЗВЛЕЧЬ СООБЩЕНИЕ", command=self.extract_message,
                               bg=self.get_color('accent'), fg='white', font=('SF Pro Display', 11, 'bold'),
                               border=0, relief='flat', cursor='hand2', padx=20, pady=12)
        extract_btn.pack(side='left', fill='x', expand=True, padx=10)
        
        clear_btn = tk.Button(btn_frame, text="ОЧИСТИТЬ ВСЕ", command=self.clear_all,
                             bg=self.get_color('card_bg'), fg=self.get_color('text_primary'),
                             font=('SF Pro Display', 11), border=0, relief='flat',
                             cursor='hand2', padx=20, pady=12)
        clear_btn.pack(side='left', fill='x', expand=True, padx=(10, 0))
    
    def setup_info_section(self, parent):
        info_card = tk.Frame(parent, bg=self.get_color('card_bg'), relief='flat',
                            highlightbackground=self.get_color('border'), highlightthickness=1)
        info_card.pack(fill='x', pady=(0, 15))
        
        tk.Label(info_card, text="📊 ИНФОРМАЦИЯ О ИЗОБРАЖЕНИИ", bg=self.get_color('card_bg'),
                fg=self.get_color('text_primary'), font=('SF Pro Display', 12, 'bold')).pack(anchor='w', padx=20, pady=(20, 10))
        
        content_frame = tk.Frame(info_card, bg=self.get_color('card_bg'))
        content_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        self.capacity_label = tk.Label(content_frame, text="Загрузите изображение для анализа", 
                                      bg=self.get_color('card_bg'), fg=self.get_color('text_primary'),
                                      justify='left', font=('SF Pro Text', 10), wraplength=350)
        self.capacity_label.pack(fill='x', pady=10)
    
    def setup_result_section(self, parent):
        # Карточка сообщения
        message_card = tk.Frame(parent, bg=self.get_color('card_bg'), relief='flat',
                               highlightbackground=self.get_color('border'), highlightthickness=1)
        message_card.pack(fill='both', expand=True, pady=(0, 15))
        
        tk.Label(message_card, text="💬 ВВОД СООБЩЕНИЯ", bg=self.get_color('card_bg'),
                fg=self.get_color('text_primary'), font=('SF Pro Display', 12, 'bold')).pack(anchor='w', padx=20, pady=(20, 10))
        
        content_frame = tk.Frame(message_card, bg=self.get_color('card_bg'))
        content_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        self.text_input = tk.Text(content_frame, height=6, bg=self.get_color('card_bg'), 
                                 fg=self.get_color('text_primary'), font=('SF Pro Text', 10),
                                 relief='flat', wrap='word', padx=10, pady=10,
                                 highlightthickness=1, highlightbackground=self.get_color('border'),
                                 insertbackground=self.get_color('text_primary'))
        
        scrollbar = tk.Scrollbar(content_frame, command=self.text_input.yview)
        self.text_input.config(yscrollcommand=scrollbar.set)
        
        self.text_input.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Счетчик символов
        self.char_count_label = tk.Label(content_frame, text="0 символов", 
                                        bg=self.get_color('card_bg'), fg=self.get_color('text_secondary'),
                                        font=('SF Pro Text', 9))
        self.char_count_label.pack(anchor='e', pady=(5, 0))
        
        self.text_input.bind('<KeyRelease>', self.update_char_count)
        
        # Карточка результатов
        result_card = tk.Frame(parent, bg=self.get_color('card_bg'), relief='flat',
                              highlightbackground=self.get_color('border'), highlightthickness=1)
        result_card.pack(fill='both', expand=True)
        
        tk.Label(result_card, text="📋 РЕЗУЛЬТАТ", bg=self.get_color('card_bg'),
                fg=self.get_color('text_primary'), font=('SF Pro Display', 12, 'bold')).pack(anchor='w', padx=20, pady=(20, 10))
        
        result_content = tk.Frame(result_card, bg=self.get_color('card_bg'))
        result_content.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        self.result_text = tk.Text(result_content, height=8, bg=self.get_color('card_bg'),
                                  fg=self.get_color('text_primary'), font=('SF Mono', 10),
                                  relief='flat', wrap='word', padx=15, pady=15,
                                  highlightthickness=1, highlightbackground=self.get_color('border'),
                                  insertbackground=self.get_color('text_primary'))
        
        result_scrollbar = tk.Scrollbar(result_content, command=self.result_text.yview)
        self.result_text.config(yscrollcommand=result_scrollbar.set)
        
        self.result_text.pack(side='left', fill='both', expand=True)
        result_scrollbar.pack(side='right', fill='y')
    
    def apply_theme(self):
        # Применяем тему ко всем виджетам
        pass
    
    def browse_image(self):
        filename = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=[
                ("Все поддерживаемые форматы", "*.png *.bmp *.jpg *.jpeg *.tiff"),
                ("PNG файлы", "*.png"),
                ("BMP файлы", "*.bmp"),
                ("JPEG файлы", "*.jpg *.jpeg"),
                ("Все файлы", "*.*")
            ]
        )
        if filename:
            self.image_path.set(filename)
            self.check_capacity()
    
    def check_capacity(self):
        try:
            image_path = self.image_path.get()
            if not image_path:
                self.capacity_label.config(text="Загрузите изображение для анализа")
                return
            
            info = self.steganography.get_image_info(image_path)
            width = info['width']
            height = info['height']
            max_chars = info['max_chars']
            max_bytes = info['max_bytes']
            bits = info['bits_per_channel']
            file_format = info['format']
            
            info_text = (f"▫️ Размер: {width} × {height} px\n"
                        f"▫️ Битов на канал: {bits}\n"
                        f"▫️ Макс. вместимость: {max_chars} симв.\n"
                        f"▫️ Макс. байт: {max_bytes}\n"
                        f"▫️ Формат: {file_format}")
            
            self.capacity_label.config(text=info_text)
            
        except Exception as e:
            self.capacity_label.config(text=f"❌ Ошибка: {str(e)}")
    
    def update_char_count(self, event=None):
        text = self.text_input.get("1.0", tk.END).strip()
        char_count = len(text)
        self.char_count_label.config(text=f"{char_count} символов")
    
    def embed_message(self):
        try:
            image_path = self.image_path.get()
            text = self.text_input.get("1.0", tk.END).strip()
            password = self.password_var.get()
            
            if not image_path:
                messagebox.showerror("Ошибка", "Выберите изображение")
                return
                
            if not text:
                messagebox.showerror("Ошибка", "Введите сообщение для встраивания")
                return
            
            # Запрашиваем подтверждение пароля
            if password:
                confirm_password = simpledialog.askstring("Подтверждение пароля", 
                                                         "Повторите пароль:", show='*')
                if confirm_password != password:
                    messagebox.showerror("Ошибка", "Пароли не совпадают")
                    return
            
            output_path = filedialog.asksaveasfilename(
                title="Сохранить стего-изображение",
                defaultextension=".png",
                filetypes=[
                    ("PNG файлы", "*.png"),
                    ("BMP файлы", "*.bmp"),
                    ("Все файлы", "*.*")
                ]
            )
            
            if output_path:
                self.show_result("⏳ Встраивание сообщения с шифрованием...")
                self.root.update()
                
                success = self.steganography.embed_message(image_path, text, output_path, password)
                if success:
                    info_text = (f"✅ Сообщение успешно встроено!\n\n"
                               f"▫️ Файл: {output_path}\n"
                               f"▫️ Размер: {self.steganography.image_processor.size}\n"
                               f"▫️ Шифрование: {'AES-256' if password else 'нет'}\n"
                               f"▫️ Использовано: {len(text)} символов\n"
                               f"▫️ Проверка целостности: ✅ включена")
                    
                    self.show_result(info_text)
                    messagebox.showinfo("Успех", "✅ Сообщение успешно встроено и защищено!")
                
        except Exception as e:
            error_msg = f"❌ Ошибка при встраивании:\n{str(e)}"
            self.show_result(error_msg)
            messagebox.showerror("Ошибка", error_msg)
    
    def extract_message(self):
        try:
            image_path = self.image_path.get()
            
            if not image_path:
                messagebox.showerror("Ошибка", "Выберите стего-изображение")
                return
            
            # Запрашиваем пароль если нужно
            password = None
            if messagebox.askyesno("Пароль", "Сообщение было защищено паролем?"):
                password = simpledialog.askstring("Ввод пароля", 
                                                 "Введите пароль для расшифровки:", show='*')
            
            self.show_result("⏳ Извлечение и проверка сообщения...")
            self.root.update()
            
            text = self.steganography.extract_message(image_path, password)
            
            if text:
                info_text = (f"✅ Сообщение успешно извлечено!\n\n"
                           f"▫️ Проверка целостности: ✅ пройдена\n"
                           f"▫️ Шифрование: {'AES-256' if password else 'нет'}\n"
                           f"▫️ Длина: {len(text)} символов\n\n"
                           f"📝 Текст:\n{'─'*40}\n{text}\n{'─'*40}")
                
                self.show_result(info_text)
                messagebox.showinfo("Результат", f"✅ Сообщение извлечено!\n\n{text}")
            else:
                self.show_result("❌ Сообщение не найдено или пароль неверен")
                messagebox.showwarning("Результат", "Сообщение не найдено. Возможно, неверный пароль или изображение повреждено.")
            
        except Exception as e:
            error_msg = f"❌ Ошибка при извлечении:\n{str(e)}"
            self.show_result(error_msg)
            messagebox.showerror("Ошибка", error_msg)
    
    def show_result(self, message: str):
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", message)
    
    def clear_all(self):
        self.image_path.set("")
        self.password_var.set("")
        if hasattr(self, 'password_entry'):
            self.password_entry.config(show="*")  # Сбрасываем показ пароля
        self.show_password_var.set(False)  # Сбрасываем чекбокс
        if hasattr(self, 'show_password_cb'):
            self.show_password_cb.config(text="Показать пароль")
        self.text_input.delete("1.0", tk.END)
        self.result_text.delete("1.0", tk.END)
        self.capacity_label.config(text="Загрузите изображение для анализа")
        self.char_count_label.config(text="0 символов")
    
    def run(self):
        self.root.mainloop()

# Для обратной совместимости
SteganographyGUI = ModernSteganographyGUI