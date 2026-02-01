"""
Presentation Generator Client

Client for communicating with the Viralify presentation-generator service
to get content for populating diagram templates.
"""

import os
import json
from typing import Dict, Optional, Any, List
from dataclasses import dataclass, field
from enum import Enum
import httpx


class ContentType(str, Enum):
    """Types of content that can be requested"""
    ARCHITECTURE = "architecture"
    CLASS_STRUCTURE = "class_structure"
    DATA_FLOW = "data_flow"
    SEQUENCE = "sequence"
    PROCESS = "process"
    DEPLOYMENT = "deployment"
    THREAT_MODEL = "threat_model"
    PIPELINE = "pipeline"


@dataclass
class ContentElement:
    """A single content element for a diagram"""
    id: str
    label: str
    element_type: str
    description: Optional[str] = None
    properties: Dict[str, Any] = field(default_factory=dict)
    children: List['ContentElement'] = field(default_factory=list)


@dataclass
class ContentRelation:
    """A relation between content elements"""
    source_id: str
    target_id: str
    relation_type: str
    label: Optional[str] = None
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DiagramContentRequest:
    """Request for diagram content from presentation-generator"""
    topic: str
    diagram_type: str
    template_id: str
    context: Optional[str] = None
    target_audience: str = "developer"
    complexity: str = "medium"
    max_elements: int = 15
    language: str = "en"
    additional_instructions: Optional[str] = None
    source_documents: List[str] = field(default_factory=list)


@dataclass
class DiagramContentResponse:
    """Response containing content for a diagram"""
    success: bool
    elements: List[ContentElement] = field(default_factory=list)
    relations: List[ContentRelation] = field(default_factory=list)
    title: Optional[str] = None
    description: Optional[str] = None
    narration: Optional[str] = None
    suggested_layout: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None


class PresentationGeneratorClient:
    """
    Client for the Viralify presentation-generator service.

    This client requests diagram content from the presentation-generator,
    which uses AI to generate appropriate elements and relations for diagrams.

    Example:
        >>> client = PresentationGeneratorClient()
        >>> request = DiagramContentRequest(
        ...     topic="Microservices Authentication Flow",
        ...     diagram_type="sequence",
        ...     template_id="uml_sequence"
        ... )
        >>> response = await client.get_diagram_content(request)
        >>> if response.success:
        ...     for element in response.elements:
        ...         print(f"Element: {element.label}")
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: float = 60.0
    ):
        """
        Initialize the client.

        Args:
            base_url: URL of the presentation-generator service
            api_key: API key for authentication (if required)
            timeout: Request timeout in seconds
        """
        self.base_url = base_url or os.getenv(
            "PRESENTATION_GENERATOR_URL",
            "http://localhost:8006"
        )
        self.api_key = api_key or os.getenv("PRESENTATION_GENERATOR_API_KEY")
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client"""
        if self._client is None:
            headers = {"Content-Type": "application/json"}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"

            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                headers=headers,
                timeout=self.timeout
            )
        return self._client

    async def close(self):
        """Close the HTTP client"""
        if self._client:
            await self._client.aclose()
            self._client = None

    async def get_diagram_content(
        self,
        request: DiagramContentRequest
    ) -> DiagramContentResponse:
        """
        Request diagram content from the presentation-generator.

        Args:
            request: The content request specification

        Returns:
            DiagramContentResponse with elements and relations
        """
        client = await self._get_client()

        try:
            payload = {
                "topic": request.topic,
                "diagram_type": request.diagram_type,
                "template_id": request.template_id,
                "context": request.context,
                "target_audience": request.target_audience,
                "complexity": request.complexity,
                "max_elements": request.max_elements,
                "language": request.language,
                "additional_instructions": request.additional_instructions,
                "source_documents": request.source_documents,
            }

            response = await client.post(
                "/api/v1/diagrams/content",
                json=payload
            )

            if response.status_code == 200:
                data = response.json()
                return self._parse_response(data)
            else:
                return DiagramContentResponse(
                    success=False,
                    error=f"Request failed with status {response.status_code}: {response.text}"
                )

        except httpx.TimeoutException:
            return DiagramContentResponse(
                success=False,
                error="Request timed out"
            )
        except Exception as e:
            return DiagramContentResponse(
                success=False,
                error=f"Request failed: {str(e)}"
            )

    def _parse_response(self, data: Dict[str, Any]) -> DiagramContentResponse:
        """Parse API response into DiagramContentResponse"""
        elements = []
        for elem_data in data.get("elements", []):
            element = ContentElement(
                id=elem_data.get("id", ""),
                label=elem_data.get("label", ""),
                element_type=elem_data.get("element_type", ""),
                description=elem_data.get("description"),
                properties=elem_data.get("properties", {}),
                children=[
                    ContentElement(**child)
                    for child in elem_data.get("children", [])
                ]
            )
            elements.append(element)

        relations = []
        for rel_data in data.get("relations", []):
            relation = ContentRelation(
                source_id=rel_data.get("source_id", ""),
                target_id=rel_data.get("target_id", ""),
                relation_type=rel_data.get("relation_type", ""),
                label=rel_data.get("label"),
                properties=rel_data.get("properties", {})
            )
            relations.append(relation)

        return DiagramContentResponse(
            success=True,
            elements=elements,
            relations=relations,
            title=data.get("title"),
            description=data.get("description"),
            narration=data.get("narration"),
            suggested_layout=data.get("suggested_layout"),
            metadata=data.get("metadata", {})
        )

    async def check_health(self) -> bool:
        """Check if the presentation-generator service is healthy"""
        client = await self._get_client()
        try:
            response = await client.get("/health")
            return response.status_code == 200
        except Exception:
            return False

    async def get_supported_diagram_types(self) -> List[str]:
        """Get list of diagram types supported by the service"""
        client = await self._get_client()
        try:
            response = await client.get("/api/v1/diagrams/types")
            if response.status_code == 200:
                return response.json().get("types", [])
            return []
        except Exception:
            return []


