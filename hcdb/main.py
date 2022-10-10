from argparse import ArgumentParser

cmdparser = ArgumentParser(prog="cdb",
                           description="Create and query CDBs.")


def main():
    cmdparser.parse_args()


if __name__ == '__main__':
    main()
