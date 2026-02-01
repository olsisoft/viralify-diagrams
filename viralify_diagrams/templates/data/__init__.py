"""
Data Templates

Includes:
- Data Flow Diagram (DFD)
- Entity Relationship Diagram (ERD)
- Data Lineage Diagram
"""

from viralify_diagrams.templates.data.dfd import DFDTemplate
from viralify_diagrams.templates.data.erd import ERDTemplate
from viralify_diagrams.templates.data.lineage import DataLineageTemplate

__all__ = [
    "DFDTemplate",
    "ERDTemplate",
    "DataLineageTemplate",
]
