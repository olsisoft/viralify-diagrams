"""
Icon Registry - Central management for all icons

Provides:
- Icon loading and caching
- Category-based organization
- SVG content retrieval
- Icon metadata
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from pathlib import Path
import json

from viralify_diagrams.icons.categories import IconCategory, IconProvider


@dataclass
class IconInfo:
    """Metadata for an icon"""
    id: str                          # e.g., "aws/compute/ec2"
    name: str                        # e.g., "Amazon EC2"
    provider: IconProvider
    category: IconCategory
    svg_content: str                 # Inline SVG content
    width: int = 64
    height: int = 64
    keywords: List[str] = field(default_factory=list)
    aliases: List[str] = field(default_factory=list)


class IconRegistry:
    """
    Central registry for all diagram icons.

    Manages loading, caching, and retrieval of cloud provider
    and technology icons.
    """

    def __init__(self):
        self._icons: Dict[str, IconInfo] = {}
        self._by_category: Dict[IconCategory, List[str]] = {}
        self._by_provider: Dict[IconProvider, List[str]] = {}
        self._loaded = False

    def _ensure_loaded(self):
        """Lazy-load built-in icons"""
        if not self._loaded:
            self._load_builtin_icons()
            self._loaded = True

    def _load_builtin_icons(self):
        """Load all built-in icons"""
        # AWS Icons
        self._register_aws_icons()
        # GCP Icons
        self._register_gcp_icons()
        # Azure Icons
        self._register_azure_icons()
        # Kubernetes Icons
        self._register_k8s_icons()
        # Generic Icons
        self._register_generic_icons()

    def register(self, icon: IconInfo) -> None:
        """Register an icon"""
        self._icons[icon.id] = icon

        # Index by category
        if icon.category not in self._by_category:
            self._by_category[icon.category] = []
        self._by_category[icon.category].append(icon.id)

        # Index by provider
        if icon.provider not in self._by_provider:
            self._by_provider[icon.provider] = []
        self._by_provider[icon.provider].append(icon.id)

        # Index aliases
        for alias in icon.aliases:
            self._icons[alias] = icon

    def get(self, icon_id: str) -> Optional[IconInfo]:
        """Get an icon by ID"""
        self._ensure_loaded()
        return self._icons.get(icon_id)

    def get_svg(self, icon_id: str) -> Optional[str]:
        """Get SVG content for an icon"""
        icon = self.get(icon_id)
        return icon.svg_content if icon else None

    def list_by_category(self, category: IconCategory) -> List[str]:
        """List all icon IDs in a category"""
        self._ensure_loaded()
        return self._by_category.get(category, [])

    def list_by_provider(self, provider: IconProvider) -> List[str]:
        """List all icon IDs from a provider"""
        self._ensure_loaded()
        return self._by_provider.get(provider, [])

    def list_all(self) -> List[str]:
        """List all icon IDs"""
        self._ensure_loaded()
        return list(set(icon.id for icon in self._icons.values()))

    def search(self, query: str) -> List[IconInfo]:
        """Search icons by name or keywords"""
        self._ensure_loaded()
        query = query.lower()
        results = []
        seen = set()

        for icon in self._icons.values():
            if icon.id in seen:
                continue
            if (query in icon.name.lower() or
                query in icon.id.lower() or
                any(query in kw.lower() for kw in icon.keywords)):
                results.append(icon)
                seen.add(icon.id)

        return results

    # =========================================================================
    # AWS Icons
    # =========================================================================
    def _register_aws_icons(self):
        """Register AWS Architecture Icons"""

        # EC2
        self.register(IconInfo(
            id="aws/compute/ec2",
            name="Amazon EC2",
            provider=IconProvider.AWS,
            category=IconCategory.COMPUTE,
            keywords=["instance", "server", "virtual machine", "vm"],
            aliases=["ec2", "aws-ec2"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="aws-ec2-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#FF9900"/>
      <stop offset="100%" style="stop-color:#FF6600"/>
    </linearGradient>
  </defs>
  <rect x="4" y="4" width="56" height="56" rx="4" fill="url(#aws-ec2-grad)"/>
  <rect x="12" y="16" width="40" height="32" rx="2" fill="#232F3E"/>
  <rect x="16" y="20" width="32" height="24" rx="1" fill="#FF9900" opacity="0.3"/>
  <circle cx="20" cy="44" r="2" fill="#FF9900"/>
  <rect x="26" y="42" width="20" height="4" rx="1" fill="#FF9900"/>
</svg>'''
        ))

        # Lambda
        self.register(IconInfo(
            id="aws/compute/lambda",
            name="AWS Lambda",
            provider=IconProvider.AWS,
            category=IconCategory.SERVERLESS,
            keywords=["function", "serverless", "faas"],
            aliases=["lambda", "aws-lambda"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="aws-lambda-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#FF9900"/>
      <stop offset="100%" style="stop-color:#FF6600"/>
    </linearGradient>
  </defs>
  <rect x="4" y="4" width="56" height="56" rx="4" fill="url(#aws-lambda-grad)"/>
  <path d="M20 48 L32 16 L36 16 L28 36 L40 36 L26 48 Z" fill="#232F3E"/>
</svg>'''
        ))

        # S3
        self.register(IconInfo(
            id="aws/storage/s3",
            name="Amazon S3",
            provider=IconProvider.AWS,
            category=IconCategory.STORAGE,
            keywords=["bucket", "object storage", "files"],
            aliases=["s3", "aws-s3"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="aws-s3-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#3ECF8E"/>
      <stop offset="100%" style="stop-color:#2DA66E"/>
    </linearGradient>
  </defs>
  <rect x="4" y="4" width="56" height="56" rx="4" fill="url(#aws-s3-grad)"/>
  <ellipse cx="32" cy="20" rx="20" ry="8" fill="#232F3E"/>
  <path d="M12 20 L12 44 C12 48.4 21 52 32 52 C43 52 52 48.4 52 44 L52 20" fill="none" stroke="#232F3E" stroke-width="4"/>
  <ellipse cx="32" cy="44" rx="20" ry="8" fill="#232F3E"/>
</svg>'''
        ))

        # RDS
        self.register(IconInfo(
            id="aws/database/rds",
            name="Amazon RDS",
            provider=IconProvider.AWS,
            category=IconCategory.DATABASE,
            keywords=["mysql", "postgres", "database", "sql"],
            aliases=["rds", "aws-rds"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="aws-rds-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#2E7D32"/>
      <stop offset="100%" style="stop-color:#1B5E20"/>
    </linearGradient>
  </defs>
  <rect x="4" y="4" width="56" height="56" rx="4" fill="url(#aws-rds-grad)"/>
  <ellipse cx="32" cy="16" rx="16" ry="6" fill="#FFFFFF" opacity="0.9"/>
  <rect x="16" y="16" width="32" height="32" fill="#FFFFFF" opacity="0.9"/>
  <ellipse cx="32" cy="48" rx="16" ry="6" fill="#FFFFFF" opacity="0.9"/>
  <ellipse cx="32" cy="26" rx="16" ry="6" fill="none" stroke="#2E7D32" stroke-width="2"/>
  <ellipse cx="32" cy="38" rx="16" ry="6" fill="none" stroke="#2E7D32" stroke-width="2"/>
</svg>'''
        ))

        # DynamoDB
        self.register(IconInfo(
            id="aws/database/dynamodb",
            name="Amazon DynamoDB",
            provider=IconProvider.AWS,
            category=IconCategory.DATABASE,
            keywords=["nosql", "key-value", "document"],
            aliases=["dynamodb", "aws-dynamodb"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="aws-ddb-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#2E7D32"/>
      <stop offset="100%" style="stop-color:#1B5E20"/>
    </linearGradient>
  </defs>
  <rect x="4" y="4" width="56" height="56" rx="4" fill="url(#aws-ddb-grad)"/>
  <path d="M16 32 L32 16 L48 32 L32 48 Z" fill="#FFFFFF" opacity="0.9"/>
  <circle cx="32" cy="32" r="8" fill="#2E7D32"/>
</svg>'''
        ))

        # API Gateway
        self.register(IconInfo(
            id="aws/network/api-gateway",
            name="Amazon API Gateway",
            provider=IconProvider.AWS,
            category=IconCategory.API,
            keywords=["rest", "http", "websocket", "api"],
            aliases=["api-gateway", "aws-api-gateway", "apigw"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="aws-apigw-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#7B1FA2"/>
      <stop offset="100%" style="stop-color:#6A1B9A"/>
    </linearGradient>
  </defs>
  <rect x="4" y="4" width="56" height="56" rx="4" fill="url(#aws-apigw-grad)"/>
  <rect x="26" y="12" width="12" height="40" rx="2" fill="#FFFFFF" opacity="0.9"/>
  <path d="M14 24 L26 32 L14 40" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>
  <path d="M50 24 L38 32 L50 40" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>
</svg>'''
        ))

        # ELB/ALB
        self.register(IconInfo(
            id="aws/network/elb",
            name="Elastic Load Balancer",
            provider=IconProvider.AWS,
            category=IconCategory.LOAD_BALANCER,
            keywords=["alb", "nlb", "load balancer", "traffic"],
            aliases=["elb", "alb", "aws-elb", "aws-alb"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="aws-elb-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#5E35B1"/>
      <stop offset="100%" style="stop-color:#4527A0"/>
    </linearGradient>
  </defs>
  <rect x="4" y="4" width="56" height="56" rx="4" fill="url(#aws-elb-grad)"/>
  <circle cx="20" cy="32" r="10" fill="#FFFFFF" opacity="0.9"/>
  <circle cx="44" cy="18" r="6" fill="#FFFFFF" opacity="0.9"/>
  <circle cx="44" cy="32" r="6" fill="#FFFFFF" opacity="0.9"/>
  <circle cx="44" cy="46" r="6" fill="#FFFFFF" opacity="0.9"/>
  <path d="M30 28 L38 18" stroke="#FFFFFF" stroke-width="2"/>
  <path d="M30 32 L38 32" stroke="#FFFFFF" stroke-width="2"/>
  <path d="M30 36 L38 46" stroke="#FFFFFF" stroke-width="2"/>
</svg>'''
        ))

        # CloudFront
        self.register(IconInfo(
            id="aws/network/cloudfront",
            name="Amazon CloudFront",
            provider=IconProvider.AWS,
            category=IconCategory.CDN,
            keywords=["cdn", "edge", "cache", "distribution"],
            aliases=["cloudfront", "aws-cloudfront"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="aws-cf-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#9C27B0"/>
      <stop offset="100%" style="stop-color:#7B1FA2"/>
    </linearGradient>
  </defs>
  <rect x="4" y="4" width="56" height="56" rx="4" fill="url(#aws-cf-grad)"/>
  <circle cx="32" cy="32" r="16" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.9"/>
  <circle cx="32" cy="32" r="8" fill="#FFFFFF" opacity="0.9"/>
  <circle cx="32" cy="12" r="4" fill="#FFFFFF" opacity="0.9"/>
  <circle cx="32" cy="52" r="4" fill="#FFFFFF" opacity="0.9"/>
  <circle cx="12" cy="32" r="4" fill="#FFFFFF" opacity="0.9"/>
  <circle cx="52" cy="32" r="4" fill="#FFFFFF" opacity="0.9"/>
</svg>'''
        ))

        # SQS
        self.register(IconInfo(
            id="aws/integration/sqs",
            name="Amazon SQS",
            provider=IconProvider.AWS,
            category=IconCategory.QUEUE,
            keywords=["queue", "message", "fifo"],
            aliases=["sqs", "aws-sqs"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="aws-sqs-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#FF5722"/>
      <stop offset="100%" style="stop-color:#E64A19"/>
    </linearGradient>
  </defs>
  <rect x="4" y="4" width="56" height="56" rx="4" fill="url(#aws-sqs-grad)"/>
  <rect x="12" y="20" width="40" height="24" rx="4" fill="#FFFFFF" opacity="0.9"/>
  <rect x="16" y="26" width="8" height="12" rx="1" fill="#FF5722"/>
  <rect x="28" y="26" width="8" height="12" rx="1" fill="#FF5722"/>
  <rect x="40" y="26" width="8" height="12" rx="1" fill="#FF5722"/>
</svg>'''
        ))

        # SNS
        self.register(IconInfo(
            id="aws/integration/sns",
            name="Amazon SNS",
            provider=IconProvider.AWS,
            category=IconCategory.MESSAGING,
            keywords=["notification", "pubsub", "topic"],
            aliases=["sns", "aws-sns"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="aws-sns-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#FF5722"/>
      <stop offset="100%" style="stop-color:#E64A19"/>
    </linearGradient>
  </defs>
  <rect x="4" y="4" width="56" height="56" rx="4" fill="url(#aws-sns-grad)"/>
  <circle cx="32" cy="32" r="12" fill="#FFFFFF" opacity="0.9"/>
  <circle cx="16" cy="20" r="6" fill="#FFFFFF" opacity="0.9"/>
  <circle cx="48" cy="20" r="6" fill="#FFFFFF" opacity="0.9"/>
  <circle cx="16" cy="44" r="6" fill="#FFFFFF" opacity="0.9"/>
  <circle cx="48" cy="44" r="6" fill="#FFFFFF" opacity="0.9"/>
  <path d="M32 20 L16 20 M32 20 L48 20 M32 44 L16 44 M32 44 L48 44" stroke="#FF5722" stroke-width="2"/>
</svg>'''
        ))

        # VPC
        self.register(IconInfo(
            id="aws/network/vpc",
            name="Amazon VPC",
            provider=IconProvider.AWS,
            category=IconCategory.NETWORK,
            keywords=["virtual private cloud", "network", "subnet"],
            aliases=["vpc", "aws-vpc"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="aws-vpc-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#7B1FA2"/>
      <stop offset="100%" style="stop-color:#6A1B9A"/>
    </linearGradient>
  </defs>
  <rect x="4" y="4" width="56" height="56" rx="4" fill="url(#aws-vpc-grad)"/>
  <rect x="12" y="12" width="40" height="40" rx="4" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-dasharray="8,4"/>
  <rect x="20" y="20" width="24" height="24" rx="2" fill="#FFFFFF" opacity="0.3"/>
</svg>'''
        ))

        # ElastiCache
        self.register(IconInfo(
            id="aws/database/elasticache",
            name="Amazon ElastiCache",
            provider=IconProvider.AWS,
            category=IconCategory.CACHE,
            keywords=["redis", "memcached", "cache", "in-memory"],
            aliases=["elasticache", "aws-elasticache", "aws-redis"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="aws-cache-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#4CAF50"/>
      <stop offset="100%" style="stop-color:#388E3C"/>
    </linearGradient>
  </defs>
  <rect x="4" y="4" width="56" height="56" rx="4" fill="url(#aws-cache-grad)"/>
  <path d="M32 12 L48 22 L48 42 L32 52 L16 42 L16 22 Z" fill="#FFFFFF" opacity="0.9"/>
  <path d="M32 12 L32 32 L16 22" fill="none" stroke="#4CAF50" stroke-width="2"/>
  <path d="M32 32 L48 22" fill="none" stroke="#4CAF50" stroke-width="2"/>
  <path d="M32 32 L32 52" fill="none" stroke="#4CAF50" stroke-width="2"/>
</svg>'''
        ))

        # CloudWatch
        self.register(IconInfo(
            id="aws/management/cloudwatch",
            name="Amazon CloudWatch",
            provider=IconProvider.AWS,
            category=IconCategory.MONITORING,
            keywords=["metrics", "logs", "alarms", "monitoring"],
            aliases=["cloudwatch", "aws-cloudwatch"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="aws-cw-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#FF5722"/>
      <stop offset="100%" style="stop-color:#E64A19"/>
    </linearGradient>
  </defs>
  <rect x="4" y="4" width="56" height="56" rx="4" fill="url(#aws-cw-grad)"/>
  <circle cx="32" cy="32" r="16" fill="none" stroke="#FFFFFF" stroke-width="3"/>
  <path d="M32 20 L32 32 L40 36" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>
</svg>'''
        ))

        # EKS
        self.register(IconInfo(
            id="aws/container/eks",
            name="Amazon EKS",
            provider=IconProvider.AWS,
            category=IconCategory.CONTAINER,
            keywords=["kubernetes", "k8s", "container", "orchestration"],
            aliases=["eks", "aws-eks"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="aws-eks-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#FF6B35"/>
      <stop offset="100%" style="stop-color:#CC5529"/>
    </linearGradient>
  </defs>
  <rect x="4" y="4" width="56" height="56" rx="4" fill="url(#aws-eks-grad)"/>
  <path d="M32 12 L48 22 L48 42 L32 52 L16 42 L16 22 Z" fill="#FFFFFF" opacity="0.9"/>
  <circle cx="32" cy="32" r="6" fill="#FF6B35"/>
  <circle cx="24" cy="22" r="3" fill="#FF6B35"/>
  <circle cx="40" cy="22" r="3" fill="#FF6B35"/>
  <circle cx="24" cy="42" r="3" fill="#FF6B35"/>
  <circle cx="40" cy="42" r="3" fill="#FF6B35"/>
</svg>'''
        ))

        # ECS
        self.register(IconInfo(
            id="aws/container/ecs",
            name="Amazon ECS",
            provider=IconProvider.AWS,
            category=IconCategory.CONTAINER,
            keywords=["container", "docker", "fargate"],
            aliases=["ecs", "aws-ecs"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="aws-ecs-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#FF6B35"/>
      <stop offset="100%" style="stop-color:#CC5529"/>
    </linearGradient>
  </defs>
  <rect x="4" y="4" width="56" height="56" rx="4" fill="url(#aws-ecs-grad)"/>
  <rect x="16" y="16" width="14" height="14" rx="2" fill="#FFFFFF" opacity="0.9"/>
  <rect x="34" y="16" width="14" height="14" rx="2" fill="#FFFFFF" opacity="0.9"/>
  <rect x="16" y="34" width="14" height="14" rx="2" fill="#FFFFFF" opacity="0.9"/>
  <rect x="34" y="34" width="14" height="14" rx="2" fill="#FFFFFF" opacity="0.9"/>
</svg>'''
        ))

        # Cognito
        self.register(IconInfo(
            id="aws/security/cognito",
            name="Amazon Cognito",
            provider=IconProvider.AWS,
            category=IconCategory.IAM,
            keywords=["auth", "authentication", "identity", "user pool"],
            aliases=["cognito", "aws-cognito"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="aws-cognito-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#F44336"/>
      <stop offset="100%" style="stop-color:#D32F2F"/>
    </linearGradient>
  </defs>
  <rect x="4" y="4" width="56" height="56" rx="4" fill="url(#aws-cognito-grad)"/>
  <circle cx="32" cy="24" r="10" fill="#FFFFFF" opacity="0.9"/>
  <path d="M18 48 C18 38 46 38 46 48" fill="#FFFFFF" opacity="0.9"/>
</svg>'''
        ))

        # IAM
        self.register(IconInfo(
            id="aws/security/iam",
            name="AWS IAM",
            provider=IconProvider.AWS,
            category=IconCategory.IAM,
            keywords=["identity", "access", "policy", "role"],
            aliases=["iam", "aws-iam"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="aws-iam-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#E53935"/>
      <stop offset="100%" style="stop-color:#C62828"/>
    </linearGradient>
  </defs>
  <rect x="4" y="4" width="56" height="56" rx="4" fill="url(#aws-iam-grad)"/>
  <path d="M32 12 L32 20 M24 20 L40 20 L40 36 L32 44 L24 36 L24 20" fill="#FFFFFF" opacity="0.9"/>
  <circle cx="32" cy="52" r="4" fill="#FFFFFF" opacity="0.9"/>
  <path d="M32 44 L32 48" stroke="#FFFFFF" stroke-width="2"/>
</svg>'''
        ))

        # Kinesis
        self.register(IconInfo(
            id="aws/analytics/kinesis",
            name="Amazon Kinesis",
            provider=IconProvider.AWS,
            category=IconCategory.DATA,
            keywords=["streaming", "real-time", "data stream"],
            aliases=["kinesis", "aws-kinesis"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="aws-kinesis-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#00796B"/>
      <stop offset="100%" style="stop-color:#00695C"/>
    </linearGradient>
  </defs>
  <rect x="4" y="4" width="56" height="56" rx="4" fill="url(#aws-kinesis-grad)"/>
  <path d="M12 20 Q32 12 52 20" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.9"/>
  <path d="M12 32 Q32 24 52 32" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.9"/>
  <path d="M12 44 Q32 36 52 44" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.9"/>
</svg>'''
        ))

    # =========================================================================
    # GCP Icons
    # =========================================================================
    def _register_gcp_icons(self):
        """Register Google Cloud Platform Icons"""

        # Compute Engine
        self.register(IconInfo(
            id="gcp/compute/gce",
            name="Compute Engine",
            provider=IconProvider.GCP,
            category=IconCategory.COMPUTE,
            keywords=["vm", "instance", "server"],
            aliases=["gce", "gcp-compute"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="4" width="56" height="56" rx="4" fill="#4285F4"/>
  <rect x="14" y="18" width="36" height="28" rx="2" fill="#FFFFFF"/>
  <rect x="18" y="22" width="28" height="16" rx="1" fill="#4285F4" opacity="0.3"/>
  <circle cx="22" cy="42" r="2" fill="#4285F4"/>
  <rect x="28" y="40" width="16" height="4" rx="1" fill="#4285F4"/>
</svg>'''
        ))

        # Cloud Functions
        self.register(IconInfo(
            id="gcp/compute/functions",
            name="Cloud Functions",
            provider=IconProvider.GCP,
            category=IconCategory.SERVERLESS,
            keywords=["serverless", "function", "faas"],
            aliases=["gcf", "gcp-functions"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="4" width="56" height="56" rx="4" fill="#4285F4"/>
  <path d="M20 48 L32 16 L36 16 L28 36 L40 36 L26 48 Z" fill="#FFFFFF"/>
</svg>'''
        ))

        # Cloud Storage
        self.register(IconInfo(
            id="gcp/storage/gcs",
            name="Cloud Storage",
            provider=IconProvider.GCP,
            category=IconCategory.STORAGE,
            keywords=["bucket", "object storage", "files"],
            aliases=["gcs", "gcp-storage"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="4" width="56" height="56" rx="4" fill="#4285F4"/>
  <path d="M16 28 L32 16 L48 28 L48 44 L32 52 L16 44 Z" fill="#FFFFFF"/>
  <path d="M32 16 L32 36 M16 28 L32 36 L48 28" fill="none" stroke="#4285F4" stroke-width="2"/>
</svg>'''
        ))

        # Cloud SQL
        self.register(IconInfo(
            id="gcp/database/cloudsql",
            name="Cloud SQL",
            provider=IconProvider.GCP,
            category=IconCategory.DATABASE,
            keywords=["mysql", "postgres", "sql server"],
            aliases=["cloudsql", "gcp-sql"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="4" width="56" height="56" rx="4" fill="#4285F4"/>
  <ellipse cx="32" cy="18" rx="14" ry="6" fill="#FFFFFF"/>
  <rect x="18" y="18" width="28" height="28" fill="#FFFFFF"/>
  <ellipse cx="32" cy="46" rx="14" ry="6" fill="#FFFFFF"/>
  <ellipse cx="32" cy="28" rx="14" ry="6" fill="none" stroke="#4285F4" stroke-width="2"/>
  <ellipse cx="32" cy="38" rx="14" ry="6" fill="none" stroke="#4285F4" stroke-width="2"/>
</svg>'''
        ))

        # BigQuery
        self.register(IconInfo(
            id="gcp/analytics/bigquery",
            name="BigQuery",
            provider=IconProvider.GCP,
            category=IconCategory.ANALYTICS,
            keywords=["data warehouse", "sql", "analytics"],
            aliases=["bigquery", "bq", "gcp-bigquery"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="4" width="56" height="56" rx="4" fill="#4285F4"/>
  <path d="M20 20 L32 12 L44 20 L44 44 L32 52 L20 44 Z" fill="#FFFFFF"/>
  <circle cx="32" cy="32" r="8" fill="#4285F4"/>
  <path d="M38 38 L46 46" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>
</svg>'''
        ))

        # Pub/Sub
        self.register(IconInfo(
            id="gcp/integration/pubsub",
            name="Pub/Sub",
            provider=IconProvider.GCP,
            category=IconCategory.MESSAGING,
            keywords=["messaging", "queue", "events"],
            aliases=["pubsub", "gcp-pubsub"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="4" width="56" height="56" rx="4" fill="#4285F4"/>
  <circle cx="32" cy="32" r="10" fill="#FFFFFF"/>
  <circle cx="16" cy="20" r="6" fill="#FFFFFF"/>
  <circle cx="48" cy="20" r="6" fill="#FFFFFF"/>
  <circle cx="16" cy="44" r="6" fill="#FFFFFF"/>
  <circle cx="48" cy="44" r="6" fill="#FFFFFF"/>
  <path d="M32 22 L16 20 M32 22 L48 20 M32 42 L16 44 M32 42 L48 44" stroke="#4285F4" stroke-width="2"/>
</svg>'''
        ))

        # GKE
        self.register(IconInfo(
            id="gcp/container/gke",
            name="Google Kubernetes Engine",
            provider=IconProvider.GCP,
            category=IconCategory.CONTAINER,
            keywords=["kubernetes", "k8s", "container"],
            aliases=["gke", "gcp-gke"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="4" width="56" height="56" rx="4" fill="#4285F4"/>
  <path d="M32 12 L48 22 L48 42 L32 52 L16 42 L16 22 Z" fill="#FFFFFF"/>
  <circle cx="32" cy="32" r="6" fill="#4285F4"/>
  <circle cx="24" cy="22" r="3" fill="#4285F4"/>
  <circle cx="40" cy="22" r="3" fill="#4285F4"/>
  <circle cx="24" cy="42" r="3" fill="#4285F4"/>
  <circle cx="40" cy="42" r="3" fill="#4285F4"/>
</svg>'''
        ))

        # Cloud Run
        self.register(IconInfo(
            id="gcp/container/cloudrun",
            name="Cloud Run",
            provider=IconProvider.GCP,
            category=IconCategory.SERVERLESS,
            keywords=["container", "serverless", "knative"],
            aliases=["cloudrun", "gcp-cloudrun"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="4" width="56" height="56" rx="4" fill="#4285F4"/>
  <path d="M20 44 L32 20 L44 44 Z" fill="#FFFFFF"/>
  <circle cx="32" cy="36" r="4" fill="#4285F4"/>
</svg>'''
        ))

        # Cloud Load Balancing
        self.register(IconInfo(
            id="gcp/network/loadbalancing",
            name="Cloud Load Balancing",
            provider=IconProvider.GCP,
            category=IconCategory.LOAD_BALANCER,
            keywords=["lb", "traffic", "balancer"],
            aliases=["gcp-lb", "gcp-loadbalancing"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="4" width="56" height="56" rx="4" fill="#4285F4"/>
  <circle cx="20" cy="32" r="10" fill="#FFFFFF"/>
  <circle cx="44" cy="18" r="6" fill="#FFFFFF"/>
  <circle cx="44" cy="32" r="6" fill="#FFFFFF"/>
  <circle cx="44" cy="46" r="6" fill="#FFFFFF"/>
  <path d="M30 28 L38 18 M30 32 L38 32 M30 36 L38 46" stroke="#FFFFFF" stroke-width="2"/>
</svg>'''
        ))

        # VPC
        self.register(IconInfo(
            id="gcp/network/vpc",
            name="Virtual Private Cloud",
            provider=IconProvider.GCP,
            category=IconCategory.NETWORK,
            keywords=["network", "vpc", "subnet"],
            aliases=["gcp-vpc"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="4" width="56" height="56" rx="4" fill="#4285F4"/>
  <rect x="12" y="12" width="40" height="40" rx="4" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-dasharray="8,4"/>
  <rect x="20" y="20" width="24" height="24" rx="2" fill="#FFFFFF" opacity="0.3"/>
</svg>'''
        ))

        # Firestore
        self.register(IconInfo(
            id="gcp/database/firestore",
            name="Cloud Firestore",
            provider=IconProvider.GCP,
            category=IconCategory.DATABASE,
            keywords=["nosql", "document", "realtime"],
            aliases=["firestore", "gcp-firestore"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="4" width="56" height="56" rx="4" fill="#FBBC04"/>
  <path d="M32 12 L20 24 L32 36 L44 24 Z" fill="#FFFFFF"/>
  <path d="M20 40 L32 52 L44 40 L32 28 Z" fill="#FFFFFF"/>
</svg>'''
        ))

        # Cloud CDN
        self.register(IconInfo(
            id="gcp/network/cdn",
            name="Cloud CDN",
            provider=IconProvider.GCP,
            category=IconCategory.CDN,
            keywords=["cdn", "cache", "edge"],
            aliases=["gcp-cdn"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="4" width="56" height="56" rx="4" fill="#4285F4"/>
  <circle cx="32" cy="32" r="16" fill="none" stroke="#FFFFFF" stroke-width="3"/>
  <circle cx="32" cy="32" r="8" fill="#FFFFFF"/>
  <circle cx="32" cy="12" r="4" fill="#FFFFFF"/>
  <circle cx="32" cy="52" r="4" fill="#FFFFFF"/>
  <circle cx="12" cy="32" r="4" fill="#FFFFFF"/>
  <circle cx="52" cy="32" r="4" fill="#FFFFFF"/>
</svg>'''
        ))

    # =========================================================================
    # Azure Icons
    # =========================================================================
    def _register_azure_icons(self):
        """Register Microsoft Azure Icons"""

        # Virtual Machines
        self.register(IconInfo(
            id="azure/compute/vm",
            name="Virtual Machines",
            provider=IconProvider.AZURE,
            category=IconCategory.COMPUTE,
            keywords=["vm", "instance", "server"],
            aliases=["azure-vm", "azure-compute"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="azure-vm-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0078D4"/>
      <stop offset="100%" style="stop-color:#005A9E"/>
    </linearGradient>
  </defs>
  <rect x="4" y="4" width="56" height="56" rx="4" fill="url(#azure-vm-grad)"/>
  <rect x="14" y="18" width="36" height="28" rx="2" fill="#FFFFFF"/>
  <rect x="18" y="22" width="28" height="16" rx="1" fill="#0078D4" opacity="0.3"/>
  <circle cx="22" cy="42" r="2" fill="#0078D4"/>
  <rect x="28" y="40" width="16" height="4" rx="1" fill="#0078D4"/>
</svg>'''
        ))

        # Azure Functions
        self.register(IconInfo(
            id="azure/compute/functions",
            name="Azure Functions",
            provider=IconProvider.AZURE,
            category=IconCategory.SERVERLESS,
            keywords=["serverless", "function", "faas"],
            aliases=["azure-functions"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="azure-func-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#FFCA28"/>
      <stop offset="100%" style="stop-color:#FFA000"/>
    </linearGradient>
  </defs>
  <rect x="4" y="4" width="56" height="56" rx="4" fill="url(#azure-func-grad)"/>
  <path d="M20 48 L32 16 L36 16 L28 36 L40 36 L26 48 Z" fill="#FFFFFF"/>
</svg>'''
        ))

        # Blob Storage
        self.register(IconInfo(
            id="azure/storage/blob",
            name="Blob Storage",
            provider=IconProvider.AZURE,
            category=IconCategory.STORAGE,
            keywords=["object storage", "files", "container"],
            aliases=["azure-blob", "azure-storage"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="azure-blob-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0078D4"/>
      <stop offset="100%" style="stop-color:#005A9E"/>
    </linearGradient>
  </defs>
  <rect x="4" y="4" width="56" height="56" rx="4" fill="url(#azure-blob-grad)"/>
  <rect x="16" y="16" width="32" height="32" rx="4" fill="#FFFFFF"/>
  <rect x="22" y="22" width="20" height="6" rx="1" fill="#0078D4" opacity="0.7"/>
  <rect x="22" y="30" width="20" height="6" rx="1" fill="#0078D4" opacity="0.5"/>
  <rect x="22" y="38" width="20" height="6" rx="1" fill="#0078D4" opacity="0.3"/>
</svg>'''
        ))

        # Azure SQL
        self.register(IconInfo(
            id="azure/database/sql",
            name="Azure SQL Database",
            provider=IconProvider.AZURE,
            category=IconCategory.DATABASE,
            keywords=["sql server", "database", "relational"],
            aliases=["azure-sql", "azure-sqldb"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="azure-sql-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0078D4"/>
      <stop offset="100%" style="stop-color:#005A9E"/>
    </linearGradient>
  </defs>
  <rect x="4" y="4" width="56" height="56" rx="4" fill="url(#azure-sql-grad)"/>
  <ellipse cx="32" cy="18" rx="14" ry="6" fill="#FFFFFF"/>
  <rect x="18" y="18" width="28" height="28" fill="#FFFFFF"/>
  <ellipse cx="32" cy="46" rx="14" ry="6" fill="#FFFFFF"/>
  <ellipse cx="32" cy="28" rx="14" ry="6" fill="none" stroke="#0078D4" stroke-width="2"/>
  <ellipse cx="32" cy="38" rx="14" ry="6" fill="none" stroke="#0078D4" stroke-width="2"/>
</svg>'''
        ))

        # Cosmos DB
        self.register(IconInfo(
            id="azure/database/cosmosdb",
            name="Azure Cosmos DB",
            provider=IconProvider.AZURE,
            category=IconCategory.DATABASE,
            keywords=["nosql", "global", "multi-model"],
            aliases=["cosmosdb", "azure-cosmosdb"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="azure-cosmos-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0078D4"/>
      <stop offset="100%" style="stop-color:#005A9E"/>
    </linearGradient>
  </defs>
  <rect x="4" y="4" width="56" height="56" rx="4" fill="url(#azure-cosmos-grad)"/>
  <circle cx="32" cy="32" r="16" fill="none" stroke="#FFFFFF" stroke-width="2"/>
  <ellipse cx="32" cy="32" rx="16" ry="8" fill="none" stroke="#FFFFFF" stroke-width="2" transform="rotate(60 32 32)"/>
  <ellipse cx="32" cy="32" rx="16" ry="8" fill="none" stroke="#FFFFFF" stroke-width="2" transform="rotate(-60 32 32)"/>
  <circle cx="32" cy="32" r="4" fill="#FFFFFF"/>
</svg>'''
        ))

        # AKS
        self.register(IconInfo(
            id="azure/container/aks",
            name="Azure Kubernetes Service",
            provider=IconProvider.AZURE,
            category=IconCategory.CONTAINER,
            keywords=["kubernetes", "k8s", "container"],
            aliases=["aks", "azure-aks"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="azure-aks-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0078D4"/>
      <stop offset="100%" style="stop-color:#005A9E"/>
    </linearGradient>
  </defs>
  <rect x="4" y="4" width="56" height="56" rx="4" fill="url(#azure-aks-grad)"/>
  <path d="M32 12 L48 22 L48 42 L32 52 L16 42 L16 22 Z" fill="#FFFFFF"/>
  <circle cx="32" cy="32" r="6" fill="#0078D4"/>
  <circle cx="24" cy="22" r="3" fill="#0078D4"/>
  <circle cx="40" cy="22" r="3" fill="#0078D4"/>
  <circle cx="24" cy="42" r="3" fill="#0078D4"/>
  <circle cx="40" cy="42" r="3" fill="#0078D4"/>
</svg>'''
        ))

        # App Service
        self.register(IconInfo(
            id="azure/compute/appservice",
            name="App Service",
            provider=IconProvider.AZURE,
            category=IconCategory.COMPUTE,
            keywords=["web app", "paas", "hosting"],
            aliases=["azure-appservice", "azure-webapp"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="azure-app-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0078D4"/>
      <stop offset="100%" style="stop-color:#005A9E"/>
    </linearGradient>
  </defs>
  <rect x="4" y="4" width="56" height="56" rx="4" fill="url(#azure-app-grad)"/>
  <rect x="14" y="14" width="36" height="36" rx="4" fill="#FFFFFF"/>
  <path d="M20 32 L28 24 L28 40 Z" fill="#0078D4"/>
  <path d="M44 32 L36 24 L36 40 Z" fill="#0078D4"/>
</svg>'''
        ))

        # API Management
        self.register(IconInfo(
            id="azure/integration/apim",
            name="API Management",
            provider=IconProvider.AZURE,
            category=IconCategory.API,
            keywords=["api", "gateway", "management"],
            aliases=["azure-apim", "apim"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="azure-apim-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0078D4"/>
      <stop offset="100%" style="stop-color:#005A9E"/>
    </linearGradient>
  </defs>
  <rect x="4" y="4" width="56" height="56" rx="4" fill="url(#azure-apim-grad)"/>
  <rect x="26" y="12" width="12" height="40" rx="2" fill="#FFFFFF"/>
  <path d="M14 24 L26 32 L14 40" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>
  <path d="M50 24 L38 32 L50 40" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>
</svg>'''
        ))

        # Service Bus
        self.register(IconInfo(
            id="azure/integration/servicebus",
            name="Service Bus",
            provider=IconProvider.AZURE,
            category=IconCategory.MESSAGING,
            keywords=["queue", "topic", "messaging"],
            aliases=["azure-servicebus"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="azure-sb-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0078D4"/>
      <stop offset="100%" style="stop-color:#005A9E"/>
    </linearGradient>
  </defs>
  <rect x="4" y="4" width="56" height="56" rx="4" fill="url(#azure-sb-grad)"/>
  <rect x="12" y="20" width="40" height="24" rx="4" fill="#FFFFFF"/>
  <rect x="16" y="26" width="8" height="12" rx="1" fill="#0078D4"/>
  <rect x="28" y="26" width="8" height="12" rx="1" fill="#0078D4"/>
  <rect x="40" y="26" width="8" height="12" rx="1" fill="#0078D4"/>
</svg>'''
        ))

        # Azure Monitor
        self.register(IconInfo(
            id="azure/management/monitor",
            name="Azure Monitor",
            provider=IconProvider.AZURE,
            category=IconCategory.MONITORING,
            keywords=["monitoring", "metrics", "logs"],
            aliases=["azure-monitor"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="azure-mon-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0078D4"/>
      <stop offset="100%" style="stop-color:#005A9E"/>
    </linearGradient>
  </defs>
  <rect x="4" y="4" width="56" height="56" rx="4" fill="url(#azure-mon-grad)"/>
  <rect x="12" y="20" width="40" height="28" rx="2" fill="#FFFFFF"/>
  <path d="M18 40 L26 30 L34 36 L42 24 L50 28" fill="none" stroke="#0078D4" stroke-width="3" stroke-linecap="round"/>
</svg>'''
        ))

        # Load Balancer
        self.register(IconInfo(
            id="azure/network/lb",
            name="Load Balancer",
            provider=IconProvider.AZURE,
            category=IconCategory.LOAD_BALANCER,
            keywords=["lb", "traffic", "balancer"],
            aliases=["azure-lb"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="azure-lb-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0078D4"/>
      <stop offset="100%" style="stop-color:#005A9E"/>
    </linearGradient>
  </defs>
  <rect x="4" y="4" width="56" height="56" rx="4" fill="url(#azure-lb-grad)"/>
  <circle cx="20" cy="32" r="10" fill="#FFFFFF"/>
  <circle cx="44" cy="18" r="6" fill="#FFFFFF"/>
  <circle cx="44" cy="32" r="6" fill="#FFFFFF"/>
  <circle cx="44" cy="46" r="6" fill="#FFFFFF"/>
  <path d="M30 28 L38 18 M30 32 L38 32 M30 36 L38 46" stroke="#FFFFFF" stroke-width="2"/>
</svg>'''
        ))

        # VNet
        self.register(IconInfo(
            id="azure/network/vnet",
            name="Virtual Network",
            provider=IconProvider.AZURE,
            category=IconCategory.NETWORK,
            keywords=["vnet", "network", "subnet"],
            aliases=["azure-vnet"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="azure-vnet-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0078D4"/>
      <stop offset="100%" style="stop-color:#005A9E"/>
    </linearGradient>
  </defs>
  <rect x="4" y="4" width="56" height="56" rx="4" fill="url(#azure-vnet-grad)"/>
  <rect x="12" y="12" width="40" height="40" rx="4" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-dasharray="8,4"/>
  <rect x="20" y="20" width="24" height="24" rx="2" fill="#FFFFFF" opacity="0.3"/>
</svg>'''
        ))

    # =========================================================================
    # Kubernetes Icons
    # =========================================================================
    def _register_k8s_icons(self):
        """Register Kubernetes/CNCF Icons"""

        # Pod
        self.register(IconInfo(
            id="k8s/workload/pod",
            name="Pod",
            provider=IconProvider.KUBERNETES,
            category=IconCategory.POD,
            keywords=["container", "workload"],
            aliases=["pod", "k8s-pod"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="4" width="56" height="56" rx="4" fill="#326CE5"/>
  <rect x="14" y="14" width="36" height="36" rx="4" fill="#FFFFFF"/>
  <rect x="20" y="20" width="24" height="24" rx="2" fill="#326CE5"/>
</svg>'''
        ))

        # Deployment
        self.register(IconInfo(
            id="k8s/workload/deployment",
            name="Deployment",
            provider=IconProvider.KUBERNETES,
            category=IconCategory.DEPLOYMENT,
            keywords=["replicas", "rollout"],
            aliases=["deployment", "k8s-deployment", "deploy"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="4" width="56" height="56" rx="4" fill="#326CE5"/>
  <rect x="10" y="14" width="18" height="18" rx="2" fill="#FFFFFF"/>
  <rect x="36" y="14" width="18" height="18" rx="2" fill="#FFFFFF"/>
  <rect x="10" y="36" width="18" height="18" rx="2" fill="#FFFFFF"/>
  <rect x="36" y="36" width="18" height="18" rx="2" fill="#FFFFFF"/>
  <circle cx="19" cy="23" r="4" fill="#326CE5"/>
  <circle cx="45" cy="23" r="4" fill="#326CE5"/>
  <circle cx="19" cy="45" r="4" fill="#326CE5"/>
  <circle cx="45" cy="45" r="4" fill="#326CE5"/>
</svg>'''
        ))

        # Service
        self.register(IconInfo(
            id="k8s/network/service",
            name="Service",
            provider=IconProvider.KUBERNETES,
            category=IconCategory.SERVICE,
            keywords=["clusterip", "nodeport", "loadbalancer"],
            aliases=["service", "k8s-service", "svc"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="4" width="56" height="56" rx="4" fill="#326CE5"/>
  <circle cx="32" cy="32" r="18" fill="#FFFFFF"/>
  <circle cx="32" cy="32" r="10" fill="none" stroke="#326CE5" stroke-width="3"/>
  <circle cx="32" cy="32" r="4" fill="#326CE5"/>
</svg>'''
        ))

        # Ingress
        self.register(IconInfo(
            id="k8s/network/ingress",
            name="Ingress",
            provider=IconProvider.KUBERNETES,
            category=IconCategory.INGRESS,
            keywords=["http", "routing", "gateway"],
            aliases=["ingress", "k8s-ingress"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="4" width="56" height="56" rx="4" fill="#326CE5"/>
  <path d="M12 32 L32 12 L52 32 L32 52 Z" fill="#FFFFFF"/>
  <path d="M32 12 L32 32 L12 32" fill="none" stroke="#326CE5" stroke-width="2"/>
  <circle cx="32" cy="32" r="6" fill="#326CE5"/>
</svg>'''
        ))

        # ConfigMap
        self.register(IconInfo(
            id="k8s/config/configmap",
            name="ConfigMap",
            provider=IconProvider.KUBERNETES,
            category=IconCategory.CONFIGMAP,
            keywords=["config", "environment", "settings"],
            aliases=["configmap", "k8s-configmap", "cm"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="4" width="56" height="56" rx="4" fill="#7B61FF"/>
  <rect x="14" y="14" width="36" height="36" rx="2" fill="#FFFFFF"/>
  <rect x="20" y="22" width="24" height="4" rx="1" fill="#7B61FF"/>
  <rect x="20" y="30" width="18" height="4" rx="1" fill="#7B61FF"/>
  <rect x="20" y="38" width="20" height="4" rx="1" fill="#7B61FF"/>
</svg>'''
        ))

        # Secret
        self.register(IconInfo(
            id="k8s/config/secret",
            name="Secret",
            provider=IconProvider.KUBERNETES,
            category=IconCategory.SECRET,
            keywords=["credentials", "password", "token"],
            aliases=["secret", "k8s-secret"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="4" width="56" height="56" rx="4" fill="#F5A623"/>
  <path d="M32 14 L32 26 M24 26 L40 26 L40 42 L32 50 L24 42 L24 26" fill="#FFFFFF"/>
  <circle cx="32" cy="36" r="4" fill="#F5A623"/>
</svg>'''
        ))

        # PersistentVolume
        self.register(IconInfo(
            id="k8s/storage/pv",
            name="PersistentVolume",
            provider=IconProvider.KUBERNETES,
            category=IconCategory.VOLUME,
            keywords=["storage", "disk", "persistent"],
            aliases=["pv", "k8s-pv", "persistentvolume"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="4" width="56" height="56" rx="4" fill="#0DB7ED"/>
  <ellipse cx="32" cy="18" rx="16" ry="6" fill="#FFFFFF"/>
  <rect x="16" y="18" width="32" height="28" fill="#FFFFFF"/>
  <ellipse cx="32" cy="46" rx="16" ry="6" fill="#FFFFFF"/>
  <ellipse cx="32" cy="32" rx="16" ry="6" fill="none" stroke="#0DB7ED" stroke-width="2"/>
</svg>'''
        ))

        # Namespace
        self.register(IconInfo(
            id="k8s/cluster/namespace",
            name="Namespace",
            provider=IconProvider.KUBERNETES,
            category=IconCategory.NETWORK,
            keywords=["isolation", "scope", "project"],
            aliases=["namespace", "k8s-namespace", "ns"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="4" width="56" height="56" rx="4" fill="#326CE5"/>
  <rect x="10" y="10" width="44" height="44" rx="4" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-dasharray="8,4"/>
  <text x="32" y="38" fill="#FFFFFF" font-size="12" text-anchor="middle" font-family="Arial">NS</text>
</svg>'''
        ))

        # Node
        self.register(IconInfo(
            id="k8s/cluster/node",
            name="Node",
            provider=IconProvider.KUBERNETES,
            category=IconCategory.COMPUTE,
            keywords=["worker", "master", "server"],
            aliases=["node", "k8s-node"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="4" width="56" height="56" rx="4" fill="#326CE5"/>
  <rect x="12" y="16" width="40" height="32" rx="2" fill="#FFFFFF"/>
  <rect x="16" y="20" width="32" height="20" rx="1" fill="#326CE5" opacity="0.3"/>
  <circle cx="20" cy="44" r="2" fill="#326CE5"/>
  <circle cx="28" cy="44" r="2" fill="#326CE5"/>
  <rect x="34" y="42" width="14" height="4" rx="1" fill="#326CE5"/>
</svg>'''
        ))

        # Helm
        self.register(IconInfo(
            id="k8s/tools/helm",
            name="Helm",
            provider=IconProvider.KUBERNETES,
            category=IconCategory.DEVOPS,
            keywords=["chart", "package", "release"],
            aliases=["helm"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="4" width="56" height="56" rx="4" fill="#0F1689"/>
  <circle cx="32" cy="32" r="18" fill="none" stroke="#FFFFFF" stroke-width="4"/>
  <path d="M32 14 L32 22 M32 42 L32 50 M14 32 L22 32 M42 32 L50 32" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
  <path d="M20 20 L26 26 M38 38 L44 44 M20 44 L26 38 M38 26 L44 20" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>
</svg>'''
        ))

    # =========================================================================
    # Generic Icons
    # =========================================================================
    def _register_generic_icons(self):
        """Register generic technology icons"""

        # User/Client
        self.register(IconInfo(
            id="generic/user/client",
            name="Client",
            provider=IconProvider.GENERIC,
            category=IconCategory.CLIENT,
            keywords=["user", "browser", "frontend"],
            aliases=["client", "user", "browser"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="4" width="56" height="56" rx="4" fill="#607D8B"/>
  <circle cx="32" cy="24" r="10" fill="#FFFFFF"/>
  <path d="M16 52 C16 40 48 40 48 52" fill="#FFFFFF"/>
</svg>'''
        ))

        # Database (generic)
        self.register(IconInfo(
            id="generic/database/db",
            name="Database",
            provider=IconProvider.GENERIC,
            category=IconCategory.DATABASE,
            keywords=["sql", "data", "storage"],
            aliases=["db", "database"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="4" width="56" height="56" rx="4" fill="#2E7D32"/>
  <ellipse cx="32" cy="18" rx="16" ry="8" fill="#FFFFFF"/>
  <rect x="16" y="18" width="32" height="28" fill="#FFFFFF"/>
  <ellipse cx="32" cy="46" rx="16" ry="8" fill="#FFFFFF"/>
  <ellipse cx="32" cy="28" rx="16" ry="6" fill="none" stroke="#2E7D32" stroke-width="2"/>
  <ellipse cx="32" cy="38" rx="16" ry="6" fill="none" stroke="#2E7D32" stroke-width="2"/>
</svg>'''
        ))

        # Server
        self.register(IconInfo(
            id="generic/compute/server",
            name="Server",
            provider=IconProvider.GENERIC,
            category=IconCategory.COMPUTE,
            keywords=["host", "machine", "backend"],
            aliases=["server"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="4" width="56" height="56" rx="4" fill="#455A64"/>
  <rect x="12" y="12" width="40" height="16" rx="2" fill="#FFFFFF"/>
  <rect x="12" y="32" width="40" height="16" rx="2" fill="#FFFFFF"/>
  <circle cx="20" cy="20" r="3" fill="#4CAF50"/>
  <circle cx="20" cy="40" r="3" fill="#4CAF50"/>
  <rect x="28" y="18" width="20" height="4" rx="1" fill="#455A64"/>
  <rect x="28" y="38" width="20" height="4" rx="1" fill="#455A64"/>
</svg>'''
        ))

        # API
        self.register(IconInfo(
            id="generic/integration/api",
            name="API",
            provider=IconProvider.GENERIC,
            category=IconCategory.API,
            keywords=["rest", "http", "endpoint"],
            aliases=["api"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="4" width="56" height="56" rx="4" fill="#7B1FA2"/>
  <rect x="26" y="12" width="12" height="40" rx="2" fill="#FFFFFF"/>
  <path d="M14 24 L26 32 L14 40" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>
  <path d="M50 24 L38 32 L50 40" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>
</svg>'''
        ))

        # Message Queue
        self.register(IconInfo(
            id="generic/integration/queue",
            name="Message Queue",
            provider=IconProvider.GENERIC,
            category=IconCategory.QUEUE,
            keywords=["mq", "rabbitmq", "kafka"],
            aliases=["queue", "mq"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="4" width="56" height="56" rx="4" fill="#FF5722"/>
  <rect x="12" y="20" width="40" height="24" rx="4" fill="#FFFFFF"/>
  <rect x="16" y="26" width="8" height="12" rx="1" fill="#FF5722"/>
  <rect x="28" y="26" width="8" height="12" rx="1" fill="#FF5722"/>
  <rect x="40" y="26" width="8" height="12" rx="1" fill="#FF5722"/>
</svg>'''
        ))

        # Cache
        self.register(IconInfo(
            id="generic/database/cache",
            name="Cache",
            provider=IconProvider.GENERIC,
            category=IconCategory.CACHE,
            keywords=["redis", "memcached", "memory"],
            aliases=["cache", "redis"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="4" width="56" height="56" rx="4" fill="#D32F2F"/>
  <path d="M32 12 L48 22 L48 42 L32 52 L16 42 L16 22 Z" fill="#FFFFFF"/>
  <path d="M32 12 L32 32 L16 22" fill="none" stroke="#D32F2F" stroke-width="2"/>
  <path d="M32 32 L48 22" fill="none" stroke="#D32F2F" stroke-width="2"/>
  <path d="M32 32 L32 52" fill="none" stroke="#D32F2F" stroke-width="2"/>
</svg>'''
        ))

        # CDN
        self.register(IconInfo(
            id="generic/network/cdn",
            name="CDN",
            provider=IconProvider.GENERIC,
            category=IconCategory.CDN,
            keywords=["edge", "distribution", "cache"],
            aliases=["cdn"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="4" width="56" height="56" rx="4" fill="#9C27B0"/>
  <circle cx="32" cy="32" r="16" fill="none" stroke="#FFFFFF" stroke-width="3"/>
  <circle cx="32" cy="32" r="8" fill="#FFFFFF"/>
  <circle cx="32" cy="12" r="4" fill="#FFFFFF"/>
  <circle cx="32" cy="52" r="4" fill="#FFFFFF"/>
  <circle cx="12" cy="32" r="4" fill="#FFFFFF"/>
  <circle cx="52" cy="32" r="4" fill="#FFFFFF"/>
</svg>'''
        ))

        # Load Balancer
        self.register(IconInfo(
            id="generic/network/lb",
            name="Load Balancer",
            provider=IconProvider.GENERIC,
            category=IconCategory.LOAD_BALANCER,
            keywords=["traffic", "distribution", "balancer"],
            aliases=["lb", "loadbalancer"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="4" width="56" height="56" rx="4" fill="#5E35B1"/>
  <circle cx="20" cy="32" r="10" fill="#FFFFFF"/>
  <circle cx="44" cy="18" r="6" fill="#FFFFFF"/>
  <circle cx="44" cy="32" r="6" fill="#FFFFFF"/>
  <circle cx="44" cy="46" r="6" fill="#FFFFFF"/>
  <path d="M30 28 L38 18 M30 32 L38 32 M30 36 L38 46" stroke="#FFFFFF" stroke-width="2"/>
</svg>'''
        ))

        # Firewall
        self.register(IconInfo(
            id="generic/security/firewall",
            name="Firewall",
            provider=IconProvider.GENERIC,
            category=IconCategory.FIREWALL,
            keywords=["security", "waf", "protection"],
            aliases=["firewall", "waf"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="4" width="56" height="56" rx="4" fill="#D32F2F"/>
  <rect x="12" y="16" width="40" height="32" rx="2" fill="#FFFFFF"/>
  <rect x="16" y="20" width="4" height="24" fill="#D32F2F"/>
  <rect x="24" y="20" width="4" height="24" fill="#D32F2F"/>
  <rect x="32" y="20" width="4" height="24" fill="#D32F2F"/>
  <rect x="40" y="20" width="4" height="24" fill="#D32F2F"/>
</svg>'''
        ))

        # Cloud (generic)
        self.register(IconInfo(
            id="generic/infra/cloud",
            name="Cloud",
            provider=IconProvider.GENERIC,
            category=IconCategory.COMPUTE,
            keywords=["cloud", "provider", "infrastructure"],
            aliases=["cloud"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="4" width="56" height="56" rx="4" fill="#2196F3"/>
  <path d="M16 40 C8 40 8 28 18 26 C18 18 28 14 36 18 C42 14 54 16 54 28 C62 28 62 40 54 40 Z" fill="#FFFFFF"/>
</svg>'''
        ))

        # Internet
        self.register(IconInfo(
            id="generic/network/internet",
            name="Internet",
            provider=IconProvider.GENERIC,
            category=IconCategory.NETWORK,
            keywords=["web", "www", "global"],
            aliases=["internet", "web"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="4" width="56" height="56" rx="4" fill="#00BCD4"/>
  <circle cx="32" cy="32" r="18" fill="none" stroke="#FFFFFF" stroke-width="2"/>
  <ellipse cx="32" cy="32" rx="8" ry="18" fill="none" stroke="#FFFFFF" stroke-width="2"/>
  <path d="M14 32 L50 32 M32 14 L32 50" stroke="#FFFFFF" stroke-width="2"/>
</svg>'''
        ))

        # Mobile
        self.register(IconInfo(
            id="generic/user/mobile",
            name="Mobile",
            provider=IconProvider.GENERIC,
            category=IconCategory.MOBILE,
            keywords=["phone", "app", "ios", "android"],
            aliases=["mobile", "phone"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="4" width="56" height="56" rx="4" fill="#78909C"/>
  <rect x="20" y="10" width="24" height="44" rx="4" fill="#FFFFFF"/>
  <rect x="24" y="16" width="16" height="28" rx="1" fill="#78909C" opacity="0.3"/>
  <circle cx="32" cy="50" r="3" fill="#78909C"/>
</svg>'''
        ))

        # Monitoring
        self.register(IconInfo(
            id="generic/devops/monitoring",
            name="Monitoring",
            provider=IconProvider.GENERIC,
            category=IconCategory.MONITORING,
            keywords=["metrics", "dashboard", "grafana"],
            aliases=["monitoring", "metrics"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="4" width="56" height="56" rx="4" fill="#FF5722"/>
  <rect x="12" y="16" width="40" height="32" rx="2" fill="#FFFFFF"/>
  <path d="M18 40 L26 30 L34 36 L42 24 L50 28" fill="none" stroke="#FF5722" stroke-width="3" stroke-linecap="round"/>
</svg>'''
        ))

        # CI/CD
        self.register(IconInfo(
            id="generic/devops/cicd",
            name="CI/CD",
            provider=IconProvider.GENERIC,
            category=IconCategory.CI_CD,
            keywords=["pipeline", "jenkins", "github actions"],
            aliases=["cicd", "pipeline"],
            svg_content='''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="4" width="56" height="56" rx="4" fill="#3F51B5"/>
  <circle cx="18" cy="32" r="8" fill="#FFFFFF"/>
  <circle cx="46" cy="32" r="8" fill="#FFFFFF"/>
  <path d="M26 32 L38 32" stroke="#FFFFFF" stroke-width="4"/>
  <path d="M34 26 L40 32 L34 38" fill="none" stroke="#FFFFFF" stroke-width="3"/>
</svg>'''
        ))


# Global registry instance
_registry: Optional[IconRegistry] = None


def get_icon_registry() -> IconRegistry:
    """Get the global icon registry instance"""
    global _registry
    if _registry is None:
        _registry = IconRegistry()
    return _registry


def get_icon(icon_id: str) -> Optional[IconInfo]:
    """Get an icon by ID"""
    return get_icon_registry().get(icon_id)


def list_icons(provider: Optional[IconProvider] = None, category: Optional[IconCategory] = None) -> List[str]:
    """List icon IDs, optionally filtered"""
    registry = get_icon_registry()
    if provider:
        return registry.list_by_provider(provider)
    if category:
        return registry.list_by_category(category)
    return registry.list_all()


def list_categories() -> List[IconCategory]:
    """List all icon categories"""
    return list(IconCategory)
