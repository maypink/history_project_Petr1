from typing import List, Dict
import json
from dataclasses import dataclass

@dataclass
class Monument:


    name: str
    location: str
    type: str
    status: str
    description: List[List[str]]    # list for each paragraph
    imageURLs: List[str]

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
    
    @property
    def imageURLs(self):
        return self._imageURLs

    @imageURLs.setter
    def name(self, imageURLs):
        self._imageURLs = imageURLs

    @classmethod
    def from_json(cls, json_object: str):
        monument_info = json.loads(json_object)
        return cls(monument_info['name'], monument_info['location'],
                   monument_info['type'], monument_info['status'],
                   monument_info['description'], monument_info['imageURLs'])

    def to_json(self) -> Dict:
        monument_json = dict({'name': self.name,
                              'location': self.location,
                              'type': self.type,
                              'status': self.status,
                              'description': self.description,
                              'imageURLs': self.imageURLs})
        return monument_json
