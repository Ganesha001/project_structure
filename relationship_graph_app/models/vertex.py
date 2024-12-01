from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any

@dataclass
class Vertex:
    id: Optional[str] = None
    label: str = ''
    properties: Dict[str, Any] = None

    def __post_init__(self):
        if self.properties is None:
            self.properties = {}

    def to_dict(self):
        return {
            'id': self.id,
            'label': self.label,
            'properties': self.properties
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            id=data.get('id'),
            label=data.get('label', ''),
            properties=data.get('properties', {})
        )
