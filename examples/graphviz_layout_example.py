"""
Example: Hybrid Graphviz Layout with viralify-diagrams

This example demonstrates the hybrid approach:
1. Graphviz calculates optimal node positions (edge crossing minimization)
2. viralify-diagrams applies professional theming and exports SVG

This is ideal for:
- Complex diagrams with 50+ components
- Enterprise Integration Patterns
- Microservices architectures
- Data pipelines
"""

from viralify_diagrams import (
    Diagram,
    Cluster,
    GraphvizLayout,
    GraphvizAlgorithm,
    auto_layout,
    SVGExporter,
    get_theme_manager,
)


def create_microservices_diagram():
    """Create a complex microservices architecture diagram"""

    # Create diagram with dark theme
    diagram = Diagram(
        title="E-Commerce Microservices Architecture",
        description="Enterprise-grade microservices with 20+ components",
        theme="dark",  # Will use dark theme colors
        width=1920,
        height=1080,
    )

    # API Gateway cluster
    with diagram.cluster("api_cluster", "API Layer") as api_cluster:
        diagram.add_node("api_gateway", "API Gateway", cluster="api_cluster")
        diagram.add_node("load_balancer", "Load Balancer", cluster="api_cluster")
        diagram.add_node("rate_limiter", "Rate Limiter", cluster="api_cluster")

    # Core Services cluster
    with diagram.cluster("core_cluster", "Core Services") as core:
        diagram.add_node("user_service", "User Service", cluster="core_cluster")
        diagram.add_node("product_service", "Product Service", cluster="core_cluster")
        diagram.add_node("order_service", "Order Service", cluster="core_cluster")
        diagram.add_node("payment_service", "Payment Service", cluster="core_cluster")
        diagram.add_node("inventory_service", "Inventory Service", cluster="core_cluster")
        diagram.add_node("shipping_service", "Shipping Service", cluster="core_cluster")

    # Data Layer cluster
    with diagram.cluster("data_cluster", "Data Layer") as data:
        diagram.add_node("user_db", "User DB (PostgreSQL)", cluster="data_cluster")
        diagram.add_node("product_db", "Product DB (MongoDB)", cluster="data_cluster")
        diagram.add_node("order_db", "Order DB (PostgreSQL)", cluster="data_cluster")
        diagram.add_node("cache", "Redis Cache", cluster="data_cluster")
        diagram.add_node("search", "Elasticsearch", cluster="data_cluster")

    # Event Bus cluster
    with diagram.cluster("event_cluster", "Event Bus") as events:
        diagram.add_node("kafka", "Apache Kafka", cluster="event_cluster")
        diagram.add_node("schema_registry", "Schema Registry", cluster="event_cluster")

    # External Services
    with diagram.cluster("external_cluster", "External Services") as external:
        diagram.add_node("stripe", "Stripe API", cluster="external_cluster")
        diagram.add_node("sendgrid", "SendGrid", cluster="external_cluster")
        diagram.add_node("twilio", "Twilio SMS", cluster="external_cluster")

    # Monitoring cluster
    with diagram.cluster("monitoring_cluster", "Monitoring") as monitoring:
        diagram.add_node("prometheus", "Prometheus", cluster="monitoring_cluster")
        diagram.add_node("grafana", "Grafana", cluster="monitoring_cluster")
        diagram.add_node("jaeger", "Jaeger Tracing", cluster="monitoring_cluster")

    # Add edges (connections)
    # API Layer connections
    diagram.add_edge("load_balancer", "api_gateway", label="route")
    diagram.add_edge("api_gateway", "rate_limiter", label="check")

    # API to Services
    for service in ["user_service", "product_service", "order_service", "payment_service"]:
        diagram.add_edge("api_gateway", service, label="REST")

    # Service to Database connections
    diagram.add_edge("user_service", "user_db", label="CRUD")
    diagram.add_edge("product_service", "product_db", label="CRUD")
    diagram.add_edge("order_service", "order_db", label="CRUD")

    # Service to Cache
    for service in ["user_service", "product_service", "order_service"]:
        diagram.add_edge(service, "cache", label="cache")

    # Service to Search
    diagram.add_edge("product_service", "search", label="index")

    # Event publishing
    for service in ["order_service", "payment_service", "inventory_service", "shipping_service"]:
        diagram.add_edge(service, "kafka", label="publish")

    # Event consumption
    diagram.add_edge("kafka", "inventory_service", label="consume")
    diagram.add_edge("kafka", "shipping_service", label="consume")

    # External service connections
    diagram.add_edge("payment_service", "stripe", label="payment")
    diagram.add_edge("order_service", "sendgrid", label="email")
    diagram.add_edge("shipping_service", "twilio", label="SMS")

    # Monitoring connections
    for service in ["user_service", "product_service", "order_service", "payment_service"]:
        diagram.add_edge(service, "prometheus", label="metrics")
    diagram.add_edge("prometheus", "grafana", label="visualize")
    diagram.add_edge("api_gateway", "jaeger", label="traces")

    return diagram


