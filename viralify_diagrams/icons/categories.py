"""
Icon Categories and Providers

Defines the taxonomy for organizing cloud and technology icons.
"""

from enum import Enum
from typing import Dict


class IconProvider(str, Enum):
    """Cloud providers and icon sources"""
    AWS = "aws"
    GCP = "gcp"
    AZURE = "azure"
    KUBERNETES = "k8s"
    GENERIC = "generic"
    ONPREM = "onprem"
    SAAS = "saas"
    PROGRAMMING = "programming"


class IconCategory(str, Enum):
    """Functional categories for icons"""
    # Compute
    COMPUTE = "compute"
    CONTAINER = "container"
    SERVERLESS = "serverless"

    # Storage
    STORAGE = "storage"
    DATABASE = "database"
    CACHE = "cache"

    # Network
    NETWORK = "network"
    CDN = "cdn"
    DNS = "dns"
    LOAD_BALANCER = "load_balancer"
    VPN = "vpn"
    FIREWALL = "firewall"

    # Security
    SECURITY = "security"
    IAM = "iam"
    ENCRYPTION = "encryption"

    # Integration
    INTEGRATION = "integration"
    MESSAGING = "messaging"
    API = "api"
    QUEUE = "queue"
    EVENT = "event"

    # Analytics
    ANALYTICS = "analytics"
    ML = "ml"
    AI = "ai"
    DATA = "data"

    # DevOps
    DEVOPS = "devops"
    CI_CD = "ci_cd"
    MONITORING = "monitoring"
    LOGGING = "logging"

    # General
    USER = "user"
    CLIENT = "client"
    MOBILE = "mobile"
    WEB = "web"
    IOT = "iot"

    # Kubernetes specific
    POD = "pod"
    SERVICE = "service"
    DEPLOYMENT = "deployment"
    INGRESS = "ingress"
    CONFIGMAP = "configmap"
    SECRET = "secret"
    VOLUME = "volume"


