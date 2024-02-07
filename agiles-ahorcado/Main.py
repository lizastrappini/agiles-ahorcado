import random


# Palabras disponibles
palabras_facil = [["sol", "Fuente principal de luz del sistema solar"], ["gato", "Animal doméstico de compañía"],["casa", "Lugar donde vives"] ]
palabras_intermedio = [["travesia", "Largo viaje o trampolín de experiencias"],["aventura", "Viaje emocionante y arriesgado"], ["melodia", "Secuencia armoniosa de sonidos"] ]
palabras_dificil = [["efimero", "Que dura por un corto periodo de tiempo"],["magico", "Relacionado con la magia o algo extraordinario"], ["enigma", "Misterio o situación difícil de entender"]]


# Crea una lista de letras del abecedario
abecedario =["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

class Ahorcado():
    def __init__(self):
        self.intentos = 6
        self.letras_adivinadas = []
        self.fin_juego = 0
        self.letras_usadas = []
        self.palabra_mostrada = ''
        self.pista = ''
        self.dificultad = ''
        self.palabra_a_adivinar = ''


    def iniciar(self, dificultad):
        self.intentos = 6
        self.letras_adivinadas = []
        self.fin_juego = 0
        self.letras_usadas = []
        self.palabra_a_adivinar = self.elegir_palabra(dificultad)
        self.palabra_mostrada = self.crear_lineas(self.palabra_a_adivinar[0])
        self.pista = ''
        self.dificultad = dificultad


    def elegir_palabra(self,dificultad):
        if dificultad == 'facil':
            return random.choice(palabras_facil)
        elif dificultad == 'media':
            return random.choice(palabras_intermedio)
        else:
            return random.choice(palabras_dificil)

    # Obtengo la pista asociada a la palabra a adivinar
    def obtener_pista(self):
        self.pista = self.palabra_a_adivinar[1]
        return self.pista
    
    # Verificar si las letras usadas estan en la palabra a adivinar
    def revelar_letra(self, palabra, letras_usadas):
        letras_adiv =''
        for l in palabra:
            if l in letras_usadas:
                letras_adiv+=l
            else:   
                letras_adiv+='_'
        muestra = letras_adiv
        return muestra
    
    # Decrementar intentos
    def decrementar_intentos(self):
        self.intentos -= 1
        print(self.intentos)

    # Creo las lineas de la palabra a adivinar
    # Si la letra no esta en la palabra muestra un guion bajo, sino muestra la letra
    def crear_lineas(self, palabra):
        palabra_mostrada = ''
        for l in palabra:
            palabra_mostrada += '_'
        return palabra_mostrada
    
    # Verifica si la letra ingresada esta en la palabra a adivinar
    def verificar_letra(self, letra, palabra, letras_usadas):
        self.palabra_mostrada = self.revelar_letra(palabra, letras_usadas)
        if letra not in self.palabra_a_adivinar[0]:
            self.decrementar_intentos()
        return self.palabra_mostrada
    
        
    # Verifica si la letra ingresada ya fue usada
    def letraUsada(self, letra):
        if letra in self.letras_adivinadas:
            return True
        else:
            return False
    
    # Verificar si termino el juego
    def verificar_fin_juego(self,palabra_mostrada):
        if self.intentos == 0 or ('_' not in palabra_mostrada):
            self.fin_juego = 1
        return self.fin_juego

    
    def abecedario(self):
        return abecedario