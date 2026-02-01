"""
Data Lineage Diagram Template

Shows data flow and transformations across systems:
- Source systems
- ETL/ELT pipelines
- Data warehouses and lakes
- BI and analytics tools
"""

from typing import Dict, Optional, Any, List

from viralify_diagrams.templates.base import (
    DiagramTemplate,
    TemplateConfig,
    TemplateElement,
    TemplateRelation,
    TemplateConstraint,
    ElementShape,
    RelationType,
)


# =============================================================================
# Data Lineage Elements
# =============================================================================

LINEAGE_SOURCE_SYSTEM = TemplateElement(
    id="source_system",
    name="Source System",
    description="Origin of data (OLTP, files, APIs)",
    shape=ElementShape.RECTANGLE,
    default_color="#E6F3FF",
    default_stroke="#0066CC",
    required_fields=["name"],
    optional_fields=["type", "technology", "owner"],
)

LINEAGE_DATABASE = TemplateElement(
    id="database",
    name="Database",
    description="A database (operational or analytical)",
    shape=ElementShape.CYLINDER,
    default_color="#FFFACD",
    default_stroke="#B8860B",
    required_fields=["name"],
    optional_fields=["technology", "schema", "tables"],
)

LINEAGE_DATA_LAKE = TemplateElement(
    id="data_lake",
    name="Data Lake",
    description="Raw data storage (S3, ADLS, GCS)",
    shape=ElementShape.CLOUD,
    default_color="#E6FFE6",
    default_stroke="#059669",
    required_fields=["name"],
    optional_fields=["technology", "format", "zones"],
)

LINEAGE_DATA_WAREHOUSE = TemplateElement(
    id="data_warehouse",
    name="Data Warehouse",
    description="Analytical data warehouse",
    shape=ElementShape.CYLINDER,
    default_color="#FFE6CC",
    default_stroke="#D97706",
    required_fields=["name"],
    optional_fields=["technology", "schema"],
)

LINEAGE_ETL = TemplateElement(
    id="etl",
    name="ETL/ELT Process",
    description="Data transformation process",
    shape=ElementShape.HEXAGON,
    default_color="#E6E6FA",
    default_stroke="#6A5ACD",
    required_fields=["name"],
    optional_fields=["technology", "schedule", "transformations"],
)

LINEAGE_STREAMING = TemplateElement(
    id="streaming",
    name="Streaming Pipeline",
    description="Real-time data streaming",
    shape=ElementShape.PARALLELOGRAM,
    default_color="#FFF0F5",
    default_stroke="#DC2626",
    required_fields=["name"],
    optional_fields=["technology", "throughput"],
)

LINEAGE_API = TemplateElement(
    id="api",
    name="API",
    description="Data API endpoint",
    shape=ElementShape.ROUNDED,
    default_color="#F0F0F0",
    default_stroke="#666666",
    required_fields=["name"],
    optional_fields=["protocol", "format"],
)

LINEAGE_FILE = TemplateElement(
    id="file",
    name="File",
    description="File-based data source",
    shape=ElementShape.FILE,
    default_color="#FFFFFF",
    default_stroke="#999999",
    required_fields=["name"],
    optional_fields=["format", "location"],
)

LINEAGE_BI_TOOL = TemplateElement(
    id="bi_tool",
    name="BI Tool",
    description="Business Intelligence/Analytics tool",
    shape=ElementShape.RECTANGLE,
    default_color="#E8F5E9",
    default_stroke="#2E7D32",
    required_fields=["name"],
    optional_fields=["technology", "dashboards"],
)

LINEAGE_ML_MODEL = TemplateElement(
    id="ml_model",
    name="ML Model",
    description="Machine learning model or feature store",
    shape=ElementShape.HEXAGON,
    default_color="#FCE4EC",
    default_stroke="#C2185B",
    required_fields=["name"],
    optional_fields=["type", "version"],
)

LINEAGE_TABLE = TemplateElement(
    id="table",
    name="Table/Dataset",
    description="A specific table or dataset",
    shape=ElementShape.RECTANGLE,
    default_color="#FFFFFF",
    default_stroke="#333333",
    required_fields=["name"],
    optional_fields=["columns", "row_count", "partitions"],
)

LINEAGE_COLUMN = TemplateElement(
    id="column",
    name="Column",
    description="A specific column (for column-level lineage)",
    shape=ElementShape.RECTANGLE,
    default_color="#F5F5F5",
    default_stroke="#666666",
    required_fields=["name", "table"],
    optional_fields=["type", "description"],
)


# =============================================================================
# Data Lineage Relations
# =============================================================================

LINEAGE_EXTRACTS = TemplateRelation(
    id="extracts",
    name="Extracts",
    relation_type=RelationType.READS_FROM,
    description="Extracts data from source",
    line_style="solid",
    arrow_style="open",
)

LINEAGE_TRANSFORMS = TemplateRelation(
    id="transforms",
    name="Transforms",
    relation_type=RelationType.FLOW,
    description="Transforms data",
    line_style="solid",
    arrow_style="open",
    label_required=True,
)

LINEAGE_LOADS = TemplateRelation(
    id="loads",
    name="Loads",
    relation_type=RelationType.WRITES_TO,
    description="Loads data into target",
    line_style="solid",
    arrow_style="filled",
)

LINEAGE_STREAMS = TemplateRelation(
    id="streams",
    name="Streams",
    relation_type=RelationType.SENDS_TO,
    description="Real-time data flow",
    line_style="dashed",
    arrow_style="open",
)

LINEAGE_DERIVES = TemplateRelation(
    id="derives",
    name="Derives",
    relation_type=RelationType.DEPENDS_ON,
    description="Column derives from another",
    line_style="dotted",
    arrow_style="open",
)