def main():
    print("Creating microservices architecture diagram...")
    diagram = create_microservices_diagram()

    print(f"Diagram has {len(diagram.nodes)} nodes and {len(diagram.edges)} edges")
    print(f"Clusters: {[c.label for c in diagram.clusters]}")

    # Apply Graphviz layout (hybrid approach)
    print("\nApplying Graphviz layout (algorithm: dot)...")
    layout = GraphvizLayout(
        algorithm="dot",      # Hierarchical layout for directed graphs
        rankdir="TB",         # Top to Bottom
        nodesep=0.8,          # Space between nodes
        ranksep=1.2,          # Space between ranks/levels
        splines="spline",     # Curved edges
    )

    diagram = layout.layout(diagram)
    print(f"Layout complete. Diagram size: {diagram.width}x{diagram.height}")

    # Export to SVG with dark theme
    print("\nExporting to SVG with dark theme...")
    exporter = SVGExporter()
    svg_content = exporter.export(diagram, "microservices_architecture.svg")
    print(f"SVG exported: {len(svg_content)} bytes")

    # Also try auto_layout which recommends the best algorithm
    print("\n--- Testing auto_layout ---")
    diagram2 = create_microservices_diagram()
    diagram2 = auto_layout(diagram2)
    print("Auto layout complete!")

    # Export with ocean theme
    ocean_theme = get_theme_manager().get("ocean")
    exporter_ocean = SVGExporter(theme=ocean_theme)
    svg_ocean = exporter_ocean.export(diagram2, "microservices_ocean.svg")
    print(f"Ocean theme SVG exported: {len(svg_ocean)} bytes")


def example_simple_pipeline():
    """Simple data pipeline example"""
    diagram = Diagram(
        title="Data Pipeline",
        theme="gradient",
        width=1200,
        height=600,
    )

    # Add nodes
    diagram.add_node("source", "Data Source")
    diagram.add_node("ingest", "Kafka Ingest")
    diagram.add_node("transform", "Spark Transform")
    diagram.add_node("warehouse", "Data Warehouse")
    diagram.add_node("analytics", "Analytics")

    # Add edges
    diagram.add_edge("source", "ingest", label="raw data")
    diagram.add_edge("ingest", "transform", label="stream")
    diagram.add_edge("transform", "warehouse", label="batch")
    diagram.add_edge("warehouse", "analytics", label="query")

    # Layout with horizontal flow
    layout = GraphvizLayout(algorithm="dot", rankdir="LR")
    diagram = layout.layout(diagram)

    # Export
    exporter = SVGExporter()
    exporter.export(diagram, "data_pipeline.svg")
    print("Data pipeline diagram exported!")


if __name__ == "__main__":
    main()
    print("\n" + "=" * 50)
    example_simple_pipeline()
