from typing import List, Dict
import json
from dataclasses import dataclass

@dataclass
class Monument:

    id: int
    name: str
    location: str
    coords: Dict[float, float]
    type: str
    status: str
    description: List[List[str]]    # list for each paragraph

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        self._location = location

    @property
    def coords(self):
        return self._coords

    @coords.setter
    def coords(self, coords):
        self._coords = coords

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @classmethod
    def from_json(cls, json_object: str):
        monument_info = json.loads(json_object)
        return cls(monument_info['id'], monument_info['name'],
                   monument_info['location'], monument_info['coords'],
                   monument_info['type'], monument_info['status'],
                   monument_info['description'])

    def info_to_json(self) -> Dict:
        monument_json = dict({'id': self.id,
                              'name': self.name,
                              'location': self.location,
                              'type': self.type,
                              'status': self.status,
                              'description': self.description})
        return monument_json

    def coords_to_json(self) -> Dict:
        monument_json = dict({'id': self.id,
                              'coords': self.coords})
        return monument_json

    def to_json(self) -> Dict:
        monument_json = dict({'id': self.id,
                              'name': self.name,
                              'location': self.location,
                              'coords': self.coords,
                              'type': self.type,
                              'status': self.status,
                              'description': self.description})
        return monument_json
