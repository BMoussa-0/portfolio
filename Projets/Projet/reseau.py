import tkinter as tk
from PIL import Image, ImageTk, ImageGrab
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import A4
import os
import sys

window = tk.Tk()
window.title("Simulateur de Schéma Réseau")
canvas = tk.Canvas(window, width=800, height=600, bg="white")
canvas.pack()

image_routeur = Image.open("images/1257487.png")
image_switch = Image.open("images/switch.png")
image_ordinateur = Image.open("images/ordinateur.png")

largeur, hauteur = 50, 50
image_routeur = image_routeur.resize((largeur, hauteur), Image.Resampling.LANCZOS)
image_routeur_tk = ImageTk.PhotoImage(image_routeur)
image_switch = image_switch.resize((largeur, hauteur), Image.Resampling.LANCZOS)
image_switch_tk = ImageTk.PhotoImage(image_switch)
image_ordinateur = image_ordinateur.resize((largeur, hauteur), Image.Resampling.LANCZOS)
image_pc_tk = ImageTk.PhotoImage(image_ordinateur)

selected_object = None
cable_start_x = None
cable_start_y = None
cable_end_x = None
cable_end_y = None
drawing_cable = False
selected_cable_end = None

def ajouter_equipement(equipement):
    x, y = 100, 100
    if equipement == "routeur":
        obj = canvas.create_image(x, y, image=image_routeur_tk, tags=("routeur", "equipment"))
    elif equipement == "switch":
        obj = canvas.create_image(x, y, image=image_switch_tk, tags=("switch", "equipment"))
    elif equipement == "ordinateur":
        obj = canvas.create_image(x, y, image=image_pc_tk, tags=("ordinateur", "equipment"))
    elif equipement == "cable":
        global drawing_cable
        drawing_cable = True
        return
    canvas.itemconfig(obj, tags=(str(obj), "equipment"))

def start_cable(event):
    global cable_start_x, cable_start_y, drawing_cable
    if drawing_cable:
        cable_start_x = event.x
        cable_start_y = event.y
        # Créer un câble temporaire
        obj = canvas.create_line(cable_start_x, cable_start_y, cable_start_x, cable_start_y, width=2, fill="black", tags=("cable"))
        canvas.itemconfig(obj, tags=(str(obj), "cable"))
        global selected_object
        selected_object = obj

def drag_cable(event):
    global drawing_cable, selected_object
    if drawing_cable and selected_object:
        # Mettre à jour le point final du câble pendant le déplacement
        cable_coords = canvas.coords(selected_object)
        canvas.coords(selected_object, cable_coords[0], cable_coords[1], event.x, event.y)

def end_cable(event):
    global drawing_cable, selected_object
    if drawing_cable:
        drawing_cable = False
        selected_object = None

def clic_objet(event):
    global selected_object, selected_cable_end
    objet_cible = canvas.find_closest(event.x, event.y)
    if objet_cible:
        tags = canvas.gettags(objet_cible[0])
        if "cable" in tags:
            # Déterminer quelle extrémité du câble est la plus proche
            coords = canvas.coords(objet_cible[0])
            start_dist = ((coords[0] - event.x) ** 2 + (coords[1] - event.y) ** 2) ** 0.5
            end_dist = ((coords[2] - event.x) ** 2 + (coords[3] - event.y) ** 2) ** 0.5
            
            selected_object = objet_cible[0]
            selected_cable_end = "start" if start_dist < end_dist else "end"
        else:
            selected_object = objet_cible[0]
            selected_cable_end = None

def deplacer_objet(event):
    global selected_object, selected_cable_end
    if selected_object:
        tags = canvas.gettags(selected_object)
        if "cable" in tags:
            coords = canvas.coords(selected_object)
            if selected_cable_end == "start":
                canvas.coords(selected_object, event.x, event.y, coords[2], coords[3])
            elif selected_cable_end == "end":
                canvas.coords(selected_object, coords[0], coords[1], event.x, event.y)
        else:
            dx = event.x - canvas.coords(selected_object)[0]
            dy = event.y - canvas.coords(selected_object)[1]
            canvas.move(selected_object, dx, dy)

def supprimer_objet():
    global selected_object
    if selected_object:
        canvas.delete(selected_object)
        selected_object = None        

def exporter_pdf():
    # Capturer le canvas en image
    # Gérer le cas de différents OS pour la capture d'écran
    if sys.platform == "win32":
        # Pour Windows
        x = window.winfo_rootx() + canvas.winfo_x()
        y = window.winfo_rooty() + canvas.winfo_y()
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        image = ImageGrab.grab(bbox=(x, y, x+width, y+height))
    else:
        # Pour Linux/Mac
        canvas.update()
        canvas.postscript(file="temp.eps", colormode='color')
        image = Image.open("temp.eps")
    
    # Sauvegarder temporairement l'image
    image.save("temp_canvas.png", "PNG")
    
    # Créer le PDF
    c = pdf_canvas.Canvas("schema_reseau.pdf", pagesize=A4)
    
    # Obtenir les dimensions de la page A4
    a4_width, a4_height = A4
    
    # Calculer les dimensions pour adapter l'image à la page A4
    img_width = image.width
    img_height = image.height
    aspect = img_height / float(img_width)
    
    # Définir la largeur maximale sur la page (avec marges)
    max_width = a4_width - 40  # 20 pixels de marge de chaque côté
    max_height = a4_height - 40
    
    # Calculer les dimensions finales
    if img_width > max_width:
        new_width = max_width
        new_height = new_width * aspect
        if new_height > max_height:
            new_height = max_height
            new_width = new_height / aspect
    else:
        new_width = img_width
        new_height = img_height
    
    # Dessiner l'image sur le PDF
    c.drawImage("temp_canvas.png", 20, a4_height - new_height - 20, 
                width=new_width, height=new_height)
    
    # Ajouter un titre
    c.setFont("Helvetica-Bold", 16)
    c.drawString(20, a4_height - 15, "Schéma Réseau")
    
    # Sauvegarder le PDF
    c.save()
    
    # Nettoyer les fichiers temporaires
    if os.path.exists("temp_canvas.png"):
        os.remove("temp_canvas.png")
    if os.path.exists("temp.eps"):
        os.remove("temp.eps")
    
    print("PDF exporté avec succès : schema_reseau.pdf")

canvas.bind("<Button-1>", lambda e: start_cable(e) if drawing_cable else clic_objet(e))
canvas.bind("<B1-Motion>", lambda e: drag_cable(e) if drawing_cable else deplacer_objet(e))
canvas.bind("<ButtonRelease-1>", end_cable)


btn_routeur = tk.Button(window, text="Ajouter Routeur", command=lambda: ajouter_equipement("routeur"))
btn_routeur.pack(side=tk.LEFT)
btn_switch = tk.Button(window, text="Ajouter Switch", command=lambda: ajouter_equipement("switch"))
btn_switch.pack(side=tk.LEFT)
btn_ordinateur = tk.Button(window, text="Ajouter Ordinateur", command=lambda: ajouter_equipement("ordinateur"))
btn_ordinateur.pack(side=tk.LEFT)
btn_cable = tk.Button(window, text="Ajouter Cable", command=lambda: ajouter_equipement("cable"))
btn_cable.pack(side=tk.LEFT)
btn_supprimer = tk.Button(window, text="Supprimer", command=supprimer_objet)
btn_supprimer.pack(side=tk.LEFT)
btn_export = tk.Button(window, text="Exporter PDF", command=exporter_pdf)
btn_export.pack(side=tk.LEFT)


window.mainloop()
