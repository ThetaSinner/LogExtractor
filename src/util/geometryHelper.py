import re


class GeometryHelper:
    def __init__(self, widget):
        widget.update_idletasks()

        geometry_string = widget.geometry()

        p = re.compile('([0-9]+)x([0-9]+)([+-][0-9]+)([+-][0-9]+)')
        geometry_values = re.findall(p, geometry_string)[0]

        self.geometry_values = {'w': geometry_values[0], 'h': geometry_values[1], 'x': geometry_values[2],
                                'y': geometry_values[3]}

    def get_width(self):
        return int(self.geometry_values['w'])

    def get_height(self):
        return int(self.geometry_values['h'])

    def get_x(self):
        return int(self.geometry_values['x'][1:])

    def get_y(self):
        return int(self.geometry_values['y'][1:])

# app = Tk()
# app.geometry("200x300")

# gs = GeometryService(app)
# print(gs.get_width())
# print(gs.get_height())
# print(gs.get_x())
# print(gs.get_y())
