from tkinter import *
import tkinter as tk
import requests
import json
from tkinter import messagebox


class Cine():

    def __init__(self, api_key):
        self.__api_key = api_key
        self.__base_url = 'https://api.themoviedb.org/3'
        self.__generos = self.obtener_generos()
        self.__peliculas = self.obtener_peliculas()
        self.__ventana = tk.Tk()
        self.__ventana.title('Cinéfilos Argentinos')
        self.__ventana.geometry('400x320')
        self.__listabox = tk.Listbox(self.__ventana)
        self.__listabox.pack(expand=True, fill=tk.BOTH)
        for pelicula in self.__peliculas:
            self.__listabox.insert(tk.END, pelicula['title'])
        self.__listabox.bind('<Double-Button-1>', self.mostrar_peliculas)
        self.__ventana.mainloop()

    def obtener_generos(self):
        generos = {}

        with open('genres.json', 'r') as file:
            data = json.load(file)
            for genero in data['genres']:
                generos[genero['id']] = genero['name']

        return generos

    def obtener_peliculas(self):
        peliculas = []
        try:
            url = f'{self.__base_url}/discover/movie?api_key={self.__api_key}&language=es'
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            peliculas = data['results']
        except requests.exceptions.RequestException as error:
            messagebox.showerror('Error en la conexion', str(error))
        return peliculas

    def mostrar_peliculas(self, event):
        widget = event.widget
        indice = int(widget.curselection()[0])
        pelicula = self.__peliculas[indice]
        generos = []
        for id_gen in pelicula['genre_ids']:
            genero = self.__generos.get(id_gen)
            if genero:
                generos.append(genero)
        generos_str = ','.join(generos)  #Combina los elementos de la lista generos en una sola cadena separada por comas.
        if pelicula:
            ventana_pelicula = Toplevel(self.__ventana)  #Se crea una nueva ventana
            ventana_pelicula.title(pelicula['title'])
            etiqueta_titulo = Label(ventana_pelicula, text=f"Título: {pelicula['title']}")
            etiqueta_titulo.pack(anchor='w')
            etiqueta_resumen = Label(ventana_pelicula, text=f"Resumen: {pelicula['overview']}", wraplength=400)
            etiqueta_resumen.pack(anchor='w')
            etiqueta_lenguaje = Label(ventana_pelicula, text=f"Lenguaje Original: {pelicula['original_language']}")
            etiqueta_lenguaje.pack(anchor='w')
            etiqueta_fecha = Label(ventana_pelicula, text=f"Fecha de Lanzamiento: {pelicula['release_date']}")
            etiqueta_fecha.pack(anchor='w')
            etiqueta_genero = Label(ventana_pelicula, text=f"Género: {generos_str}")
            etiqueta_genero.pack(anchor='w')


def test():
    api_key = '430cf528a46775985b9fc5d23ed47254'
    app = Cine(api_key)


if __name__ == '__main__':
    test()
