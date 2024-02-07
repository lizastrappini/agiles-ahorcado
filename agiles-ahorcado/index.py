from flask import Flask, render_template, request, redirect, session
from Main import Ahorcado

app = Flask(__name__)


juego = Ahorcado()

# Clave para poder utilizar variables de sesion
app.secret_key = 'tu_clave_secreta'

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/empezar',methods=['POST'])
def empezar():
    dificultad = request.form.get('dificultad')
    juego.iniciar(dificultad)
    palabra_mostrada = juego.crear_lineas(juego.palabra_a_adivinar[0])
    return render_template('jugar.html',dificultad=juego.dificultad, pista=juego.pista, palabra_a_adivinar=juego.palabra_a_adivinar[0], abecedario=juego.abecedario(), intentos=juego.intentos, letras_adivinadas=juego.letras_adivinadas, palabra_mostrada=palabra_mostrada, letras_usadas=juego.letras_usadas, fin_juego=juego.verificar_fin_juego(palabra_mostrada))


@app.route('/jugar', methods=['POST'])
def jugar():

    # Recupero las letras usadas de la variable de sesion
    letras_usadas = juego.letras_usadas


    # Recupero la palabra a adivinar de la variable de sesion
    palabra = juego.palabra_a_adivinar[0]


    # Recupero la letra segun el boton que se presiono
    letra = request.form.get('letra').lower()

    
    # Agrego la letra a la lista de letras usadas
    letras_usadas.append(letra)


    # Actualizo la variable con la lista de letras usadas para poder seguir utilizandola en los siguientes intentos
    juego.letras_usadas = letras_usadas

    # Devuelvo la palabra a adivinar/mostrar con las letras adivinadas
    palabra_mostrada = juego.verificar_letra(letra,palabra, letras_usadas)

    # Si no quedan mas intentos o si la palabra fue adivinada redirecciono al index
    juego.verificar_fin_juego(palabra_mostrada)
    
    
    return render_template('jugar.html', dificultad=juego.dificultad, pista=juego.pista, palabra_mostrada=palabra_mostrada, letras_adivinadas=juego.letras_adivinadas, intentos=juego.intentos, abecedario=juego.abecedario(), letras_usadas=juego.letras_usadas,palabra_a_adivinar=juego.palabra_a_adivinar[0], fin_juego=juego.verificar_fin_juego(palabra_mostrada)) 

    
@app.route('/pista', methods=['POST'])
def pista():
    juego.obtener_pista()
    return render_template('jugar.html', dificultad=juego.dificultad, pista=juego.pista, palabra_mostrada=juego.palabra_mostrada, letras_adivinadas=juego.letras_adivinadas, intentos=juego.intentos,abecedario=juego.abecedario(), letras_usadas=juego.letras_usadas,palabra_a_adivinar=juego.palabra_a_adivinar[0],fin_juego=juego.verificar_fin_juego(juego.palabra_mostrada))

    

