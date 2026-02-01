"""
Template Registry

Central registry for all diagram templates. Provides:
- Template registration and lookup
- Template discovery by domain/category
- Template instantiation
- Integration with taxonomy system
"""

from typing import Dict, List, Optional, Type, Any
from threading import Lock

from viralify_diagrams.templates.base import DiagramTemplate, TemplateConfig
from viralify_diagrams.taxonomy.categories import (
    DiagramDomain,
    DiagramCategory,
    DiagramType,
)


class TemplateRegistry:
    """
    Central registry for diagram templates.

    Thread-safe singleton registry that manages all available templates.

    Example:
        >>> registry = get_template_registry()
        >>> template = registry.get("c4_context")
        >>> templates = registry.list_by_domain(DiagramDomain.ARCHITECTURE)
    """

    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._templates: Dict[str, DiagramTemplate] = {}
        self._template_classes: Dict[str, Type[DiagramTemplate]] = {}
        self._by_domain: Dict[DiagramDomain, List[str]] = {}
        self._by_category: Dict[DiagramCategory, List[str]] = {}
        self._by_type: Dict[DiagramType, str] = {}

        self._initialized = True

        # Register built-in templates
        self._register_builtin_templates()

    def register(
        self,
        template_class: Type[DiagramTemplate],
        domain: DiagramDomain,
        category: DiagramCategory,
        diagram_type: Optional[DiagramType] = None
    ) -> None:
        """
        Register a template class.

        Args:
            template_class: The template class to register
            domain: Domain classification
            category: Category classification
            diagram_type: Optional specific diagram type
        """
        # Instantiate template to get ID
        template = template_class()
        template_id = template.template_id

        self._templates[template_id] = template
        self._template_classes[template_id] = template_class

        # Index by domain
        if domain not in self._by_domain:
            self._by_domain[domain] = []
        if template_id not in self._by_domain[domain]:
            self._by_domain[domain].append(template_id)

        # Index by category
        if category not in self._by_category:
            self._by_category[category] = []
        if template_id not in self._by_category[category]:
            self._by_category[category].append(template_id)

        # Index by type
        if diagram_type:
            self._by_type[diagram_type] = template_id

    def get(self, template_id: str) -> Optional[DiagramTemplate]:
        """Get a template by ID"""
        return self._templates.get(template_id)

    def get_by_type(self, diagram_type: DiagramType) -> Optional[DiagramTemplate]:
        """Get template for a specific diagram type"""
        template_id = self._by_type.get(diagram_type)
        if template_id:
            return self._templates.get(template_id)
        return None

    def list_all(self) -> List[str]:
        """List all template IDs"""
        return list(self._templates.keys())

    def list_by_domain(self, domain: DiagramDomain) -> List[str]:
        """List templates in a domain"""
        return self._by_domain.get(domain, [])

    def list_by_category(self, category: DiagramCategory) -> List[str]:
        """List templates in a category"""
        return self._by_category.get(category, [])

    def get_template_info(self, template_id: str) -> Optional[Dict[str, Any]]:
        """Get template information"""
        template = self._templates.get(template_id)
        if template:
            return template.to_dict()
        return None

    def list_all_info(self) -> List[Dict[str, Any]]:
        """Get info for all templates"""
        return [t.to_dict() for t in self._templates.values()]

    def create_fresh_instance(self, template_id: str) -> Optional[DiagramTemplate]:
        """Create a fresh instance of a template"""
        template_class = self._template_classes.get(template_id)
        if template_class:
            return template_class()
        return None

    def _register_builtin_templates(self):
        """Register all built-in templates"""
        # Import and register templates lazily to avoid circular imports
        self._register_architecture_templates()
        self._register_uml_templates()
        self._register_data_templates()
        self._register_security_templates()
        self._register_devops_templates()
        self._register_business_templates()

    def _register_architecture_templates(self):
        """Register architecture templates (C4, TOGAF, etc.)"""
        try:
            from viralify_diagrams.templates.architecture.c4 import (
                C4ContextTemplate,
                C4ContainerTemplate,
                C4ComponentTemplate,
                C4DeploymentTemplate,
            )

            self.register(
                C4ContextTemplate,
                DiagramDomain.ARCHITECTURE,
                DiagramCategory.C4_MODEL,
                DiagramType.C4_CONTEXT
            )
            self.register(
                C4ContainerTemplate,
                DiagramDomain.ARCHITECTURE,
                DiagramCategory.C4_MODEL,
                DiagramType.C4_CONTAINER
            )
            self.register(
                C4ComponentTemplate,
                DiagramDomain.ARCHITECTURE,
                DiagramCategory.C4_MODEL,
                DiagramType.C4_COMPONENT
            )
            self.register(
                C4DeploymentTemplate,
                DiagramDomain.ARCHITECTURE,
                DiagramCategory.C4_MODEL,
                DiagramType.C4_DEPLOYMENT
            )
        except ImportError:
            pass  # Templates not yet implemented

    def _register_uml_templates(self):
        """Register UML templates"""
        try:
            from viralify_diagrams.templates.uml.class_diagram import UMLClassTemplate
            from viralify_diagrams.templates.uml.sequence import UMLSequenceTemplate
            from viralify_diagrams.templates.uml.activity import UMLActivityTemplate

            self.register(
                UMLClassTemplate,
                DiagramDomain.DEVELOPMENT,
                DiagramCategory.UML_STRUCTURAL,
                DiagramType.UML_CLASS
            )
            self.register(
                UMLSequenceTemplate,
                DiagramDomain.DEVELOPMENT,
                DiagramCategory.UML_INTERACTION,
                DiagramType.UML_SEQUENCE
            )
            self.register(
                UMLActivityTemplate,
                DiagramDomain.DEVELOPMENT,
                DiagramCategory.UML_BEHAVIORAL,
                DiagramType.UML_ACTIVITY
            )
        except ImportError:
            pass

    def _register_data_templates(self):
        """Register data templates (DFD, ERD, etc.)"""
        try:
            from viralify_diagrams.templates.data.dfd import DFDTemplate
            from viralify_diagrams.templates.data.erd import ERDTemplate
            from viralify_diagrams.templates.data.lineage import DataLineageTemplate

            self.register(
                DFDTemplate,
                DiagramDomain.DATA,
                DiagramCategory.DATA_FLOW,
                DiagramType.DFD_LEVEL0
            )
            self.register(
                ERDTemplate,
                DiagramDomain.DATA,
                DiagramCategory.DATA_MODELING,
                DiagramType.ERD
            )
            self.register(
                DataLineageTemplate,
                DiagramDomain.DATA,
                DiagramCategory.DATA_FLOW,
                DiagramType.DATA_LINEAGE
            )
        except ImportError:
            pass

    def _register_security_templates(self):
        """Register security templates"""
        try:
            from viralify_diagrams.templates.security.threat_model import STRIDEThreatTemplate

            self.register(
                STRIDEThreatTemplate,
                DiagramDomain.SECURITY,
                DiagramCategory.THREAT_MODELING,
                DiagramType.STRIDE_THREAT_MODEL
            )
        except ImportError:
            pass

    def _register_devops_templates(self):
        """Register DevOps templates"""
        try:
            from viralify_diagrams.templates.devops.cicd import CICDPipelineTemplate
            from viralify_diagrams.templates.devops.kubernetes import KubernetesTemplate

            self.register(
                CICDPipelineTemplate,
                DiagramDomain.DEVOPS,
                DiagramCategory.CI_CD,
                DiagramType.CI_CD_PIPELINE
            )
            self.register(
                KubernetesTemplate,
                DiagramDomain.DEVOPS,
                DiagramCategory.CONTAINER_ORCHESTRATION,
                DiagramType.KUBERNETES_CLUSTER
            )
        except ImportError:
            pass

    def _register_business_templates(self):
        """Register business templates"""
        try:
            from viralify_diagrams.templates.business.bpmn import BPMNProcessTemplate

            self.register(
                BPMNProcessTemplate,
                DiagramDomain.BUSINESS,
                DiagramCategory.BUSINESS_PROCESS,
                DiagramType.BPMN_PROCESS
            )
        except ImportError:
            pass


# Singleton instance
_registry: Optional[TemplateRegistry] = None


def get_template_registry() -> TemplateRegistry:
    """Get the global template registry instance"""
    global _registry
    if _registry is None:
        _registry = TemplateRegistry()
    return _registry


def get_template(template_id: str) -> Optional[DiagramTemplate]:
    """Get a template by ID"""
    return get_template_registry().get(template_id)


def list_templates(
    domain: Optional[DiagramDomain] = None,
    category: Optional[DiagramCategory] = None
) -> List[str]:
    """
    List available templates.

    Args:
        domain: Filter by domain
        category: Filter by category

    Returns:
        List of template IDs
    """
    registry = get_template_registry()

    if category:
        return registry.list_by_category(category)
    elif domain:
        return registry.list_by_domain(domain)
    else:
        return registry.list_all()


def register_template(
    template_class: Type[DiagramTemplate],
    domain: DiagramDomain,
    category: DiagramCategory,
    diagram_type: Optional[DiagramType] = None
) -> None:
    """
    Register a custom template.

    Args:
        template_class: Template class to register
        domain: Domain classification
        category: Category classification
        diagram_type: Optional diagram type
    """
    get_template_registry().register(template_class, domain, category, diagram_type)
