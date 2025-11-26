import tkinter as tk
from tkinter import filedialog, messagebox
from steganography import Steganography

class ModernSteganographyGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("StegoLab • Стеганография")
        self.root.geometry("900x750")
        self.root.configure(bg='#000000')
        
        # Текущая тема
        self.dark_theme = True
        self.setup_themes()
        
        self.steganography = Steganography()
        self.setup_ui()
    
    def setup_themes(self):
        # Темная тема (основная)
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
    
    def toggle_theme(self):
        self.dark_theme = not self.dark_theme
        self.apply_theme()
    
    def apply_theme(self):
        bg = self.get_color('bg')
        card_bg = self.get_color('card_bg')
        text_primary = self.get_color('text_primary')
        text_secondary = self.get_color('text_secondary')
        border = self.get_color('border')
        
        self.root.configure(bg=bg)
        
        # Обновляем все виджеты
        for widget in self.root.winfo_children():
            self.update_widget_theme(widget)
    
    def update_widget_theme(self, widget):
        bg = self.get_color('bg')
        card_bg = self.get_color('card_bg')
        text_primary = self.get_color('text_primary')
        text_secondary = self.get_color('text_secondary')
        border = self.get_color('border')
        
        if isinstance(widget, (tk.Frame, tk.LabelFrame)):
            widget.configure(bg=card_bg)
            for child in widget.winfo_children():
                self.update_widget_theme(child)
        elif isinstance(widget, tk.Label):
            if 'card' in str(widget):
                widget.configure(bg=card_bg, fg=text_primary)
            else:
                widget.configure(bg=bg, fg=text_primary)
        elif isinstance(widget, tk.Button):
            if 'accent' in str(widget):
                widget.configure(bg=self.get_color('accent'), fg='white')
            else:
                widget.configure(bg=card_bg, fg=text_primary, highlightbackground=border)
        elif isinstance(widget, (tk.Entry, tk.Text)):
            widget.configure(bg=card_bg, fg=text_primary, insertbackground=text_primary,
                           selectbackground=self.get_color('accent'))
        elif isinstance(widget, tk.Scrollbar):
            widget.configure(bg=border)
    
    def create_modern_button(self, parent, text, command, accent=False, width=20):
        bg = self.get_color('accent') if accent else self.get_color('card_bg')
        fg = 'white' if accent else self.get_color('text_primary')
        hover_bg = self.get_color('accent_hover') if accent else self.get_color('glass_effect')
        
        btn = tk.Button(parent, text=text, command=command, bg=bg, fg=fg,
                       font=('SF Pro Display', 11, 'bold' if accent else 'normal'),
                       border=0, relief='flat', cursor='hand2', width=width,
                       padx=20, pady=12)
        
        # Эффект при наведении
        def on_enter(e):
            btn.configure(bg=hover_bg)
        def on_leave(e):
            btn.configure(bg=bg)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    def create_card(self, parent, title=None, padding=20):
        card = tk.Frame(parent, bg=self.get_color('card_bg'), relief='flat',
                       highlightbackground=self.get_color('border'), highlightthickness=1)
        
        if title:
            title_label = tk.Label(card, text=title, bg=self.get_color('card_bg'),
                                  fg=self.get_color('text_primary'), font=('SF Pro Display', 12, 'bold'))
            title_label.pack(anchor='w', padx=padding, pady=(padding, 10))
        
        content_frame = tk.Frame(card, bg=self.get_color('card_bg'))
        content_frame.pack(fill='both', expand=True, padx=padding, pady=(0, padding))
        
        return card, content_frame
    
    def setup_ui(self):
        # Хедер с переключением темы
        header_frame = tk.Frame(self.root, bg=self.get_color('bg'), height=80)
        header_frame.pack(fill='x', padx=30, pady=20)
        header_frame.pack_propagate(False)
        
        # Логотип и название
        logo_frame = tk.Frame(header_frame, bg=self.get_color('bg'))
        logo_frame.pack(side='left')
        
        title_label = tk.Label(logo_frame, text="StegoLab", bg=self.get_color('bg'),
                              fg=self.get_color('text_primary'), font=('SF Pro Display', 24, 'bold'))
        title_label.pack(anchor='w')
        
        subtitle_label = tk.Label(logo_frame, text="Стеганографическая лаборатория", 
                                 bg=self.get_color('bg'), fg=self.get_color('accent'),
                                 font=('SF Pro Display', 11))
        subtitle_label.pack(anchor='w')
        
        # Кнопка переключения темы
        theme_btn = self.create_modern_button(header_frame, "🌓 Сменить тему", self.toggle_theme)
        theme_btn.pack(side='right')
        
        # Основной контент
        main_container = tk.Frame(self.root, bg=self.get_color('bg'))
        main_container.pack(fill='both', expand=True, padx=30, pady=(0, 30))
        
        # Две колонки
        left_column = tk.Frame(main_container, bg=self.get_color('bg'))
        left_column.pack(side='left', fill='both', expand=True, padx=(0, 15))
        
        right_column = tk.Frame(main_container, bg=self.get_color('bg'))
        right_column.pack(side='right', fill='both', expand=True, padx=(15, 0))
        
        # Левая колонка - входные данные
        self.setup_input_section(left_column)
        self.setup_control_section(left_column)
        
        # Правая колонка - информация и результаты
        self.setup_info_section(right_column)
        self.setup_result_section(right_column)
        
        self.apply_theme()
    
    def setup_input_section(self, parent):
        # Карточка изображения
        image_card, image_content = self.create_card(parent, "📸 ИСХОДНОЕ ИЗОБРАЖЕНИЕ")
        image_card.pack(fill='x', pady=(0, 15))
        
        # Поле пути
        path_frame = tk.Frame(image_content, bg=self.get_color('card_bg'))
        path_frame.pack(fill='x', pady=5)
        
        self.image_path = tk.StringVar()
        path_entry = tk.Entry(path_frame, textvariable=self.image_path, 
                             bg=self.get_color('card_bg'), fg=self.get_color('text_primary'),
                             font=('SF Pro Text', 10), relief='flat', highlightthickness=1,
                             highlightbackground=self.get_color('border'), highlightcolor=self.get_color('accent'),
                             insertbackground=self.get_color('text_primary'))
        path_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        browse_btn = self.create_modern_button(path_frame, "ОБЗОР", self.browse_image, accent=True, width=8)
        browse_btn.pack(side='right')
        
        # Карточка сообщения
        message_card, message_content = self.create_card(parent, "💬 СООБЩЕНИЕ")
        message_card.pack(fill='both', expand=True, pady=(0, 15))
        
        self.text_input = tk.Text(message_content, height=8, bg=self.get_color('card_bg'), 
                                 fg=self.get_color('text_primary'), font=('SF Pro Text', 10),
                                 relief='flat', wrap='word', padx=10, pady=10,
                                 highlightthickness=1, highlightbackground=self.get_color('border'),
                                 insertbackground=self.get_color('text_primary'))
        
        scrollbar = tk.Scrollbar(message_content, command=self.text_input.yview)
        self.text_input.config(yscrollcommand=scrollbar.set)
        
        self.text_input.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Счетчик символов
        self.char_count_label = tk.Label(message_content, text="0 символов", 
                                        bg=self.get_color('card_bg'), fg=self.get_color('text_secondary'),
                                        font=('SF Pro Text', 9))
        self.char_count_label.pack(anchor='e', pady=(5, 0))
        
        self.text_input.bind('<KeyRelease>', self.update_char_count)
    
    def setup_control_section(self, parent):
        control_card, control_content = self.create_card(parent, "⚙️ ДЕЙСТВИЯ")
        control_card.pack(fill='x')
        
        # Основные кнопки
        btn_frame = tk.Frame(control_content, bg=self.get_color('card_bg'))
        btn_frame.pack(fill='x', pady=10)
        
        embed_btn = self.create_modern_button(btn_frame, "🔼 ВСТРОИТЬ", self.embed_message, accent=True)
        embed_btn.pack(side='left', fill='x', expand=True, padx=(0, 8))
        
        extract_btn = self.create_modern_button(btn_frame, "🔽 ИЗВЛЕЧЬ", self.extract_message, accent=True)
        extract_btn.pack(side='left', fill='x', expand=True, padx=8)
        
        clear_btn = self.create_modern_button(btn_frame, "ОЧИСТИТЬ", self.clear_all)
        clear_btn.pack(side='left', fill='x', expand=True, padx=(8, 0))
        
        # Настройки
        settings_frame = tk.Frame(control_content, bg=self.get_color('card_bg'))
        settings_frame.pack(fill='x', pady=(15, 0))
        
        tk.Label(settings_frame, text="Битов на канал:", bg=self.get_color('card_bg'),
                fg=self.get_color('text_primary'), font=('SF Pro Text', 10)).pack(side='left')
        
        self.bits_var = tk.StringVar(value="1")
        bits_spinbox = tk.Spinbox(settings_frame, from_=1, to=4, width=4, 
                                 textvariable=self.bits_var, command=self.update_bits,
                                 bg=self.get_color('card_bg'), fg=self.get_color('text_primary'),
                                 font=('SF Pro Text', 10), relief='flat',
                                 highlightthickness=1, highlightbackground=self.get_color('border'),
                                 buttonbackground=self.get_color('accent'))
        bits_spinbox.pack(side='left', padx=10)
    
    def setup_info_section(self, parent):
        info_card, info_content = self.create_card(parent, "📊 АНАЛИТИКА")
        info_card.pack(fill='x', pady=(0, 15))
        
        self.capacity_label = tk.Label(info_content, text="Загрузите изображение для анализа", 
                                      bg=self.get_color('card_bg'), fg=self.get_color('text_primary'),
                                      justify='left', font=('SF Pro Text', 10), wraplength=350)
        self.capacity_label.pack(fill='x', pady=10)
    
    def setup_result_section(self, parent):
        result_card, result_content = self.create_card(parent, "📋 РЕЗУЛЬТАТ")
        result_card.pack(fill='both', expand=True)
        
        self.result_text = tk.Text(result_content, height=12, bg=self.get_color('card_bg'),
                                  fg=self.get_color('text_primary'), font=('SF Mono', 10),
                                  relief='flat', wrap='word', padx=15, pady=15,
                                  highlightthickness=1, highlightbackground=self.get_color('border'),
                                  insertbackground=self.get_color('text_primary'))
        
        scrollbar = tk.Scrollbar(result_content, command=self.result_text.yview)
        self.result_text.config(yscrollcommand=scrollbar.set)
        
        self.result_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def browse_image(self):
        filename = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff")]
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
            
            self.steganography.image_processor.load_image(image_path)
            pixels = self.steganography.image_processor.get_pixels()
            max_chars = self.steganography.calculate_capacity(pixels)
            
            width, height = self.steganography.image_processor.size
            bits = self.steganography.lsb_algorithm.bits_per_channel
            
            info_text = (f"▫️ Размер: {width} × {height} px\n"
                        f"▫️ Битов на канал: {bits}\n"
                        f"▫️ Макс. вместимость: {max_chars} симв.\n"
                        f"▫️ Рекомендуется: {max_chars - 10} симв.")
            
            self.capacity_label.config(text=info_text)
            
        except Exception as e:
            self.capacity_label.config(text=f"❌ Ошибка: {str(e)}")
    
    def update_bits(self):
        try:
            bits = int(self.bits_var.get())
            if 1 <= bits <= 4:
                self.steganography = Steganography(bits)
                self.check_capacity()
        except ValueError:
            pass
    
    def update_char_count(self, event=None):
        text = self.text_input.get("1.0", tk.END).strip()
        char_count = len(text)
        self.char_count_label.config(text=f"{char_count} символов")
        
        try:
            image_path = self.image_path.get()
            if image_path:
                self.steganography.image_processor.load_image(image_path)
                pixels = self.steganography.image_processor.get_pixels()
                max_chars = self.steganography.calculate_capacity(pixels)
                
                if char_count > max_chars:
                    self.char_count_label.config(fg=self.get_color('error'))
                else:
                    self.char_count_label.config(fg=self.get_color('success'))
        except:
            pass
    
    def embed_message(self):
        try:
            image_path = self.image_path.get()
            text = self.text_input.get("1.0", tk.END).strip()
            
            if not image_path:
                self.show_result("❌ Выберите изображение")
                messagebox.showerror("Ошибка", "Выберите изображение")
                return
                
            if not text:
                self.show_result("❌ Введите сообщение")
                messagebox.showerror("Ошибка", "Введите сообщение для встраивания")
                return
            
            self.steganography.image_processor.load_image(image_path)
            pixels = self.steganography.image_processor.get_pixels()
            max_chars = self.steganography.calculate_capacity(pixels)
            
            if len(text) > max_chars:
                self.show_result(f"❌ Сообщение слишком длинное\n\n"
                               f"Максимум: {max_chars} символов\n"
                               f"Ваше: {len(text)} символов")
                messagebox.showerror("Ошибка", f"Сообщение слишком длинное!\nМаксимум: {max_chars} символов")
                return
            
            output_path = filedialog.asksaveasfilename(
                title="Сохранить изображение со скрытым сообщением",
                defaultextension=".png",
                filetypes=[("PNG files", "*.png")]
            )
            
            if output_path:
                self.show_result("⏳ Встраивание сообщения...")
                self.root.update()
                
                success = self.steganography.embed_message(image_path, text, output_path)
                if success:
                    info_text = (f"✅ Сообщение встроено!\n\n"
                               f"▫️ Файл: {output_path}\n"
                               f"▫️ Размер: {self.steganography.image_processor.size}\n"
                               f"▫️ Битов: {self.steganography.lsb_algorithm.bits_per_channel}\n"
                               f"▫️ Использовано: {len(text)}/{max_chars} симв.\n\n"
                               f"💡 Для извлечения используйте эту программу")
                    
                    self.show_result(info_text)
                    messagebox.showinfo("Успех", "✅ Сообщение успешно встроено!")
                
        except Exception as e:
            error_msg = f"❌ Ошибка при встраивании:\n{str(e)}"
            self.show_result(error_msg)
            messagebox.showerror("Ошибка", error_msg)
    
    def extract_message(self):
        try:
            image_path = self.image_path.get()
            
            if not image_path:
                self.show_result("❌ Выберите изображение")
                messagebox.showerror("Ошибка", "Выберите изображение")
                return
            
            self.show_result("⏳ Извлечение сообщения...")
            self.root.update()
            
            text = self.steganography.extract_message(image_path)
            
            if text:
                info_text = (f"✅ Сообщение извлечено!\n\n"
                           f"▫️ Размер: {self.steganography.image_processor.size}\n"
                           f"▫️ Битов: {self.steganography.lsb_algorithm.bits_per_channel}\n"
                           f"▫️ Длина: {len(text)} символов\n\n"
                           f"📝 Текст:\n{'─'*40}\n{text}\n{'─'*40}")
                
                self.show_result(info_text)
                messagebox.showinfo("Результат", f"✅ Сообщение извлечено!\n\n{text}")
            else:
                self.show_result("❌ Сообщение не найдено")
                messagebox.showwarning("Результат", "Сообщение не найдено")
            
        except Exception as e:
            error_msg = f"❌ Ошибка при извлечении:\n{str(e)}"
            self.show_result(error_msg)
            messagebox.showerror("Ошибка", error_msg)
    
    def show_result(self, message: str):
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", message)
    
    def clear_all(self):
        self.image_path.set("")
        self.text_input.delete("1.0", tk.END)
        self.result_text.delete("1.0", tk.END)
        self.capacity_label.config(text="Загрузите изображение для анализа")
        self.char_count_label.config(text="0 символов", fg=self.get_color('text_secondary'))
    
    def run(self):
        self.root.mainloop()

# Для обратной совместимости
SteganographyGUI = ModernSteganographyGUI