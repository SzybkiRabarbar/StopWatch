from tkinter import Tk, font
import csv

root = Tk()
font_names = font.families()

with open('DB\\font_names.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for font_name in font_names:
        writer.writerow([font_name])