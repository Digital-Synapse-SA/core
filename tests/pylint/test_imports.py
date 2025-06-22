"""Tests for pylint hass_imports plugin."""

from __future__ import annotations

import astroid
from pylint.checkers import BaseChecker
import pylint.testutils
from pylint.testutils.unittest_linter import UnittestLinter
import pytest

from . import assert_adds_messages, assert_no_messages


@pytest.mark.parametrize(
    ("module_name", "import_from", "import_what"),
    [
        (
            "smarthub.components.pylint_test.sensor",
            "smarthub.const",
            "CONSTANT",
        ),
        (
            "smarthub.components.pylint_test.sensor",
            "smarthub.components.pylint_testing",
            "CONSTANT",
        ),
        ("smarthub.components.pylint_test.sensor", ".const", "CONSTANT"),
        ("smarthub.components.pylint_test.sensor", ".", "CONSTANT"),
        ("smarthub.components.pylint_test.sensor", "..", "pylint_test"),
        (
            "smarthub.components.pylint_test.api.hub",
            "smarthub.const",
            "CONSTANT",
        ),
        ("smarthub.components.pylint_test.api.hub", "..const", "CONSTANT"),
        ("smarthub.components.pylint_test.api.hub", "..", "CONSTANT"),
        ("smarthub.components.pylint_test.api.hub", "...", "pylint_test"),
        ("tests.components.pylint_test.api.hub", "..const", "CONSTANT"),
    ],
)
def test_good_import(
    linter: UnittestLinter,
    imports_checker: BaseChecker,
    module_name: str,
    import_from: str,
    import_what: str,
) -> None:
    """Ensure good imports pass through ok."""

    import_node = astroid.extract_node(
        f"from {import_from} import {import_what} #@",
        module_name,
    )
    imports_checker.visit_module(import_node.parent)

    with assert_no_messages(linter):
        imports_checker.visit_importfrom(import_node)


@pytest.mark.parametrize(
    ("module_name", "import_from", "import_what", "error_code"),
    [
        (
            "smarthub.components.pylint_test.sensor",
            "smarthub.components.pylint_test.const",
            "CONSTANT",
            "hass-relative-import",
        ),
        (
            "smarthub.components.pylint_test.sensor",
            "..const",
            "CONSTANT",
            "hass-absolute-import",
        ),
        (
            "smarthub.components.pylint_test.sensor",
            "...const",
            "CONSTANT",
            "hass-absolute-import",
        ),
        (
            "smarthub.components.pylint_test.api.hub",
            "smarthub.components.pylint_test.api.const",
            "CONSTANT",
            "hass-relative-import",
        ),
        (
            "smarthub.components.pylint_test.api.hub",
            "...const",
            "CONSTANT",
            "hass-absolute-import",
        ),
        (
            "smarthub.components.pylint_test.api.hub",
            "smarthub.components",
            "pylint_test",
            "hass-relative-import",
        ),
        (
            "smarthub.components.pylint_test.api.hub",
            "smarthub.components.pylint_test.const",
            "CONSTANT",
            "hass-relative-import",
        ),
        (
            "tests.components.pylint_test.api.hub",
            "tests.components.pylint_test.const",
            "CONSTANT",
            "hass-relative-import",
        ),
        (
            "tests.components.pylint_test.api.hub",
            "...const",
            "CONSTANT",
            "hass-absolute-import",
        ),
    ],
)
def test_bad_import(
    linter: UnittestLinter,
    imports_checker: BaseChecker,
    module_name: str,
    import_from: str,
    import_what: str,
    error_code: str,
) -> None:
    """Ensure bad imports are rejected."""

    import_node = astroid.extract_node(
        f"from {import_from} import {import_what} #@",
        module_name,
    )
    imports_checker.visit_module(import_node.parent)

    with assert_adds_messages(
        linter,
        pylint.testutils.MessageTest(
            msg_id=error_code,
            node=import_node,
            args=None,
            line=1,
            col_offset=0,
            end_line=1,
            end_col_offset=len(import_from) + len(import_what) + 13,
        ),
    ):
        imports_checker.visit_importfrom(import_node)


@pytest.mark.parametrize(
    ("import_node", "module_name"),
    [
        (
            "from smarthub.components import climate",
            "smarthub.components.pylint_test.climate",
        ),
        (
            "from smarthub.components.climate import ClimateEntityFeature",
            "smarthub.components.pylint_test.climate",
        ),
        (
            "from smarthub.components.pylint_test import const",
            "tests.components.pylint_test.climate",
        ),
        (
            "from smarthub.components.pylint_test.const import CONSTANT",
            "tests.components.pylint_test.climate",
        ),
        (
            "import smarthub.components.pylint_test.const as climate",
            "tests.components.pylint_test.climate",
        ),
    ],
)
def test_good_root_import(
    linter: UnittestLinter,
    imports_checker: BaseChecker,
    import_node: str,
    module_name: str,
) -> None:
    """Ensure bad root imports are rejected."""

    node = astroid.extract_node(
        f"{import_node} #@",
        module_name,
    )
    imports_checker.visit_module(node.parent)

    with assert_no_messages(linter):
        if import_node.startswith("import"):
            imports_checker.visit_import(node)
        if import_node.startswith("from"):
            imports_checker.visit_importfrom(node)


