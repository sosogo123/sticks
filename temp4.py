"""https://graphviz.org/Gallery/directed/fsm.html"""

import graphviz

# with open('fsm.gv', 'r') as dot_file:
#     src = graphviz.Source(dot_file.read())
#     src.render(view=True)
    # src.render('test-output/holy-grenade.gv', view=True)

filepath = 'sticks-2.gv'
# filepath = 'fsm.gv'
graphviz.render(engine='dot', format='png', filepath=filepath)
graphviz.view(f'{filepath}.png')