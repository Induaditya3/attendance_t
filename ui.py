from rich.table import Table
from textual.color import Color
from textual.containers import Horizontal, Vertical

from textual.app import App, ComposeResult
from textual.widgets import Static, Header, Footer, Button

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

INSTRUCTIONS = (
    "\nStat - displays current percentage of attendance\n",
    "Last Ten - displays 10 records of each subjects\n",
    "Custom Date - to mark attendace on custom date\n",
    "Custom Today - o mark attendance of selected subject according to routine\n",
    "Custom Stat - to compute percentage of attendace given start date and end date\n",
    "Quit - to exit app gracefully\n",
    "a  - to mark attendance of selected subject according to routine\n",
    "p  - to compute percentage of attendace given start date and end date\n",
    "h -  to exit gracefully ,i.e. , after closing the database connection"
)
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
        # sidebar buttons
        # these are mounted verically
        with Static(classes="sidebar"):
            yield Button("Stat", id="stat",variant="primary")
            yield Button("Last Ten", id="last_ten", variant="success")
            # TO-DO: change color of the rest of buttons by looking up doc of Button and variant
            yield Button("Custom Date", id="custom_date")
            yield Button("Custom Today", id="custom_today")
            yield Button("Custom Stat", id="custom_stat")
            yield Button("Quit", id="quit",variant="error")
        for i in range(len(INSTRUCTIONS)):
            yield Static(INSTRUCTIONS[i], id = f"instruction{i}")
        
        yield LastTen()
        yield Header(id="header") # give " " as arg to display time in header
        yield Footer()
        # how custom today button will show row along with option
        # TO-DO: add border and title of subject
        # TO-DO: also reduce the margin and border of below, so it does not overlap sidebar buttons
        with Horizontal(classes="columns"):
            date = "2025-07-29"
            yield Static(date)
            yield Button("Absent",variant="warning",id="A_"+date)
            yield Button("Present",variant="success",id="P_" + date)
            yield Button("Holiday",variant="primary",id="H_" + date)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.exit(event.button.id)
    
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


if __name__ == "__main__":
    app = MyApp()
    app.run()