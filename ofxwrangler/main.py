import argparse
import logging
import sys
from typing import TextIO

from ofxtools.Parser import OFXTree
from ofxtools.header import make_header
import xml.etree.ElementTree as ET


logging.basicConfig(level=logging.INFO)


class OFXSwapper:
    USELESS_NAMES = ["DEBIT", "CREDIT", "EFTPOS"]

    def __init__(self, inputFile: str):
        self._inputFile = inputFile
        self._parser = OFXTree()
        self._tree = self._parser.parse(self._inputFile)
        self._ofx = self._parser.convert()
        self._swap_names_and_memos()

    def _swap_names_and_memos(self):
        logging.info(self.USELESS_NAMES)
        statements = self._ofx.statements
        for statement in statements:
            logging.info(
                f"Processing statement for acct: {statement.bankacctfrom.bankid}-{statement.bankacctfrom.branchid}-{statement.bankacctfrom.acctid}"
            )
            transactions = statement.banktranlist
            for transaction in transactions:
                name: str = transaction.name
                memo: str = transaction.memo
                if name in self.USELESS_NAMES and memo is not None:
                    if memo.startswith("CARD"):
                        transaction.name = memo[9:].strip()
                        transaction.memo = f"{name} {memo[0:9]}".strip()
                    elif memo.startswith("FC"):
                        transaction.name = f"{memo[20:]} {memo[0:20]}".strip()
                        transaction.memo = name.strip()
                    else:
                        transaction.name = memo.strip()
                        transaction.memo = name.strip()
                    logging.info(
                        f"{transaction.dtposted.isoformat()} Swapped {transaction.memo} for {transaction.name}"
                    )

    def write_file(self, file: TextIO):
        root = self._ofx.to_etree()
        message = ET.tostring(root).decode()
        header = str(make_header(version=220))
        file.write(header + message)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Swap name and memo fields in an OFX file."
    )
    parser.add_argument("input", help="an OFX file to parse")
    parser.add_argument(
        "--overwrite",
        "-o",
        help="overwrite input file, otherwise write to stdout",
        action="store_true",
    )
    args = parser.parse_args()

    logging.info("Parsing...")
    swapper = OFXSwapper(args.input)
    if args.overwrite:
        swapper.write_file(open(args.input, "w"))
    else:
        swapper.write_file(sys.stdout)
