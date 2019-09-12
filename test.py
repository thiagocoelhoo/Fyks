import core    # importando modulo principal 
core.init() # inicializando o modulo principal 
core.set_theme("black")

from application.application import App # importando modulo de criacao de janela
from ui.frame import Frame  # importando modulo de desenho 
from ui.button import Button # importando classe Button


app = App(800, 600) # criando janela

frame = Frame((0, 0), (800, 600))   # criando frame dentro da janela


# criando um Button
my_button = Button(
    position=(20, 20),
    size=(100, 25),
    text="Cereja",
    func=None
)
my_button.pressed_color = (255, 80, 120)

# criando outro Button
other_button = Button(
    position=(20, 65),
    size=(120, 25),
    text="Other Button",
    func=None
)

frame["meu_button_legal"] = my_button # adicionado Button na frame
frame["outro_button"] = other_button # adicionando outro Button na Frame

app.views["main"] = frame

app.current_view = "main" # definindo o nome do frame atual

app.run()