LINEAGE_AGGREGATES = TemplateRelation(
    id="aggregates",
    name="Aggregates",
    relation_type=RelationType.FLOW,
    description="Aggregates multiple sources",
    line_style="solid",
    arrow_style="filled",
)

LINEAGE_JOINS = TemplateRelation(
    id="joins",
    name="Joins",
    relation_type=RelationType.FLOW,
    description="Joins data from sources",
    line_style="solid",
    arrow_style="filled",
)


# =============================================================================
# Data Lineage Template
# =============================================================================

class DataLineageTemplate(DiagramTemplate):
    """
    Data Lineage Diagram Template.

    Shows how data flows and transforms across systems.

    Levels:
    - System-level: High-level view of systems
    - Table-level: Shows specific tables/datasets
    - Column-level: Detailed field-level lineage

    Best practices:
    - Show direction of data flow (left to right typically)
    - Include transformation descriptions
    - Group by data zones (bronze/silver/gold)
    - Show data ownership and stewardship
    """

    def __init__(self):
        config = TemplateConfig(
            template_id="data_lineage",
            name="Data Lineage Diagram",
            description="Shows data flow and transformations",
            version="1.0.0",
            domain="data",
            category="data_flow",
            diagram_type="data_lineage",
            elements=[
                LINEAGE_SOURCE_SYSTEM,
                LINEAGE_DATABASE,
                LINEAGE_DATA_LAKE,
                LINEAGE_DATA_WAREHOUSE,
                LINEAGE_ETL,
                LINEAGE_STREAMING,
                LINEAGE_API,
                LINEAGE_FILE,
                LINEAGE_BI_TOOL,
                LINEAGE_ML_MODEL,
                LINEAGE_TABLE,
                LINEAGE_COLUMN,
            ],
            relations=[
                LINEAGE_EXTRACTS,
                LINEAGE_TRANSFORMS,
                LINEAGE_LOADS,
                LINEAGE_STREAMS,
                LINEAGE_DERIVES,
                LINEAGE_AGGREGATES,
                LINEAGE_JOINS,
            ],
            constraints=[
                TemplateConstraint(
                    id="has_source",
                    name="Has Source",
                    description="Lineage should have at least one source",
                    validator=lambda d: self._validate_has_source(d),
                    severity="warning",
                ),
                TemplateConstraint(
                    id="has_target",
                    name="Has Target",
                    description="Lineage should have at least one target/destination",
                    validator=lambda d: self._validate_has_target(d),
                    severity="warning",
                ),
            ],
            max_elements=40,
            max_relations=60,
            default_layout="horizontal",
            default_theme="corporate",
        )
        super().__init__(config)

    def _validate_has_source(self, diagram) -> List[str]:
        """Validate lineage has source systems"""
        source_types = ['source_system', 'database', 'file', 'api']
        has_source = any(getattr(n, 'element_type', '') in source_types
                        for n in diagram.nodes)
        if not has_source:
            return ["Data lineage should have at least one source system"]
        return []

    def _validate_has_target(self, diagram) -> List[str]:
        """Validate lineage has target systems"""
        target_types = ['data_warehouse', 'bi_tool', 'ml_model', 'database']
        has_target = any(getattr(n, 'element_type', '') in target_types
                        for n in diagram.nodes)
        if not has_target:
            return ["Data lineage should have at least one target system"]
        return []

    def create_element(
        self,
        element_type: str,
        label: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a data lineage element"""
        props = properties or {}

        element_def = self.get_element_definition(element_type)
        if not element_def:
            raise ValueError(f"Unknown element type: {element_type}")

        element = {
            "id": props.get("id", label.lower().replace(" ", "_")),
            "label": label,
            "element_type": element_type,
            "shape": element_def.shape.value,
            "fill_color": props.get("color", element_def.default_color),
            "stroke_color": element_def.default_stroke,
            "technology": props.get("technology"),
            "owner": props.get("owner"),
            "properties": props,
        }

        # Add type-specific properties
        if element_type == "etl":
            element["schedule"] = props.get("schedule")
            element["transformations"] = props.get("transformations", [])
        elif element_type == "streaming":
            element["throughput"] = props.get("throughput")
        elif element_type == "table":
            element["columns"] = props.get("columns", [])
            element["row_count"] = props.get("row_count")
        elif element_type == "column":
            element["table"] = props.get("table")
            element["data_type"] = props.get("type")
        elif element_type == "data_lake":
            element["zones"] = props.get("zones", [])  # bronze, silver, gold
            element["format"] = props.get("format")

        return element

    def create_relation(
        self,
        relation_type: str,
        source_id: str,
        target_id: str,
        label: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a data lineage relation"""
        relation_def = self.get_relation_definition(relation_type)
        if not relation_def:
            relation_def = LINEAGE_TRANSFORMS

        props = properties or {}

        return {
            "source": source_id,
            "target": target_id,
            "label": label or props.get("transformation", ""),
            "relation_type": relation_type,
            "line_style": relation_def.line_style,
            "arrow_style": relation_def.arrow_style,
            "transformation_type": props.get("transformation_type"),
            "schedule": props.get("schedule"),
            "data_volume": props.get("data_volume"),
            "latency": props.get("latency"),
            "properties": props,
        }

    def create_transformation(
        self,
        name: str,
        transformation_type: str,
        sources: List[str],
        target: str,
        description: Optional[str] = None,
        sql: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Helper to create a transformation definition.

        Args:
            name: Transformation name
            transformation_type: filter, aggregate, join, map, etc.
            sources: Source table/column IDs
            target: Target table/column ID
            description: Human-readable description
            sql: SQL expression (if applicable)
        """
        return {
            "name": name,
            "type": transformation_type,
            "sources": sources,
            "target": target,
            "description": description,
            "sql": sql,
        }
