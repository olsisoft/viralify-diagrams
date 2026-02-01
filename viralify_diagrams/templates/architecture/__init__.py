"""
Architecture Templates

Includes:
- C4 Model (Context, Container, Component, Code, Deployment)
- TOGAF Architecture Framework
- ArchiMate
"""

from viralify_diagrams.templates.architecture.c4 import (
    C4ContextTemplate,
    C4ContainerTemplate,
    C4ComponentTemplate,
    C4DeploymentTemplate,
)

__all__ = [
    "C4ContextTemplate",
    "C4ContainerTemplate",
    "C4ComponentTemplate",
    "C4DeploymentTemplate",
]
