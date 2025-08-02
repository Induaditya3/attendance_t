from rich.table import Table
from textual.color import Color
from textual.containers import Container,Horizontal, VerticalScroll, HorizontalScroll
from textual import on

from textual.app import App, ComposeResult
from textual.widgets import Static, Header, Footer, Button

CURRENT_DATE = "2025 "
ROW = f"""
[@click=app.markAttend('{CURRENT_DATE}','A')]Absent
[@click=app.markAttend('{CURRENT_DATE}','P')]Present
"""
# after applying grid property some part of the table is clipped
# for now LastTen is kept for future reference
class LastTen(Static):
    # this looks odd like someone put a sticker when height, width is auto
    # even after manual spec using % it only extends background of table and looks odd stil
    # if cannot be fixed use Static widget instead
    def on_mount(self,attend = "H") -> None:
        # TO-DO: add border and title of subject
        table = Table("Date","Day","Attend")
        for i in range(10):
            table.add_row(
                "2025-07-"+str(i),
                "Monday",
                "Absent" if attend == "A" else ("Present" if attend == "P" else "Holiday")
            )
        self.update(table)


# for passing info when certain event occurs use message - refer to message.py
class MyApp(App[str]):
    BINDINGS = [
        ('p','present_today()',"present today"),
        ('a','absent_today()',"absent today"),
        ('h','holiday_today()',"holiday today")
    ]
    CSS_PATH = "ui.tcss"
    TITLE = "Attainder App"
    SUB_TITLE = "The attendance tracker by Induaditya3"

    def compose(self) -> ComposeResult:
        yield Header(id="header") # give " " as arg to display time in header
        with Container(id="app-grid"):
            # sidebar buttons
            # these are mounted verically
            with Static(classes="sidebar"):
                yield Button("S", id="stat",variant="primary")
                yield Button("LT", id="last_ten", variant="success")
                # TO-DO: change color of the rest of buttons by looking up doc of Button and variant
                yield Button("CD", id="custom_date",variant="default")
                yield Button("CT", id="custom_today",variant="warning")
                yield Button("CS", id="custom_stat")
                yield Button("Q", id="quit",variant="error")
            with VerticalScroll(id="main-pane"):
                yield Static(ROW)
        # how custom today button will show row along with option
        # TO-DO: add border and title of subject
        # TO-DO: also reduce the margin and border of below, so it does not overlap sidebar buttons
                with Horizontal(classes="columns"):
                    # date = "2025-07-29"
                    # yield Static("2025-07-29")
                    # yield Button("Absent",variant="warning",id="A_"+date)
                    # yield Button("Present",variant="success",id="P_" + date)
                    # yield Button("Holiday",variant="primary",id="H_" + date)
                    yield Static("a",id="a")
                    yield Button("b",id="b")
                    yield Button("c")
        yield Footer()
    # this works on applies on all button
    # def on_button_pressed(self, event: Button.Pressed) -> None:
    #     self.exit(event.button.id)
    def action_markAttend(self,date,attend):
        yield Static(date+attend)
    def action_absent_today(self):
        # TO-DO: update database to mark all subject absent according to routine
        # also show some sort of confirmation message
        pass
    def action_present_today(self):
        # TO-DO
        pass
    def action_holiday_today(self):
        # TO-DO
        pass
    @on(Button.Pressed, "#stat")  
    def show_stat(self):
        """Called when the stat button is pressed."""
        pass
    @on(Button.Pressed,"#last_ten")
    def show_last_ten(self):
        """Called when last ten button is pressed"""
        pass
    @on(Button.Pressed,"#custom_date")
    def option_custom_date(self):
        """Called when custom date button is pressed"""
        pass
    @on(Button.Pressed,"#custom_today")
    def option_custom_today(self):
        """Called when custom today button is pressed"""
        pass
    @on(Button.Pressed,"#custom_stat")
    def option_custom_stat(self):
        """Called when custom stat button is pressed"""
        pass
    @on(Button.Pressed,"#quit")
    def quit(self):
        """Called when quit button is pressed"""
        # close database connection
        return "exit"
        self.exit()


if __name__ == "__main__":
    app = MyApp()
    app.run()