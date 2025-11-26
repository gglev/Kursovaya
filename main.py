import tkinter as tk
from interface import SteganographyGUI

def main():
    try:
        app = SteganographyGUI()
        app.run()
    except Exception as e:
        print(f"Ошибка запуска приложения: {str(e)}")

if __name__ == "__main__":
    main()