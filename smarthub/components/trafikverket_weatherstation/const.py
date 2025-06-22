"""Adds constants for Trafikverket Weather integration."""

from smarthub.const import Platform

DOMAIN = "trafikverket_weatherstation"
CONF_STATION = "station"
PLATFORMS = [Platform.SENSOR]
ATTRIBUTION = "Data provided by Trafikverket"
