from ..pancakekit import Topping, Tag
from ..utils import *
from collections.abc import Iterable  
import pandas as pd   

class Table(Topping):
    pd = None
    HEIGHT_SHRINK = 0.9
    def __init__(self, df=None, header=None, height:float=0.5, **kwargs):
        super().__init__(df, header, height, **kwargs)

    def prepare(self, df=None, header=None, height=0.5):
        df = pd.DataFrame()
        self.height = height
        self.header = None
        self.df = None
        self.set(df, header)
        
    
    def set(self, df, header=None):
        if df is None:
            return
        if isinstance(df, list):
            if header is not None:
                if isinstance(header, str):
                    df = pd.DataFrame(df, columns=[header])
                else:
                    df = pd.DataFrame(df, columns=header)
            else:
                df = pd.DataFrame(df)
        
        self.df = df
        if header is None:
            self.header = self.df.columns
        elif isinstance(header, Iterable):
            self.header = header
        self.updated()
        
    def html(self):
        if self.df is None or self.header is None:
            return ""
        style = {"overflow-x": "auto", "overflow-y": "auto", "max-height": f"{self.height*self.HEIGHT_SHRINK*900}px"}
        div = Tag("div", {"class": "w3-border"}, style=style) #{self.height*self.HEIGHT_SHRINK*100}%
        table = div.add("table", {"class": "w3-table w3-striped w3-bordered w3-hoverable w3-small"})
        thread = table.add("thread")
        tr = thread.add("tr")
        if isinstance(self.header, str):
            self.header = [self.header]
        df = self.df[self.header]
        for column in df.columns:
            th = tr.add("th")
            title = " ".join(column.split("_")).capitalize()
            if "units" in self.arguments and column in self.arguments["units"]:
                title += f" ({self.arguments['units'][column]})"
            th.add_html(title)
        for i, row in df.iterrows():
            tr = table.add("tr")
            row = row.fillna("---")
            if self.clicked:
                tr.set_click_response({"row": i})
            for item in row:
                td = tr.add("td")
                s = get_formatted_number_str(item)
                td.add_html(s)
        return div.render()
    
    def event_preprocessor(self, event):
        if event.event_type == "onclick":
            return self.df.loc[event.value['row']]