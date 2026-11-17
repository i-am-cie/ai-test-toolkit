"""prompt-templates: Shared prompt templates for AI Test Toolkit."""

from .test_generation import (
    UNIT_TEST_PROMPT,
    TEST_PLAN_PROMPT,
    EDGE_CASES_PROMPT,
    STRUCTURED_TEST_CASES_PROMPT,
)
from .code_review import (
    FULL_REVIEW_PROMPT,
    SECURITY_REVIEW_PROMPT,
    STYLE_REVIEW_PROMPT,
)
from .api_test import (
    API_TEST_GENERATION_PROMPT,
    API_RUN_PROMPT,
)
from .sql_test import (
    DATA_QUALITY_SQL_PROMPT,
    SQL_TEST_GENERATION_PROMPT,
    SQL_PERFORMANCE_PROMPT,
    SCHEMA_REVIEW_PROMPT,
)
from .e2e_test import (
    E2E_TEST_GENERATION_PROMPT,
)
from .perf_test import (
    PERF_TEST_GENERATION_PROMPT,
)

__all__ = [
    # test_generation
    "UNIT_TEST_PROMPT",
    "TEST_PLAN_PROMPT",
    "EDGE_CASES_PROMPT",
    "STRUCTURED_TEST_CASES_PROMPT",
    # code_review
    "FULL_REVIEW_PROMPT",
    "SECURITY_REVIEW_PROMPT",
    "STYLE_REVIEW_PROMPT",
    # api_test
    "API_TEST_GENERATION_PROMPT",
    "API_RUN_PROMPT",
    # sql_test
    "DATA_QUALITY_SQL_PROMPT",
    "SQL_TEST_GENERATION_PROMPT",
    "SQL_PERFORMANCE_PROMPT",
    "SCHEMA_REVIEW_PROMPT",
    # e2e_test
    "E2E_TEST_GENERATION_PROMPT",
    # perf_test
    "PERF_TEST_GENERATION_PROMPT",
]
