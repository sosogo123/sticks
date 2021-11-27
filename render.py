import graphviz

filepath = 'sticks-2.gv'

graphviz.render(engine='dot', format='png', filepath=filepath)
graphviz.view(f'{filepath}.png')