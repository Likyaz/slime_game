from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from systems.data.storage import DataStorage


class DataEntity:
    def __init__(self, data_storage: "DataStorage" = None):
        self.data_storage = data_storage
