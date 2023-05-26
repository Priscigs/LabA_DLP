from graphviz import Digraph  

def SimulationLR0(self, name="LR(0)"):
        # Visualize the syntax automaton using graphviz
        G = Digraph(encoding='utf-8')
        G.attr('node', shape='rectangle')  # Set node shape to rectangle

        for i in self.conjuntos:
            x = []
            for key, value in i.newprod.items():
                for prod in value:
                    x.append(f'{key} → {prod}')

            a = f'I{i.number}\n'
            a += '\n'.join(x)
            G.node(str(i.number), a)

        for key, value in self.edges.items():
            G.edge(str(key[0].number), str(key[1].number), label=value)

        G.render(filename=name, directory='./outputsLabs', format='png')
