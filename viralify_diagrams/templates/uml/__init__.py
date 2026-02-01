"""
UML Templates

Includes:
- Class Diagram
- Sequence Diagram
- Activity Diagram
- State Machine Diagram
- Use Case Diagram
"""

from viralify_diagrams.templates.uml.class_diagram import UMLClassTemplate
from viralify_diagrams.templates.uml.sequence import UMLSequenceTemplate
from viralify_diagrams.templates.uml.activity import UMLActivityTemplate

__all__ = [
    "UMLClassTemplate",
    "UMLSequenceTemplate",
    "UMLActivityTemplate",
]
