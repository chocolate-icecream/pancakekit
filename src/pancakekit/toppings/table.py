from ..pancakekit import Topping, Tag
from ..utils import *  

class Table(Topping):
    HEIGHT_SHRINK = 0.9
    def __init__(self, table=None, *, height:float=0.5, **kwargs):
        super().__init__(table, height=height, **kwargs)

    def prepare(self, table, *, height):
        self.height = height
        self.table = None
        self.num_rows = 0
        self.headers = []
        self.original_type = None
        self.set(table)
    
    def set(self, table):
        if table is None:
            self.table = None
            return
        if is_pandas_dataframe(table):
            table = table.to_dict(orient="list")
            self.original_type = "pandas"
        if isinstance(table, list):
            table = {"-": table}
            self.original_type = "list"

        assert isinstance(table, dict)
        self.table = table
        self.num_rows = max([len(x) for x in table.values()])
        self.headers = list(table.keys())
        self.updated()
        
    def html(self):
        if self.table is None:
            return ""
        style = {"overflow-x": "auto", "overflow-y": "auto", "max-height": f"{self.height*self.HEIGHT_SHRINK*900}px"}
        div = Tag("div", {"class": "w3-border"}, style=style)
        table = div.add("table", {"class": "w3-table w3-striped w3-bordered w3-hoverable w3-small"})
        thread = table.add("thread")
        tr = thread.add("tr")
        if self.original_type not in ["list"]:
            for column in self.headers:
                th = tr.add("th")
                title = " ".join(column.split("_")).capitalize()
                if "units" in self.arguments and column in self.arguments["units"]:
                    title += f" ({self.arguments['units'][column]})"
                th.add_html(title)
        max_row_dict = {c: len(self.table[c]) for c in self.headers}
        for i in range(self.num_rows):
            tr = table.add("tr")
            tr.set_click_response({"row": i})
            for column in self.headers:
                td = tr.add("td")
                if i >= max_row_dict[column] or self.table[column][i] is None:
                    td.add_html("---")
                    continue
                item = self.table[column][i]
                s = get_formatted_number_str(item)
                td.add_html(s)
        return div.render()
    
    def event_preprocessor(self, event):
        if event.event_type == "onclick":
            row = event.value['row']
            value = {c: self.table[c][row] if row < len(self.table[c]) else None for c in self.headers}
            if self.original_type == "list":
                value = value["-"]
            self.value = (row, value)
            return self.value
    
    def value_getter(self):
        return super().value_getter()