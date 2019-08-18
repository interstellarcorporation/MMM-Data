from usefull import get_json, is_date, merge_date, file_name
import os
import datetime

if __name__ == "__main__":
    import argparse

    class Args:
        def __init__(self):
            parser = argparse.ArgumentParser()

            # Positional mandatory arguments
            parser.add_argument(
                "Currency", help="The currency you want to merge.", type=str
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

        def out(self, msg: str):
            if self.output:
                with open(self.output, "a") as f:
                    f.write(msg + "\n")
            else:
                print(msg)

        def debug(self, msg: str):
            if self.verbose:
                print(msg)
            if self.logfile:
                with open(self.logfile, "a") as f:
                    f.write(msg + "\n")

    args = Args()
    for e in args.dates:
        args.out(e)
