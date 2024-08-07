#!/usr/bin/env python3
import logging
from ot import YaoGarbler
from alice import Alice
from bob import Bob

logging.basicConfig(format="[%(levelname)s] %(message)s",
                    level=logging.WARNING)

# Default print mode
PRINT_MODE = "none"

def execute(
        role,
        circuit_file="circuits/computerMaximum.json",
        use_ot=True,
        output_mode=PRINT_MODE,
        log_level=logging.WARNING,
        data_file="",
        bit_length=4
):
    logging.getLogger().setLevel(log_level)

    if not data_file.endswith('.txt'):
        logging.error("Data file must have a .txt extension")
        return

    if role == "alice":
        alice = Alice(circuit_file, oblivious_transfer=use_ot,
                      print_mode=output_mode, filename=data_file,
                      bit_size=int(bit_length))
        alice.start()
    elif role == "bob":
        bob = Bob(oblivious_transfer=use_ot,
                  filename=data_file)
        bob.listen()
    elif role == "local":
        local = LocalTest(circuit_file, print_mode=output_mode)
        local.start()
    else:
        logging.error(f"Unknown role '{role}'")


if __name__ == '__main__':
    import argparse

    def initialize():
        log_levels = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warning": logging.WARNING,
            "error": logging.ERROR,
            "critical": logging.CRITICAL
        }

        parser = argparse.ArgumentParser(description="Execute Yao protocol.")
        parser.add_argument("role",
                            choices=["alice", "bob", "local"],
                            help="the role to play in the protocol")
        parser.add_argument("-i",
                            "--input",
                            metavar="path",
                            default="",
                            help="path to the data file to read (default is empty)")
        parser.add_argument("-l",
                            "--loglevel",
                            metavar="level",
                            choices=log_levels.keys(),
                            default="warning",
                            help="the logging level (default 'warning')")

        args = parser.parse_args()

        execute(
            role=args.role,
            data_file=args.input,
            log_level=log_levels[args.loglevel]
        )

    initialize()
