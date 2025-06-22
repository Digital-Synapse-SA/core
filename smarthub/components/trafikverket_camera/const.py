"""Adds constants for Trafikverket Camera integration."""

from smarthub.const import Platform

DOMAIN = "trafikverket_camera"
PLATFORMS = [Platform.BINARY_SENSOR, Platform.CAMERA, Platform.SENSOR]
ATTRIBUTION = "Data provided by Trafikverket"

ATTR_DESCRIPTION = "description"
ATTR_TYPE = "type"
