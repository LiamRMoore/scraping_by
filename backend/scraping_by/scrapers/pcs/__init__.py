import logging

from .interface import PCSRelease

log = logging.getLogger(__name__)

# present uniform alias to class implementing contract interface
contract_cls = PCSRelease