# Singleton instance
_client: Optional[PresentationGeneratorClient] = None


def get_presentation_client() -> PresentationGeneratorClient:
    """Get the global presentation generator client"""
    global _client
    if _client is None:
        _client = PresentationGeneratorClient()
    return _client


# Synchronous wrapper for simple use cases
def get_diagram_content_sync(
    topic: str,
    diagram_type: str,
    template_id: str,
    **kwargs
) -> DiagramContentResponse:
    """
    Synchronous wrapper for getting diagram content.

    This uses a fallback approach when async is not available,
    returning mock content for local development.
    """
    import asyncio

    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Can't use async in running loop, return mock
            return _generate_mock_content(topic, diagram_type, template_id)
    except RuntimeError:
        pass

    # Try async call
    try:
        client = get_presentation_client()
        request = DiagramContentRequest(
            topic=topic,
            diagram_type=diagram_type,
            template_id=template_id,
            **kwargs
        )
        return asyncio.run(client.get_diagram_content(request))
    except Exception as e:
        return DiagramContentResponse(
            success=False,
            error=f"Sync call failed: {str(e)}"
        )


def _generate_mock_content(
    topic: str,
    diagram_type: str,
    template_id: str
) -> DiagramContentResponse:
    """Generate mock content for local development"""
    # Generate simple mock elements based on diagram type
    if "c4" in template_id.lower() or "architecture" in diagram_type.lower():
        elements = [
            ContentElement(
                id="user",
                label="User",
                element_type="person",
                description="End user of the system"
            ),
            ContentElement(
                id="system",
                label=topic,
                element_type="software_system",
                description=f"The {topic} system"
            ),
            ContentElement(
                id="database",
                label="Database",
                element_type="database",
                description="Data storage"
            ),
        ]
        relations = [
            ContentRelation(
                source_id="user",
                target_id="system",
                relation_type="uses",
                label="Uses"
            ),
            ContentRelation(
                source_id="system",
                target_id="database",
                relation_type="reads_from",
                label="Reads/Writes"
            ),
        ]
    elif "sequence" in template_id.lower():
        elements = [
            ContentElement(id="client", label="Client", element_type="actor"),
            ContentElement(id="api", label="API", element_type="object"),
            ContentElement(id="service", label="Service", element_type="object"),
        ]
        relations = [
            ContentRelation(
                source_id="client",
                target_id="api",
                relation_type="sync_call",
                label="Request"
            ),
            ContentRelation(
                source_id="api",
                target_id="service",
                relation_type="sync_call",
                label="Process"
            ),
        ]
    else:
        # Generic fallback
        elements = [
            ContentElement(id="node1", label="Component A", element_type="process"),
            ContentElement(id="node2", label="Component B", element_type="process"),
        ]
        relations = [
            ContentRelation(
                source_id="node1",
                target_id="node2",
                relation_type="flow",
                label="Data"
            ),
        ]

    return DiagramContentResponse(
        success=True,
        elements=elements,
        relations=relations,
        title=topic,
        description=f"Diagram for {topic}",
        metadata={"mock": True}
    )
