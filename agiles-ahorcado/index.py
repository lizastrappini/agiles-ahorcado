from flask import Flask, render_template, request, redirect, session
import random


app = Flask(__name__)

# Clave para poder utilizar variables de sesion
app.secret_key = 'tu_clave_secreta'

#['teclado','utilizado para escribir en la pc'],['reloj','dispositivo para ver el tiempo']

# Palabras disponibles
palabras_facil = [["sol", "Fuente principal de luz del sistema solar"], ["gato", "Animal doméstico de compañía"],["casa", "Lugar donde vives"] ]
palabras_intermedio = [["travesia", "Largo viaje o trampolín de experiencias"],["aventura", "Viaje emocionante y arriesgado"], ["melodia", "Secuencia armoniosa de sonidos"] ]
palabras_dificil = [["efimero", "Que dura por un corto periodo de tiempo"],["magico", "Relacionado con la magia o algo extraordinario"], ["enigma", "Misterio o situación difícil de entender"]]

# Crea una lista de letras del abecedario
abecedario =["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]


# Inicializa variables de sesión
def initialize_session(dificultad):
    if dificultad == 'facil':
        session['palabra_a_adivinar'] = elegir_palabra_random_facil()
    elif dificultad == 'media':
        session['palabra_a_adivinar'] = elegir_palabra_random_intermedio()
    else:
        session['palabra_a_adivinar'] = elegir_palabra_random_dificil()
    #session['palabra_a_adivinar'] = elegir_palabra_random()   
    session['intentos'] = 0 
    session['letras_adivinadas'] = []  
    session['fin_juego'] = 0
    session['letras_usadas'] = []
    session['palabra_mostrada'] = ''
    session['pista'] = ''
    session['dificultad'] = dificultad

# Elige una palabra al azar
def elegir_palabra_random_facil():
    return random.choice(palabras_facil)

def elegir_palabra_random_intermedio():
    return random.choice(palabras_intermedio)

def elegir_palabra_random_dificil():
    return random.choice(palabras_dificil)

# Obtengo la pista asociada a la palabra a adivinar
def obtener_pista():
    session['pista'] = session.get('palabra_a_adivinar')[1]
    return session['pista']


# Verificar si las letras usadas estan en la palabra a adivinar
def revelar_letra(palabra, letras_usadas):
    letras_adiv =''
    for l in palabra:
        if l in letras_usadas:
            letras_adiv+=l
        else:   
            letras_adiv+='_'
    muestra = letras_adiv
    return muestra

# Decrementar intentos
def incrementar_intentos():
    session['intentos'] += 1

# Creo las lineas de la palabra a adivinar
# Si la letra no esta en la palabra muestra un guion bajo, sino muestra la letra
def crear_lineas(palabra):
    palabra_mostrada = ''
    for l in palabra:
        palabra_mostrada += '_'
    return palabra_mostrada

# Verificar si la letra esta en la palabra a adivinar
def verificar_letra(letra, palabra, letras_usadas):
    palabra_mostrada = revelar_letra(palabra, letras_usadas)
    if letra not in palabra:
        incrementar_intentos()
    return palabra_mostrada

# Verificar si termino el juego
def verificar_fin_juego(palabra_mostrada):
    if session['intentos'] == 6 or ('_' not in palabra_mostrada):
        session['fin_juego']=1




@app.route("/")
def index():
    return render_template('index.html')


@app.route('/empezar',methods=['POST'])
def empezar():
    dificultad = request.form.get('dificultad')
    initialize_session(dificultad)
    print(dificultad)
    palabra_mostrada=crear_lineas(session['palabra_a_adivinar'][0])
    session['palabra_mostrada']=palabra_mostrada
    session['dificultad'] = request.form.get('dificultad')
    return render_template('jugar.html', pista=session['pista'], palabra_a_adivinar=session['palabra_a_adivinar'][0], abecedario=abecedario, intentos=session['intentos'], letras_adivinadas=session['letras_adivinadas'], palabra_mostrada=palabra_mostrada, letras_usadas=session['letras_usadas'], fin_juego=session['fin_juego'])

@app.route('/jugar', methods=['POST'])
def jugar():

    # Recupero las letras usadas de la variable de sesion
    letras_usadas = session.get('letras_usadas', [])


    # Recupero la palabra a adivinar de la variable de sesion
    palabra = session.get('palabra_a_adivinar')[0]


    # Recupero la letra segun el boton que se presiono
    letra = request.form.get('letra').lower()

    
    # Agrego la letra a la lista de letras usadas
    letras_usadas.append(letra)


    # Actualizo la variable de sesion con la lista de letras usadas para poder seguir utilizandola en los siguientes intentos
    session['letras_usadas'] = letras_usadas

    # Devuelvo la palabra a adivinar/mostrar con las letras adivinadas
    palabra_mostrada = verificar_letra(letra,palabra, letras_usadas)
    session['palabra_mostrada']=palabra_mostrada

    # Si no quedan mas intentos o si la palabra fue adivinada redirecciono al index
    verificar_fin_juego(palabra_mostrada)
    
    
    return render_template('jugar.html',pista=session['pista'], palabra_mostrada=palabra_mostrada, letras_adivinadas=session['letras_adivinadas'], intentos=session['intentos'], abecedario=abecedario, letras_usadas=session['letras_usadas'],palabra_a_adivinar=session['palabra_a_adivinar'][0], fin_juego=session['fin_juego']) 

    
@app.route('/pista', methods=['POST'])
def pista():
    pista = obtener_pista()
    print(pista)
    return render_template('jugar.html', pista=pista, palabra_mostrada=session['palabra_mostrada'], letras_adivinadas=session['letras_adivinadas'], intentos=session['intentos'], abecedario=abecedario, letras_usadas=session['letras_usadas'],palabra_a_adivinar=session['palabra_a_adivinar'][0],fin_juego=session['fin_juego']) 

    

