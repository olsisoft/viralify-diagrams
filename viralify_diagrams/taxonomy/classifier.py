"""
Request Classifier for Diagram Taxonomy

Intelligent classification of natural language requests to determine:
- Diagram domain (architecture, development, data, etc.)
- Diagram category (C4, UML, DFD, etc.)
- Specific diagram type (c4_context, uml_sequence, etc.)
- Complexity level
- Target audience

Uses a hybrid approach:
1. Keyword matching for explicit mentions
2. Semantic analysis for implicit context
3. Rule-based inference for ambiguous cases
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set, Tuple
import re
from collections import Counter

from viralify_diagrams.taxonomy.categories import (
    DiagramDomain,
    DiagramCategory,
    DiagramType,
    ComplexityLevel,
    AudienceType,
    DIAGRAM_KEYWORDS,
    DOMAIN_CATEGORIES,
    CATEGORY_TYPES,
    get_domain_for_category,
    get_category_for_type,
)


@dataclass
class ClassificationResult:
    """Result of request classification"""
    # Primary classification
    domain: DiagramDomain
    category: DiagramCategory
    diagram_type: DiagramType

    # Confidence scores (0.0 - 1.0)
    domain_confidence: float
    category_confidence: float
    type_confidence: float

    # Additional analysis
    complexity: ComplexityLevel
    audience: AudienceType

    # Detected elements
    detected_keywords: List[str] = field(default_factory=list)
    detected_entities: List[str] = field(default_factory=list)
    estimated_elements: int = 5

    # Alternative suggestions
    alternative_types: List[Tuple[DiagramType, float]] = field(default_factory=list)

    # Metadata
    requires_clarification: bool = False
    clarification_questions: List[str] = field(default_factory=list)

    @property
    def overall_confidence(self) -> float:
        """Combined confidence score"""
        return (self.domain_confidence + self.category_confidence + self.type_confidence) / 3

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "domain": self.domain.value,
            "category": self.category.value,
            "diagram_type": self.diagram_type.value,
            "confidence": {
                "domain": self.domain_confidence,
                "category": self.category_confidence,
                "type": self.type_confidence,
                "overall": self.overall_confidence,
            },
            "complexity": self.complexity.value,
            "audience": self.audience.value,
            "estimated_elements": self.estimated_elements,
            "detected_keywords": self.detected_keywords,
            "alternatives": [
                {"type": t.value, "confidence": c}
                for t, c in self.alternative_types
            ],
            "requires_clarification": self.requires_clarification,
        }


class RequestClassifier:
    """
    Intelligent request classifier for diagram generation.

    Analyzes natural language requests to determine the appropriate
    diagram type, complexity, and target audience.

    Example:
        >>> classifier = RequestClassifier()
        >>> result = classifier.classify(
        ...     "Create a C4 container diagram for our e-commerce platform"
        ... )
        >>> print(result.diagram_type)  # DiagramType.C4_CONTAINER
    """

    def __init__(self):
        # Compile regex patterns for better performance
        self._compile_patterns()

        # Audience keywords
        self._audience_keywords = {
            AudienceType.EXECUTIVE: {"executive", "c-level", "ceo", "cto", "board", "stakeholder", "business"},
            AudienceType.MANAGER: {"manager", "lead", "pm", "project manager", "team lead"},
            AudienceType.ARCHITECT: {"architect", "solution architect", "enterprise architect", "technical architect"},
            AudienceType.DEVELOPER: {"developer", "engineer", "programmer", "dev", "coding"},
            AudienceType.DEVOPS: {"devops", "sre", "ops", "infrastructure", "platform"},
            AudienceType.DATA_ENGINEER: {"data engineer", "data analyst", "analytics", "data scientist"},
            AudienceType.SECURITY: {"security", "infosec", "cybersecurity", "ciso", "security engineer"},
            AudienceType.BUSINESS: {"business analyst", "ba", "requirements", "stakeholder"},
        }

        # Complexity indicators
        self._complexity_indicators = {
            ComplexityLevel.SIMPLE: {"simple", "basic", "overview", "high-level", "introduction", "beginner"},
            ComplexityLevel.MODERATE: {"moderate", "standard", "typical", "normal"},
            ComplexityLevel.COMPLEX: {"complex", "detailed", "comprehensive", "in-depth", "advanced"},
            ComplexityLevel.ENTERPRISE: {"enterprise", "production", "full", "complete", "all", "entire"},
        }

    def _compile_patterns(self):
        """Compile regex patterns for keyword matching"""
        self._patterns = {}

        for diagram_type, keywords in DIAGRAM_KEYWORDS.items():
            # Create pattern that matches any keyword (case insensitive)
            pattern = r'\b(' + '|'.join(re.escape(kw) for kw in keywords) + r')\b'
            self._patterns[diagram_type] = re.compile(pattern, re.IGNORECASE)

    def classify(
        self,
        request: str,
        context: Optional[Dict] = None
    ) -> ClassificationResult:
        """
        Classify a natural language request.

        Args:
            request: The user's request text
            context: Optional additional context (previous diagrams, project info, etc.)

        Returns:
            ClassificationResult with detected diagram type and metadata
        """
        request_lower = request.lower()

        # Step 1: Extract explicit keywords
        keyword_matches = self._extract_keywords(request_lower)

        # Step 2: Score diagram types based on keyword matches
        type_scores = self._score_diagram_types(request_lower, keyword_matches)

        # Step 3: Determine best match
        if type_scores:
            best_type, best_score = max(type_scores.items(), key=lambda x: x[1])
        else:
            # Fallback to generic block diagram
            best_type = DiagramType.BLOCK_DIAGRAM
            best_score = 0.3

        # Step 4: Get category and domain
        category = get_category_for_type(best_type)
        domain = get_domain_for_category(category)

        # Step 5: Detect complexity and audience
        complexity = self._detect_complexity(request_lower)
        audience = self._detect_audience(request_lower)

        # Step 6: Estimate number of elements
        estimated_elements = self._estimate_elements(request_lower, best_type)

        # Step 7: Extract entities (nouns that might be diagram elements)
        entities = self._extract_entities(request)

        # Step 8: Generate alternatives
        alternatives = self._get_alternatives(type_scores, best_type)

        # Step 9: Check if clarification is needed
        requires_clarification = best_score < 0.5
        clarification_questions = []
        if requires_clarification:
            clarification_questions = self._generate_clarification_questions(
                request, type_scores, domain
            )

        return ClassificationResult(
            domain=domain,
            category=category,
            diagram_type=best_type,
            domain_confidence=self._calculate_domain_confidence(type_scores, domain),
            category_confidence=self._calculate_category_confidence(type_scores, category),
            type_confidence=min(best_score, 1.0),
            complexity=complexity,
            audience=audience,
            detected_keywords=list(keyword_matches),
            detected_entities=entities,
            estimated_elements=estimated_elements,
            alternative_types=alternatives,
            requires_clarification=requires_clarification,
            clarification_questions=clarification_questions,
        )

    def _extract_keywords(self, text: str) -> Set[str]:
        """Extract matching keywords from text"""
        matches = set()

        for diagram_type, pattern in self._patterns.items():
            found = pattern.findall(text)
            matches.update(kw.lower() for kw in found)

        return matches

    def _score_diagram_types(
        self,
        text: str,
        keyword_matches: Set[str]
    ) -> Dict[DiagramType, float]:
        """Score each diagram type based on text analysis"""
        scores: Dict[DiagramType, float] = {}

        for diagram_type, keywords in DIAGRAM_KEYWORDS.items():
            score = 0.0
            matched_keywords = 0

            for keyword in keywords:
                if keyword.lower() in text:
                    # Weight by keyword specificity (longer = more specific)
                    weight = min(len(keyword.split()) * 0.3, 1.0)
                    score += weight
                    matched_keywords += 1

            if matched_keywords > 0:
                # Normalize and cap at 1.0
                normalized_score = min(score / len(keywords) * 2, 1.0)

                # Boost for multiple keyword matches
                if matched_keywords > 1:
                    normalized_score = min(normalized_score * 1.2, 1.0)

                scores[diagram_type] = normalized_score

        return scores

    def _detect_complexity(self, text: str) -> ComplexityLevel:
        """Detect requested complexity level"""
        for level, keywords in self._complexity_indicators.items():
            for keyword in keywords:
                if keyword in text:
                    return level

        # Infer from element count indicators
        if any(word in text for word in ["all", "complete", "full", "entire"]):
            return ComplexityLevel.ENTERPRISE
        elif any(word in text for word in ["detailed", "comprehensive"]):
            return ComplexityLevel.COMPLEX
        elif any(word in text for word in ["simple", "basic", "overview"]):
            return ComplexityLevel.SIMPLE

        return ComplexityLevel.MODERATE

    def _detect_audience(self, text: str) -> AudienceType:
        """Detect target audience"""
        for audience, keywords in self._audience_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    return audience

        return AudienceType.GENERAL

    def _estimate_elements(self, text: str, diagram_type: DiagramType) -> int:
        """Estimate number of elements in the diagram"""
        # Look for explicit numbers
        numbers = re.findall(r'\b(\d+)\s*(?:components?|services?|elements?|nodes?|entities?)', text)
        if numbers:
            return int(numbers[0])

        # Count named entities or list items
        list_items = re.findall(r'(?:^|\n)\s*[-•*]\s*\w+', text)
        if list_items:
            return len(list_items)

        # Default based on complexity and type
        from viralify_diagrams.taxonomy.categories import DIAGRAM_MAX_ELEMENTS
        default_max = DIAGRAM_MAX_ELEMENTS.get(diagram_type, 8)

        return min(default_max, 8)

    def _extract_entities(self, text: str) -> List[str]:
        """Extract potential diagram elements from text"""
        entities = []

        # Extract quoted strings
        quoted = re.findall(r'"([^"]+)"', text)
        entities.extend(quoted)

        # Extract capitalized words (potential system/service names)
        capitalized = re.findall(r'\b([A-Z][a-z]+(?:[A-Z][a-z]+)*)\b', text)
        entities.extend(cap for cap in capitalized if len(cap) > 2)

        # Extract technical terms (CamelCase, snake_case)
        technical = re.findall(r'\b([a-z]+_[a-z_]+|[A-Z][a-z]+[A-Z][a-zA-Z]*)\b', text)
        entities.extend(technical)

        # Remove duplicates and common words
        common_words = {"the", "and", "for", "with", "from", "into", "that", "this", "create", "show", "diagram"}
        entities = list(set(e for e in entities if e.lower() not in common_words))

        return entities[:20]  # Limit to 20 entities

    def _get_alternatives(
        self,
        scores: Dict[DiagramType, float],
        best_type: DiagramType
    ) -> List[Tuple[DiagramType, float]]:
        """Get alternative diagram types sorted by score"""
        alternatives = [
            (dtype, score)
            for dtype, score in scores.items()
            if dtype != best_type and score > 0.2
        ]
        alternatives.sort(key=lambda x: x[1], reverse=True)
        return alternatives[:5]  # Top 5 alternatives

    def _calculate_domain_confidence(
        self,
        type_scores: Dict[DiagramType, float],
        target_domain: DiagramDomain
    ) -> float:
        """Calculate confidence for domain classification"""
        domain_score = 0.0
        domain_count = 0

        for dtype, score in type_scores.items():
            category = get_category_for_type(dtype)
            domain = get_domain_for_category(category)
            if domain == target_domain:
                domain_score += score
                domain_count += 1

        if domain_count == 0:
            return 0.5

        return min(domain_score / domain_count, 1.0)

    def _calculate_category_confidence(
        self,
        type_scores: Dict[DiagramType, float],
        target_category: DiagramCategory
    ) -> float:
        """Calculate confidence for category classification"""
        category_score = 0.0
        category_count = 0

        for dtype, score in type_scores.items():
            category = get_category_for_type(dtype)
            if category == target_category:
                category_score += score
                category_count += 1

        if category_count == 0:
            return 0.5

        return min(category_score / category_count, 1.0)

    def _generate_clarification_questions(
        self,
        request: str,
        type_scores: Dict[DiagramType, float],
        domain: DiagramDomain
    ) -> List[str]:
        """Generate questions to clarify ambiguous requests"""
        questions = []

        if not type_scores:
            questions.append("What type of diagram would you like? (e.g., architecture, sequence, data flow)")

        # Check for ambiguous domain
        domains_detected = set()
        for dtype in type_scores.keys():
            category = get_category_for_type(dtype)
            d = get_domain_for_category(category)
            domains_detected.add(d)

        if len(domains_detected) > 1:
            questions.append(f"Is this for {' or '.join(d.value for d in domains_detected)}?")

        # Ask about complexity if not clear
        if "complex" not in request.lower() and "simple" not in request.lower():
            questions.append("What level of detail do you need? (overview, detailed, comprehensive)")

        # Ask about audience
        if not any(kw in request.lower() for keywords in self._audience_keywords.values() for kw in keywords):
            questions.append("Who is the target audience? (executives, developers, architects)")

        return questions[:3]  # Limit to 3 questions


def classify_request(
    request: str,
    context: Optional[Dict] = None
) -> ClassificationResult:
    """
    Convenience function to classify a request.

    Args:
        request: Natural language request
        context: Optional context dictionary

    Returns:
        ClassificationResult

    Example:
        >>> result = classify_request("Show me a microservices architecture diagram")
        >>> print(result.diagram_type)  # DiagramType.MICROSERVICES_ARCH
    """
    classifier = RequestClassifier()
    return classifier.classify(request, context)
