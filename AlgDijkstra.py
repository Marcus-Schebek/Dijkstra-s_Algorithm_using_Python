import streamlit as st
import st_cytoscape

class Vertice:
    def __init__(self, nome):
        self.nome = nome
        self.vizinhos = {} #Dicionário para usar de Hash map

    def adicionar_vizinho(self, vertice, peso=0):
        self.vizinhos[vertice] = peso


class Aresta:
    def __init__(self, vertice1, vertice2, peso=0):
        self.vertice1 = vertice1
        self.vertice2 = vertice2
        self.peso = peso


class Grafo:
    def __init__(self):
        self.vertices = {}
        self.limite_vertices = 20

    def adicionar_vertice(self, nome):
        if len(self.vertices) < self.limite_vertices:
            novo_vertice = Vertice(nome)
            self.vertices[nome] = novo_vertice
        else:
            print("Limite máximo de vértices atingido")
    def definir_origem_destino(self, origem, destino):
        if origem in self.vertices and destino in self.vertices:
            self.origem = self.vertices[origem]
            self.destino = self.vertices[destino]
    def adicionar_aresta(self, nome_origem, nome_destino, peso=0):
        if nome_origem in self.vertices and nome_destino in self.vertices:
            vertice_origem = self.vertices[nome_origem]
            vertice_destino = self.vertices[nome_destino]
            vertice_origem.adicionar_vizinho(vertice_destino, peso)
            vertice_destino.adicionar_vizinho(vertice_origem, peso)
    def imprimir_grafo(self):
        for nome_vertice, vertice in self.vertices.items():
            vizinhos = vertice.vizinhos
            arestas = []
            for vizinho, peso in vizinhos.items():
                arestas.append(f"({vizinho.nome}, {peso})")
            arestas_str = ", ".join(arestas)
            print(f"Vértice {nome_vertice} -> {arestas_str}")
            
class DijkstraInfo:
    def __init__(self, vertice):
        self.vertice = vertice
        self.distancia = float('inf')
        self.antecessor = None
        
class Dikstra:
    def __init__(self, grafo, origem, destino):
        self.grafo = grafo
        self.origem = origem
        self.destino = destino
        self.info_vertices = {v: DijkstraInfo(v) for v in grafo.vertices.values()}
    def calcular_menor_caminho(self):
        self.info_vertices[self.origem].distancia = 0
        vertices_a_explorar = list(self.info_vertices.values())
        while vertices_a_explorar:
            vertices_a_explorar.sort(key = lambda x: x.distancia)
            vertice_atual = vertices_a_explorar.pop(0)
            for vizinho, peso in vertice_atual.vertice.vizinhos.items():
                nova_distancia = vertice_atual.distancia + peso
                if nova_distancia < self.info_vertices[vizinho].distancia:
                    self.info_vertices[vizinho].distancia = nova_distancia
                    self.info_vertices[vizinho].antecessor = vertice_atual.vertice
    def obter_caminho(self):
        caminho = []
        vertice_atual = self.destino
        while vertice_atual != self.origem:
            caminho.insert(0, vertice_atual.nome)
            vertice_atual = self.info_vertices[vertice_atual].antecessor

        caminho.insert(0, self.origem.nome)
        return caminho

def desenhar_grafo(grafo):
    nos = [{"data": {"id": v}} for v in grafo.vertices]
    arestas = []
    for v in grafo.vertices.values():
        for vizinho, peso in v.vizinhos.items():
            # Alterando o estilo da aresta para posicionar o label à direita
            arestas.append({"data": {"source": v.nome, "target": vizinho.nome, "label": str(peso), "text-rotation": "autorotate"}})
    elementos = nos + arestas
    # Definindo um estilo padrão
    stylesheet = [
        {
            'selector': 'node',
            'style': {
                'background-color': '#CC2936',
                'label': 'data(id)',
                'font-size': 12,
                'width': 24,  # Aumente o tamanho do nó
                'height': 24  # Aumente o tamanho do nó
            }
        },
        {
            'selector': 'edge',
            'style': {
                'line-color': '#B2B2B2',
                'width': 2,
                'label': 'data(label)',
                'font-size': 12,
                'text-halign': 'right',
                'text-valign': 'top',
                'text-margin-x': -7,
                'text-margin-y': -5,
                'color': '#FFFFFF'
            }
        }
    ]
        
    for no in nos:
        no['grabbable'] = False
    st_cytoscape.cytoscape(elements=elementos, stylesheet=stylesheet)

def main():
    grafo = Grafo()
    
    col1, col2 = st.columns([1, 1.25])

    with col1:
        st.write("Algoritmo de Dijkstra")
        # Adicionando vértices
        vertices = st.text_input("Insira os nomes das cidades, separados por vírgula: ")
        vertices = vertices.split(',')
        for vertice in vertices:
            grafo.adicionar_vertice(vertice.strip())

        # Definindo origem e destino
        origem = st.text_input("Insira o nome da cidade de Origem: ")
        destino = st.text_input("Insira o nome da cidade de Destino: ")
        grafo.definir_origem_destino(origem, destino)

        # Adicionando arestas
        arestas = st.text_input("Insira as arestas no formato 'origem, destino, peso', separadas por ponto e vírgula: ")
        arestas = arestas.split(';')
        for aresta in arestas:
            partes = aresta.split(',')
            if len(partes) == 3:
                origem, destino, peso = partes
                grafo.adicionar_aresta(origem.strip(), destino.strip(), int(peso.strip()))
            else:
                st.write(f"Aresta inválida: {aresta}. Por favor, insira as arestas no formato 'origem, destino, peso'.")


        if st.button('Calcular menor caminho'):
            dikstra = Dikstra(grafo, grafo.origem, grafo.destino)
            dikstra.calcular_menor_caminho()
            caminho = dikstra.obter_caminho()
            st.write(f"O menor caminho é: {caminho}")
    with col2:    
        desenhar_grafo(grafo)
        st.write("Criado por Marcus Schebek")

if __name__ == "__main__":
    main()
