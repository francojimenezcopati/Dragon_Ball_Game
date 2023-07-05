from csv import reader


def importar_csv_layout(path):
    mapa_layout = []
    with open(path) as mapa:
        nivel = reader(mapa, delimiter=",")
        for fila in nivel:
            mapa_layout.append(list(fila))
        return mapa_layout
