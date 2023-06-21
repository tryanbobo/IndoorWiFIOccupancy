import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import pyvista as pv
import ezdxf

path = r"C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\WifiData\output\agg\aggDuration"
df = pd.read_csv(path + "\FloorCounts_30min_static.csv")
print(df)


def load_dwg_with_layers(dwg_path):
    doc = ezdxf.readfile(dwg_path)

    # Get the modelspace and all layers
    modelspace = doc.modelspace()
    layers = doc.layers

    # Iterate through layers and access the entities on each layer
    for layer in layers:
        print(f"Layer name: {layer.dxf.name}")

        # Access the entities (e.g., polylines, circles, etc.) on the current layer
        for entity in modelspace:
            if entity.dxf.layer == layer.dxf.name and entity.dxftype() in ["POLYLINE", "CIRCLE", "LINE"]:
                print(f"Entity: {entity.dxftype()}")

# Example usage
dwg_file = r"C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\spring2023\Alkek3d\Alkek3d.dxf"
load_dwg_with_layers(dwg_file)












#alkek3d = pv.read(r"C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\spring2023\Alkek3d\Alkek3d.dwg")
#
#plotter = pv.Plotter()
#
#plotter.add_mesh(alkek3d)
#
#plotter.background_color = "white"
#plotter.show_axes()
#
#plotter.show()
