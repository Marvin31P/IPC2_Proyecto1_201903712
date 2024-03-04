import xml.etree.ElementTree as ET
from graphviz import Digraph

class PisosGuatemala:
    def __init__(self):
        self.pisos = {}

    def cargar_desde_xml(self, archivo):
        tree = ET.parse(archivo)
        root = tree.getroot()
        
        for piso_xml in root.findall('piso'):
            nombre_piso = piso_xml.attrib['nombre']
            R = int(piso_xml.find('R').text)
            C = int(piso_xml.find('C').text)
            F = int(piso_xml.find('F').text)
            S = int(piso_xml.find('S').text)
            patrones = {}
            for patron_xml in piso_xml.find('patrones').findall('patron'):
                codigo_patron = patron_xml.attrib['codigo']
                patron = patron_xml.text.split('_')
                patrones[codigo_patron] = patron
            self.pisos[nombre_piso] = {'R': R, 'C': C, 'F': F, 'S': S, 'patrones': patrones}

    def mostrar_pisos_y_patrones(self):
        print("Pisos disponibles:")
        for nombre_piso in sorted(self.pisos.keys()):
            print(nombre_piso)
            print("  Patrones disponibles:")
            for codigo_patron in sorted(self.pisos[nombre_piso]['patrones'].keys()):
                print(f"    {codigo_patron}")

    def mostrar_patron_graficamente(self, nombre_piso, codigo_patron):
        patron = self.pisos[nombre_piso]['patrones'][codigo_patron]
        graph = Digraph()
        for i in range(len(patron)):
            for j in range(len(patron[i])):
                color = 'black' if patron[i][j] == 'N' else 'white'
                graph.node(f'{i}_{j}', style='filled', fillcolor=color)
                if j > 0:
                    graph.edge(f'{i}_{j-1}', f'{i}_{j}', constraint='false')
                if i > 0:
                    graph.edge(f'{i-1}_{j}', f'{i}_{j}', constraint='false')
        graph.render(filename=f'{nombre_piso}_{codigo_patron}', format='png', cleanup=True)
        graph.view()

    def calcular_costo_minimo(self, nombre_piso, codigo_patron_actual, codigo_patron_nuevo):
        patron_actual = self.pisos[nombre_piso]['patrones'][codigo_patron_actual]
        patron_nuevo = self.pisos[nombre_piso]['patrones'][codigo_patron_nuevo]
        costo_volteo = self.pisos[nombre_piso]['F']
        costo_intercambio = self.pisos[nombre_piso]['S']
        instrucciones = []

        for i in range(len(patron_actual)):
            for j in range(len(patron_actual[i])):
                if patron_actual[i][j] != patron_nuevo[i][j]:
                    if costo_volteo <= costo_intercambio:
                        instrucciones.append(f"Voltear azulejo en la posición ({i+1},{j+1})")
                    else:
                        instrucciones.append(f"Intercambiar azulejos en las posiciones ({i+1},{j+1}) y ({i+1},{j+2})")
                        # Se asume que se pueden intercambiar azulejos adyacentes horizontalmente
                        patron_actual[i] = patron_actual[i][:j] + patron_actual[i][j+1] + patron_actual[i][j] + patron_actual[i][j+2:]
        return costo_volteo * len(instrucciones), instrucciones

    def mostrar_instrucciones(self, instrucciones):
        for instruccion in instrucciones:
            print(instruccion)

    def ejecutar(self):
        while True:
            print("\nBienvenido a Pisos de Guatemala, S.A.")
            print("¿Qué desea hacer?")
            print("1. Mostrar pisos y patrones disponibles")
            print("2. Mostrar un patrón gráficamente")
            print("3. Calcular costo mínimo para cambiar patrón")
            print("4. Salir")
            opcion = input("Seleccione una opción: ")
            if opcion == '1':
                self.mostrar_pisos_y_patrones()
            elif opcion == '2':
                nombre_piso = input("Ingrese el nombre del piso: ")
                codigo_patron = input("Ingrese el código del patrón: ")
                self.mostrar_patron_graficamente(nombre_piso, codigo_patron)
            elif opcion == '3':
                " "
            elif opcion == '4':
                print("¡Hasta luego!")
                break
            else:
                print("Opción inválida, por favor intente de nuevo.")

if __name__ == "__main__":
    pisos_guatemala = PisosGuatemala()
    pisos_guatemala.cargar_desde_xml("pisos.xml")
    pisos_guatemala.ejecutar()
