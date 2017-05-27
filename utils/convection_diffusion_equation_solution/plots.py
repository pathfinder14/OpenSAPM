import tests2 as t

t.testing(method = 'KIR', initial =  'sin', velocity = 'const')
t.testing(method = 'KIR', initial =  'sin', velocity = 'x')
t.testing(method = 'KIR', initial =  'sin', velocity = 'func')

t.testing(method = 'KIR', initial =  'peak', velocity = 'const')
t.testing(method = 'KIR', initial =  'peak', velocity = 'x')
t.testing(method = 'KIR', initial =  'peak', velocity = 'func')

t.testing(method = 'KIR', initial =  'rectangle', velocity = 'const')
t.testing(method = 'KIR', initial =  'rectangle', velocity = 'x')
t.testing(method = 'KIR', initial =  'rectangle', velocity = 'func')


t.testing(method = 'McCormack', initial =  'sin', velocity = 'const')
t.testing(method = 'McCormack', initial =  'sin', velocity = 'x')
t.testing(method = 'McCormack', initial =  'sin', velocity = 'func')

t.testing(method = 'McCormack', initial =  'peak', velocity = 'const')
t.testing(method = 'McCormack', initial =  'peak', velocity = 'x')
t.testing(method = 'McCormack', initial =  'peak', velocity = 'func')

t.testing(method = 'McCormack', initial =  'rectangle', velocity = 'const')
t.testing(method = 'McCormack', initial =  'rectangle', velocity = 'x')
t.testing(method = 'McCormack', initial =  'rectangle', velocity = 'func')


t.testing(method = 'Beam-Warming', initial =  'sin', velocity = 'const')
t.testing(method = 'Beam-Warming', initial =  'sin', velocity = 'x')
t.testing(method = 'Beam-Warming', initial =  'sin', velocity = 'func')

t.testing(method = 'Beam-Warming', initial =  'peak', velocity = 'const')
t.testing(method = 'Beam-Warming', initial =  'peak', velocity = 'x')
t.testing(method = 'Beam-Warming', initial =  'peak', velocity = 'func')

t.testing(method = 'Beam-Warming', initial =  'rectangle', velocity = 'const')
t.testing(method = 'Beam-Warming', initial =  'rectangle', velocity = 'x')
t.testing(method = 'Beam-Warming', initial =  'rectangle', velocity = 'func')


t.testing(method = 'Lax-Wendroff', initial =  'sin', velocity = 'const')
t.testing(method = 'Lax-Wendroff', initial =  'sin', velocity = 'x')
t.testing(method = 'Lax-Wendroff', initial =  'sin', velocity = 'func')

t.testing(method = 'Lax-Wendroff', initial =  'peak', velocity = 'const')
t.testing(method = 'Lax-Wendroff', initial =  'peak', velocity = 'x')
t.testing(method = 'Lax-Wendroff', initial =  'peak', velocity = 'func')

t.testing(method = 'Lax-Wendroff', initial =  'rectangle', velocity = 'const')
t.testing(method = 'Lax-Wendroff', initial =  'rectangle', velocity = 'x')
t.testing(method = 'Lax-Wendroff', initial =  'rectangle', velocity = 'func')


t.testing(method = 'Fedorenko', initial =  'sin', velocity = 'const')
t.testing(method = 'Fedorenko', initial =  'sin', velocity = 'x')
t.testing(method = 'Fedorenko', initial =  'sin', velocity = 'func')

t.testing(method = 'Fedorenko', initial =  'peak', velocity = 'const')
t.testing(method = 'Fedorenko', initial =  'peak', velocity = 'x')
t.testing(method = 'Fedorenko', initial =  'peak', velocity = 'func')

t.testing(method = 'Fedorenko', initial =  'rectangle', velocity = 'const')
t.testing(method = 'Fedorenko', initial =  'rectangle', velocity = 'x')
t.testing(method = 'Fedorenko', initial =  'rectangle', velocity = 'func')


t.testing(method = 'Rusanov', initial =  'sin', velocity = 'const')
t.testing(method = 'Rusanov', initial =  'sin', velocity = 'x')
t.testing(method = 'Rusanov', initial =  'sin', velocity = 'func')

t.testing(method = 'Rusanov', initial =  'peak', velocity = 'const')
t.testing(method = 'Rusanov', initial =  'peak', velocity = 'x')
t.testing(method = 'Rusanov', initial =  'peak', velocity = 'func')

t.testing(method = 'Rusanov', initial =  'rectangle', velocity = 'const')
t.testing(method = 'Rusanov', initial =  'rectangle', velocity = 'x')
t.testing(method = 'Rusanov', initial =  'rectangle', velocity = 'func')