@pytest.mark.parametrize(
    ("import_node", "module_name"),
    [
        (
            "import smarthub.components.climate.const as climate",
            "smarthub.components.pylint_test.climate",
        ),
        (
            "from smarthub.components.climate import const",
            "smarthub.components.pylint_test.climate",
        ),
        (
            "from smarthub.components.climate.const import ClimateEntityFeature",
            "smarthub.components.pylint_test.climate",
        ),
        (
            "from smarthub.components.climate.entity import ClimateEntityFeature",
            "smarthub.components.pylint_test.climate",
        ),
        (
            "from smarthub.components.climate import const",
            "tests.components.pylint_test.climate",
        ),
        (
            "from smarthub.components.climate.const import CONSTANT",
            "tests.components.pylint_test.climate",
        ),
        (
            "import smarthub.components.climate.const as climate",
            "tests.components.pylint_test.climate",
        ),
        (
            "import smarthub.components.climate.entity as climate",
            "tests.components.pylint_test.climate",
        ),
    ],
)
def test_bad_root_import(
    linter: UnittestLinter,
    imports_checker: BaseChecker,
    import_node: str,
    module_name: str,
) -> None:
    """Ensure bad root imports are rejected."""

    node = astroid.extract_node(
        f"{import_node} #@",
        module_name,
    )
    imports_checker.visit_module(node.parent)

    with assert_adds_messages(
        linter,
        pylint.testutils.MessageTest(
            msg_id="hass-component-root-import",
            node=node,
            args=None,
            line=1,
            col_offset=0,
            end_line=1,
            end_col_offset=len(import_node),
        ),
    ):
        if import_node.startswith("import"):
            imports_checker.visit_import(node)
        if import_node.startswith("from"):
            imports_checker.visit_importfrom(node)


@pytest.mark.parametrize(
    ("import_node", "module_name", "expected_args"),
    [
        (
            "from smarthub.helpers.issue_registry import async_get",
            "tests.components.pylint_test.climate",
            (
                "async_get",
                "smarthub.helpers.issue_registry",
                "ir",
                "ir",
                "async_get",
            ),
        ),
        (
            "from smarthub.helpers.issue_registry import async_get as async_get_issue_registry",
            "tests.components.pylint_test.climate",
            (
                "async_get",
                "smarthub.helpers.issue_registry",
                "ir",
                "ir",
                "async_get",
            ),
        ),
    ],
)
def test_bad_namespace_import(
    linter: UnittestLinter,
    imports_checker: BaseChecker,
    import_node: str,
    module_name: str,
    expected_args: tuple[str, ...],
) -> None:
    """Ensure bad namespace imports are rejected."""

    node = astroid.extract_node(
        f"{import_node} #@",
        module_name,
    )
    imports_checker.visit_module(node.parent)

    with assert_adds_messages(
        linter,
        pylint.testutils.MessageTest(
            msg_id="hass-helper-namespace-import",
            node=node,
            args=expected_args,
            line=1,
            col_offset=0,
            end_line=1,
            end_col_offset=len(import_node),
        ),
    ):
        imports_checker.visit_importfrom(node)


@pytest.mark.parametrize(
    ("module_name", "import_string", "end_col_offset"),
    [
        (
            "smarthub.components.pylint_test.sensor",
            "from smarthub.components.other import DOMAIN as OTHER_DOMAIN",
            -1,
        ),
        (
            "smarthub.components.pylint_test.sensor",
            "from smarthub.components.other import DOMAIN",
            49,
        ),
    ],
)
def test_domain_alias(
    linter: UnittestLinter,
    imports_checker: BaseChecker,
    module_name: str,
    import_string: str,
    end_col_offset: int,
) -> None:
    """Ensure good imports pass through ok."""

    import_node = astroid.extract_node(
        f"{import_string}  #@",
        module_name,
    )
    imports_checker.visit_module(import_node.parent)

    expected_messages = []
    if end_col_offset > 0:
        expected_messages.append(
            pylint.testutils.MessageTest(
                msg_id="hass-import-constant-alias",
                node=import_node,
                args=("DOMAIN", "DOMAIN", "OTHER_DOMAIN"),
                line=1,
                col_offset=0,
                end_line=1,
                end_col_offset=end_col_offset,
            )
        )

    with assert_adds_messages(linter, *expected_messages):
        if import_string.startswith("import"):
            imports_checker.visit_import(import_node)
        else:
            imports_checker.visit_importfrom(import_node)
