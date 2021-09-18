"""
Implements an
"""
from scraping_by.scrapers.contract import ContractInterface


class PCSRelease(ContractInterface):
    """
    Wrapper for deserialised OCDS "Release" entry which has been
    compiled into an up-to-data entry by OCDSKit's compile

    Implements ContractInterface; (via _build_contract_json)
    """

    @property
    def contract_notice(self):
        notices = [
            d
            for d in self.data.tender.documents
            if d.documentType == "contractNotice"
        ]
        if notices:
            return notices[0]

    @property
    def lots_description(self):
        return "\n".join([lot.description for lot in self.data.tender.lots])

    @property
    def first_lot_duration(self):
        return self.data.tender.lots[0].contractPeriod.durationInDays

    def _build_contract_json(self):
        data = {
            "id": self.data.id,
            "ocid": self.data.ocid,
            "notice_url": self.contract_notice.url,
            "notice_description": self.contract_notice.description,
            "notice_title": self.contract_notice.title,
            "date_last_update": self.data.date,
            "title": self.data.tender.title,
            "tender_description": self.data.tender.description,
            "status": self.data.tender.status,
            "buyer": self.data.buyer.name,
            "n_lots": len(self.data.tender.lots),
            "lots_description": self.lots_description,
            "first_lot_duration_days": self.first_lot_duration,
        }
        if self.data.tender.awardPeriod:
            data.update(award_start_date=self.data.tender.awardPeriod.startDate)
        if self.data.tender.tenderPeriod:
            data.update(tender_end_date=self.data.tender.tenderPeriod.endDate)
        if self.data.tender.value:
            data.update(
                value=self.data.tender.value.amount,
                currency=self.data.tender.value.currency,
            )
        return data