# Color palette for categories (for automatic node coloring)
CATEGORY_COLORS: Dict[IconCategory, Dict[str, str]] = {
    # Compute - Orange/Red
    IconCategory.COMPUTE: {"fill": "#FF9900", "stroke": "#CC7A00", "text": "#FFFFFF"},
    IconCategory.CONTAINER: {"fill": "#FF6B35", "stroke": "#CC5529", "text": "#FFFFFF"},
    IconCategory.SERVERLESS: {"fill": "#FF4F00", "stroke": "#CC3F00", "text": "#FFFFFF"},

    # Storage - Green
    IconCategory.STORAGE: {"fill": "#3ECF8E", "stroke": "#2DA66E", "text": "#FFFFFF"},
    IconCategory.DATABASE: {"fill": "#2E7D32", "stroke": "#1B5E20", "text": "#FFFFFF"},
    IconCategory.CACHE: {"fill": "#4CAF50", "stroke": "#388E3C", "text": "#FFFFFF"},

    # Network - Purple/Blue
    IconCategory.NETWORK: {"fill": "#7B1FA2", "stroke": "#6A1B9A", "text": "#FFFFFF"},
    IconCategory.CDN: {"fill": "#9C27B0", "stroke": "#7B1FA2", "text": "#FFFFFF"},
    IconCategory.DNS: {"fill": "#AB47BC", "stroke": "#8E24AA", "text": "#FFFFFF"},
    IconCategory.LOAD_BALANCER: {"fill": "#5E35B1", "stroke": "#4527A0", "text": "#FFFFFF"},
    IconCategory.VPN: {"fill": "#673AB7", "stroke": "#512DA8", "text": "#FFFFFF"},
    IconCategory.FIREWALL: {"fill": "#D32F2F", "stroke": "#C62828", "text": "#FFFFFF"},

    # Security - Red
    IconCategory.SECURITY: {"fill": "#F44336", "stroke": "#D32F2F", "text": "#FFFFFF"},
    IconCategory.IAM: {"fill": "#E53935", "stroke": "#C62828", "text": "#FFFFFF"},
    IconCategory.ENCRYPTION: {"fill": "#EF5350", "stroke": "#E53935", "text": "#FFFFFF"},

    # Integration - Blue
    IconCategory.INTEGRATION: {"fill": "#2196F3", "stroke": "#1976D2", "text": "#FFFFFF"},
    IconCategory.MESSAGING: {"fill": "#1E88E5", "stroke": "#1565C0", "text": "#FFFFFF"},
    IconCategory.API: {"fill": "#42A5F5", "stroke": "#1E88E5", "text": "#FFFFFF"},
    IconCategory.QUEUE: {"fill": "#64B5F6", "stroke": "#42A5F5", "text": "#FFFFFF"},
    IconCategory.EVENT: {"fill": "#FF5722", "stroke": "#E64A19", "text": "#FFFFFF"},

    # Analytics - Teal
    IconCategory.ANALYTICS: {"fill": "#00796B", "stroke": "#00695C", "text": "#FFFFFF"},
    IconCategory.ML: {"fill": "#00897B", "stroke": "#00796B", "text": "#FFFFFF"},
    IconCategory.AI: {"fill": "#009688", "stroke": "#00897B", "text": "#FFFFFF"},
    IconCategory.DATA: {"fill": "#26A69A", "stroke": "#00897B", "text": "#FFFFFF"},

    # DevOps - Indigo
    IconCategory.DEVOPS: {"fill": "#3F51B5", "stroke": "#303F9F", "text": "#FFFFFF"},
    IconCategory.CI_CD: {"fill": "#5C6BC0", "stroke": "#3F51B5", "text": "#FFFFFF"},
    IconCategory.MONITORING: {"fill": "#7986CB", "stroke": "#5C6BC0", "text": "#FFFFFF"},
    IconCategory.LOGGING: {"fill": "#9FA8DA", "stroke": "#7986CB", "text": "#1a1a2e"},

    # User/Client - Grey
    IconCategory.USER: {"fill": "#607D8B", "stroke": "#455A64", "text": "#FFFFFF"},
    IconCategory.CLIENT: {"fill": "#78909C", "stroke": "#607D8B", "text": "#FFFFFF"},
    IconCategory.MOBILE: {"fill": "#90A4AE", "stroke": "#78909C", "text": "#1a1a2e"},
    IconCategory.WEB: {"fill": "#B0BEC5", "stroke": "#90A4AE", "text": "#1a1a2e"},
    IconCategory.IOT: {"fill": "#00BCD4", "stroke": "#0097A7", "text": "#FFFFFF"},

    # Kubernetes - Blue
    IconCategory.POD: {"fill": "#326CE5", "stroke": "#2558C7", "text": "#FFFFFF"},
    IconCategory.SERVICE: {"fill": "#326CE5", "stroke": "#2558C7", "text": "#FFFFFF"},
    IconCategory.DEPLOYMENT: {"fill": "#326CE5", "stroke": "#2558C7", "text": "#FFFFFF"},
    IconCategory.INGRESS: {"fill": "#326CE5", "stroke": "#2558C7", "text": "#FFFFFF"},
    IconCategory.CONFIGMAP: {"fill": "#7B61FF", "stroke": "#6B51EF", "text": "#FFFFFF"},
    IconCategory.SECRET: {"fill": "#F5A623", "stroke": "#D4920F", "text": "#1a1a2e"},
    IconCategory.VOLUME: {"fill": "#0DB7ED", "stroke": "#0A9FCC", "text": "#FFFFFF"},
}


# Provider brand colors
PROVIDER_COLORS: Dict[IconProvider, Dict[str, str]] = {
    IconProvider.AWS: {
        "primary": "#FF9900",
        "secondary": "#232F3E",
        "accent": "#FF9900",
    },
    IconProvider.GCP: {
        "primary": "#4285F4",
        "secondary": "#EA4335",
        "accent": "#34A853",
    },
    IconProvider.AZURE: {
        "primary": "#0078D4",
        "secondary": "#50E6FF",
        "accent": "#00BCF2",
    },
    IconProvider.KUBERNETES: {
        "primary": "#326CE5",
        "secondary": "#FFFFFF",
        "accent": "#326CE5",
    },
    IconProvider.GENERIC: {
        "primary": "#6B7280",
        "secondary": "#374151",
        "accent": "#9CA3AF",
    },
}
