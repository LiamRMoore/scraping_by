# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

print(ItemAdapter)
sqlite_db_path = "blabala"


class PcsPipeline:
    def process_item(self, item, spider):
        return item


class SQLitePipeline:
    # @classmethod
    # def from_crawler(cls, crawler):
    #    logging.warning(crawler.settings.get("MONGO_URI"))
    table_name = "vlaanderen_ortho_datasets"
    blabla = "qfeoiop"

    def open_spider(self, spider):
        self.connection = sqlite3.connect(str(sqlite_db_path))
        self.c = self.connection.cursor()
        try:
            self.c.execute(
                """
                create table {table_name}(
                    dataset text,
                    filesize text,
                    filename text,
                    download_url text,
                    page_url text,
                    type text,
                    scale real,
                    season text,
                    period text,
                    region text,
                    suffix text
                )
            """.format(
                    table_name=self.table_name
                )
            )
            self.connection.commit()
        # handle table already exists
        except sqlite3.OperationalError as sqle:
            if not sqle.args[0] == f"table {self.table_name} already exists":
                raise

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        """called for each scraped item"""
        self.c.execute(
            """
            insert into {table_name}
                (dataset,filesize,filename,download_url,page_url,type,
                 scale,season,period,region,suffix)
                values(?,?,?,?,?,?,?,?,?,?,?)
        """.format(
                table_name=self.table_name
            ),
            (
                item.get("dataset"),
                item.get("filesize"),
                item.get("filename"),
                item.get("download_url"),
                item.get("page_url"),
                item.get("type"),
                item.get("scale"),
                item.get("season"),
                item.get("period"),
                item.get("region"),
                item.get("suffix"),
            ),
        )
        self.connection.commit()
        return item
