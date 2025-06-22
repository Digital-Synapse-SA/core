"""Support for LIRC devices."""

import logging
import threading
import time

import lirc

from smarthub.const import EVENT_HOMEASSISTANT_START, EVENT_HOMEASSISTANT_STOP
from smarthub.core import DOMAIN as HOMEASSISTANT_DOMAIN, SmartHub
from smarthub.helpers import config_validation as cv
from smarthub.helpers.issue_registry import IssueSeverity, create_issue
from smarthub.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)

BUTTON_NAME = "button_name"

DOMAIN = "lirc"

EVENT_IR_COMMAND_RECEIVED = "ir_command_received"

ICON = "mdi:remote"

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)


def setup(hass: SmartHub, config: ConfigType) -> bool:
    """Set up the LIRC capability."""
    create_issue(
        hass,
        HOMEASSISTANT_DOMAIN,
        f"deprecated_system_packages_yaml_integration_{DOMAIN}",
        breaks_in_ha_version="2025.12.0",
        is_fixable=False,
        issue_domain=DOMAIN,
        severity=IssueSeverity.WARNING,
        translation_key="deprecated_system_packages_yaml_integration",
        translation_placeholders={
            "domain": DOMAIN,
            "integration_title": "LIRC",
        },
    )
    # blocking=True gives unexpected behavior (multiple responses for 1 press)
    # also by not blocking, we allow hass to shut down the thread gracefully
    # on exit.
    lirc.init("smart-hub", blocking=False)
    lirc_interface = LircInterface(hass)

    def _start_lirc(_event):
        lirc_interface.start()

    def _stop_lirc(_event):
        lirc_interface.stopped.set()

    hass.bus.listen_once(EVENT_HOMEASSISTANT_START, _start_lirc)
    hass.bus.listen_once(EVENT_HOMEASSISTANT_STOP, _stop_lirc)

    return True


class LircInterface(threading.Thread):
    """Interfaces with the lirc daemon to read IR commands.

    When using lirc in blocking mode, sometimes repeated commands get produced
    in the next read of a command so we use a thread here to just wait
    around until a non-empty response is obtained from lirc.
    """

    def __init__(self, hass):
        """Construct a LIRC interface object."""
        threading.Thread.__init__(self)
        self.daemon = True
        self.stopped = threading.Event()
        self.hass = hass

    def run(self):
        """Run the loop of the LIRC interface thread."""
        _LOGGER.debug("LIRC interface thread started")
        while not self.stopped.is_set():
            try:
                code = lirc.nextcode()  # list; empty if no buttons pressed
            except lirc.NextCodeError:
                _LOGGER.warning("Error reading next code from LIRC")
                code = None
            # interpret result from python-lirc
            if code:
                code = code[0]
                _LOGGER.debug("Got new LIRC code %s", code)
                self.hass.bus.fire(EVENT_IR_COMMAND_RECEIVED, {BUTTON_NAME: code})
            else:
                time.sleep(0.2)
        lirc.deinit()
        _LOGGER.debug("LIRC interface thread stopped")
