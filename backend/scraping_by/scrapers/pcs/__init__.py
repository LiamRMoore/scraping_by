import logging

from scraping_by.scrapers.pcs.interface import PCSRelease
from scraping_by.scrapers.pcs.scrape import get_notices


log = logging.getLogger(__name__)

# present uniform alias to class implementing contract interface
contract_cls = PCSRelease

# flake8 fuck off
get_notices
