import random
from json import load
from math import atan2, pi
import consts as c
from povors import povors

threshold = 0.2  # meters
dangerous_threshold = 0.3


def get_distance(x1, y1, z1, x2, y2, z2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2) ** 0.5


class Clever:
    z = 0
    yaw = -pi / 2
    voltage = 0
    point_to = 0
    point_now = 0
    led = '#000000'
    status = "land"
    last_point = -1
    force_landed = False

    def __init__(self, ip):
        self.path = []
        self.busy_points = []
        self.x = random.randint(0, 100) / 100
        self.y = random.randint(0, 100) / 100
        self.ip = ip

    def random(self):
        r = lambda: random.randint(0, 255)
        self.led = '#%02X%02X%02X' % (r(), r(), r())
        self.x = random.randint(0, 2000) / 1000
        self.y = random.randint(0, 2000) / 1000
        self.z = random.randint(0, 2000) / 1000
        self.yaw = random.randint(0, 62831) / 10000

    def toDict(self):
        return {
            "led": self.led,
            "status": self.status,
            "pose": {
                "x": self.x, "y": self.y, "z": self.z,
                "yaw": self.yaw
            }
        }

    def toTelem(self, copters):
        return {
            "ip": self.ip,
            "led": self.led,
            "status": self.status,
            "pose": {
                "x": self.x, "y": self.y, "z": self.z,
                "yaw": self.yaw
            },
            "voltage": self.voltage,
            "nextp": self.toNewTelem(copters)
        }

    def toNewTelem(self, copters):
        if self.force_landed:
            return {
                "led": self.led,
                "status": 'force_land',
                "pose": {
                    "x": self.x, "y": self.y, "z": self.z,
                    "yaw": self.yaw
                }
            }
        if not self.path:
            self.busy_points = []
            self.status = 'land'
            return {
                "led": self.led,
                "status": self.status,
                "pose": {
                    "x": self.x, "y": self.y, "z": c.first_layer_height,
                    "yaw": self.yaw
                }
            }
        else:
            with open('static/roads.json', 'r') as f:
                file_data = load(f)

                # print(self.path[0][-1:])

                if self.path[0] == '-1' or len(self.path) == 1:
                    self.path = []
                    self.status = 'land'
                    return {
                        "led": self.led,
                        "status": self.status,
                        "pose": {
                            "x": self.x, "y": self.y, "z": c.first_layer_height,
                            "yaw": self.yaw
                        }
                    }
                n = int(self.path[0][:-1])
                nav_point = file_data['points'][n]
                nav_point['z'] = c.first_layer_height
                #
                # if self.path[0][-1:] == '0':
                #     nav_point['z'] = c.first_layer_height
                # elif self.path[0][-1:] == '1':
                #     nav_point['z'] = c.second_layer_height
                dist = get_distance(nav_point['x'], nav_point['y'], nav_point['z'], self.x, self.y, nav_point['z'])
                # print(dist)
                # collisions = check_collisions(self, copters)
                # if not collisions:
                #     self.status = 'fly'
                if (dist < threshold):
                    try:
                        self.last_point = self.path.pop(0)
                    except:
                        self.last_point = -1
                    return self.toNewTelem(copters)
                self.status = 'fly'
                print(self.point_now, int(self.path[0][:-1]), int(self.path[1][:-1]),
                      povors.get((self.point_now, int(self.path[0][:-1]), int(self.path[1][:-1]))))
                return {
                    "led": self.led,
                    "status": self.status,
                    "point": n,
                    "turn": povors.get((self.point_now, int(self.path[0][:-1]), int(self.path[1][:-1]))),
                    "pose": {
                        "x": nav_point['x'], "y": nav_point['y'], "z": nav_point['z'],
                        "yaw": self.yaw
                    }
                }

    def get_status(self):
        if 0 < len(self.busy_points) <= 1:
            if self.status == 'fly':
                return 'flight_to_dest'
            elif self.status == 'land':
                return 'human_wait'
        elif len(self.busy_points) == 2:
            return 'flight_to_human'
        else:
            return 'landed'

    def point(self, point_n, to):
        with open('static/roads.json', 'r') as f:
            points = load(f)['points']
        self.x = points[point_n]['x']
        self.y = points[point_n]['y']
        self.point_to = to
        self.point_now = point_n



def check_collisions(c, copters):
    paths = []
    with open('static/roads.json', 'r') as f:
        file_data = load(f)

    for copter in copters:
        if copter.ip != c.ip:
            if copter.status != 'land':
                try:
                    if copter.last_point != -1:
                        n = int(copter.path[0][:-1])
                        nav_point = file_data['points'][n]
                        nav_point['z'] = c.first_layer_height

                        if copter.path[0][-1:] == '0':
                            nav_point['z'] = c.first_layer_height
                        elif copter.path[0][-1:] == '1':
                            nav_point['z'] = c.second_layer_height
                        dist = get_distance(nav_point['x'], nav_point['y'], nav_point['z'], copter.x, copter.y,
                                            copter.z)
                        if dist > threshold:
                            paths.append(copter.last_point)
                except:
                    pass
                try:
                    paths.append(copter.path[0])
                except:
                    pass

    try:
        if c.status == 'land':
            fact = c.path[0] in paths
        else:
            fact = c.path[1] in paths
    except:
        fact = False

    for i in copters:
        if i != c:
            if get_d(c, i) < dangerous_threshold:
                if get_d_to_point(i, i.path[0]) < get_d_to_point(c, c.path[0]):
                    c.force_landed = True
                    i.force_landed = True

    return fact


def get_d(c1, c2):
    return get_distance(c1.x, c1.y, c1.z, c2.x, c2.y, c2.z)


def get_d_to_point(c, p):
    with open('static/roads.json', 'r') as f:
        file_data = load(f)

        n = int(p[:-1])
        nav_point = file_data['points'][n]
        nav_point['z'] = c.first_layer_height

        if p[-1:] == '0':
            nav_point['z'] = c.first_layer_height
        elif p[-1:] == '1':
            nav_point['z'] = c.second_layer_height

        return get_distance(nav_point['x'], nav_point['y'], nav_point['z'], c.x, c.y, c.z)


def get_angle(o, n):
    try:
        return -pi / 2  # atan2((o['x'] - n['x']), (o['y'] - n['y'])) - pi / 2
    except:
        return -pi / 2
