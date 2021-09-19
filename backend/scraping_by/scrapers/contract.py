"""
Defines a flat Contract data model which all scrapers must implement an interace to.
"""
import abc
from typing import Optional

from pydantic import BaseModel, HttpUrl


class Contract(BaseModel):
    id: str
    ocid: str
    notice_url: HttpUrl
    notice_description: str
    notice_title: str
    date_last_update: str
    title: str
    tender_description: str
    status: str
    buyer: str
    n_lots: int
    lots_description: str
    first_lot_duration_days: Optional[int] = None
    tender_end_date: Optional[str] = None
    award_start_date: Optional[str] = None
    value: Optional[float] = None
    currency: Optional[str] = None


class ContractInterface(abc.ABC):
    """
    Abstract base class definining a common interface for a contract
    """

    def __init__(self, data: BaseModel):
        self.data = data

    @abc.abstractmethod
    def _build_contract_json(self):
        pass

    @property
    def contract(self) -> Contract:
        return Contract(**self._build_contract_json())
