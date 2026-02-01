"""
DevOps Templates

Includes:
- CI/CD Pipeline
- Kubernetes Architecture
- GitOps Workflow
"""

from viralify_diagrams.templates.devops.cicd import CICDPipelineTemplate
from viralify_diagrams.templates.devops.kubernetes import KubernetesTemplate

__all__ = [
    "CICDPipelineTemplate",
    "KubernetesTemplate",
]
