"""Tests for hassfest dependency finder."""

import ast

import pytest

from script.hassfest.dependencies import ImportCollector


@pytest.fixture
def mock_collector():
    """Fixture with import collector that adds all referenced nodes."""
    collector = ImportCollector(None)
    collector.unfiltered_referenced = set()
    collector._add_reference = collector.unfiltered_referenced.add
    return collector


def test_child_import(mock_collector) -> None:
    """Test detecting a child_import reference."""
    mock_collector.visit(
        ast.parse(
            """

from smarthub.components import child_import
"""
        )
    )
    assert mock_collector.unfiltered_referenced == {"child_import"}


def test_subimport(mock_collector) -> None:
    """Test detecting a subimport reference."""
    mock_collector.visit(
        ast.parse(
            """

from smarthub.components.subimport.smart_home import EVENT_ALEXA_SMART_HOME
"""
        )
    )
    assert mock_collector.unfiltered_referenced == {"subimport"}


def test_child_import_field(mock_collector) -> None:
    """Test detecting a child_import_field reference."""
    mock_collector.visit(
        ast.parse(
            """

from smarthub.components.child_import_field import bla
"""
        )
    )
    assert mock_collector.unfiltered_referenced == {"child_import_field"}


def test_renamed_absolute(mock_collector) -> None:
    """Test detecting a renamed_absolute reference."""
    mock_collector.visit(
        ast.parse(
            """

import smarthub.components.renamed_absolute as hue
"""
        )
    )
    assert mock_collector.unfiltered_referenced == {"renamed_absolute"}


def test_all_imports(mock_collector) -> None:
    """Test all imports together."""
    mock_collector.visit(
        ast.parse(
            """

from smarthub.components import child_import

from smarthub.components.subimport.smart_home import EVENT_ALEXA_SMART_HOME

from smarthub.components.child_import_field import bla

import smarthub.components.renamed_absolute as hue
"""
        )
    )
    assert mock_collector.unfiltered_referenced == {
        "child_import",
        "subimport",
        "child_import_field",
        "renamed_absolute",
    }
