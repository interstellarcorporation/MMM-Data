from usefull import get_json, is_date, file_name
from matplotlib import pyplot as plt
import os
import datetime

if __name__ == "__main__":
    import argparse

    class Args:
        def __init__(self):
            parser = argparse.ArgumentParser()

            # Positional mandatory arguments
            parser.add_argument(
                "Currency", help="The currency you want to view.", type=str
            )
            parser.add_argument("Start", help="The start date.", type=str)
            parser.add_argument("Stop", help="The stop date.", type=str)

            # Optional arguments
            parser.add_argument(
                "-o", "--output", help="Write output in a file.", type=str
            )
            parser.add_argument(
                "-v",
                "--verbose",
                help="Verbose mod.",
                type=bool,
                nargs="?",
                const=True,
                default=False,
            )
            parser.add_argument(
                "-i",
                "--ignore",
                help="Ignore errors.",
                type=bool,
                nargs="?",
                const=True,
                default=False,
            )
            parser.add_argument("-l", "--log", help="Write logs in a file.", type=str)

            self.args = parser.parse_args()

            if self.currency not in os.listdir("data/"):
                raise AttributeError("Currency can't be recognized")
            if self.start is None:
                raise AttributeError("Start date can't be recognized")
            if self.stop is None:
                raise AttributeError("Stop date can't be recognized")
            if (self.stop - self.start).total_seconds() < 0:
                raise AttributeError("Start date must be after stop date")

        @property
        def currency(self):
            return self.args.Currency

        @property
        def start(self):
            return is_date(self.args.Start + ".json")

        @property
        def stop(self):
            return is_date(self.args.Stop + ".json")

        @property
        def dates(self):
            dates_names = []
            i = self.start
            while (self.stop - i).total_seconds() >= 0:
                dates_names.append(file_name(self.currency, i))
                i = i + datetime.timedelta(days=1)
            return dates_names

        @property
        def output(self):
            return self.args.output

        @property
        def verbose(self):
            return self.args.verbose

        @property
        def ignore(self):
            return self.args.ignore

        @property
        def logfile(self):
            return self.args.log

        def _out(self, fig: plt.Figure):
            if self.output:
                fig.savefig(self.output)
            else:
                fig.show()

        def debug(self, msg: str):
            if self.verbose:
                print(msg)
            if self.logfile:
                with open(self.logfile, "a") as f:
                    f.write(msg + "\n")

        def run(self):
            _all_data = []
            for file in self.dates:
                try:
                    curr_json = get_json(file)
                    self.debug(f"File {file} opened.")
                    for e in curr_json:
                        e["time"].update(
                            {
                                "year": int(file[-9:-5]),
                                "month": int(file[-11:-9]),
                                "day": int(file[-13:-11]),
                            }
                        )
                        _all_data.append(e)
                except FileNotFoundError:
                    if self.ignore:
                        self.debug(f"File {file} not found, ignored.")
                    else:
                        raise FileNotFoundError(f"File {file} not found.")

            self.debug("Generating graph")
            _fig, _ax = plt.subplots()

            _dates = [
                        datetime.datetime(
                            year=e["time"]["year"],
                            month=e["time"]["month"],
                            day=e["time"]["day"],
                            hour=e["time"]["hour"],
                            minute=e["time"]["minute"],
                            second=e["time"]["second"]
                                          )
                        for e in _all_data]
            _prices = [e["price"] for e in _all_data]
            _ax.plot(_dates, _prices, "k+")

            self.debug("\n".join(map(str, _dates)))
            self.debug(f"Graph generated with {len(_prices)} points")
            self._out(_fig)

    args = Args()
    args.run()
