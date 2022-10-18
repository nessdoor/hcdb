"""Implements the database operations."""
from argparse import Namespace
from itertools import chain
from pathlib import Path
from sys import stdin, stdout
from tempfile import NamedTemporaryFile

import cdblib


def add_kvs(dbfile, kvs: list[tuple[str]]) -> None:
    """Add a list of key/value pairs to a CDB."""
    with cdblib.Writer(dbfile) as db:
        for k, v in kvs:
            db.putstring(k, v)


def make(pargs: Namespace) -> None:
    """Make a new CDB from scratch."""
    # Convert input k/v pairs into a list of tuples
    kvs = map(tuple, pargs.pairs) if pargs.pairs else ()

    # If no file was specified, then write on stdout
    if pargs.file is not None:
        with open(file=pargs.file, mode='wb') as dbfile:
            add_kvs(dbfile, kvs)
    else:
        add_kvs(stdout, kvs)


def print_vals(db: cdblib.Reader, key: str) -> None:
    """Print all values associated with a key."""
    for v in db.gets(key):
        print(v)


def query(pargs: Namespace) -> None:
    """Query an existing CDB."""
    # If no file was specified, then read from stdin
    if pargs.file is not None:
        with cdblib.Reader.from_file_path(pargs.file) as db:
            print_vals(db, pargs.key)
    else:
        with cdblib.Reader.from_file_obj(stdin) as db:
            print_vals(db, pargs.key)


def add(pargs: Namespace) -> None:
    """Add key/value pairs to an existing CDB."""
    # Convert input k/v pairs into a list of tuples of bytes
    kvs = map(tuple, pargs.pairs) if pargs.pairs else ()
    kvs = ((bytes(k, encoding='utf-8'), bytes(v, encoding='utf-8'))
           for k, v in kvs)

    # Open temporary database in write mode in the destination directory
    tmpdbf = NamedTemporaryFile(mode='wb', dir=pargs.file.resolve().parent,
                                delete=False)
    with cdblib.Writer(tmpdbf) as wbd:

        # Open old database in read mode
        with cdblib.Reader.from_file_path(pargs.file) as rdb:

            # Produce an iterator that gives us a complete dump
            dump = rdb.iteritems()

            # Concatenate the new key/value pairs to the contents of the DB
            new_dump = chain(dump, kvs)

            # Transfer data into the new DB
            for k, v in new_dump:
                wbd.put(k, v)

    # Close the temporary file and rotate it in place of the old DB
    tmpdbf.close()
    Path(tmpdbf.name).replace(pargs.file)


def rm(pargs: Namespace) -> None:
    """Remove a key and all its associated values from a CDB."""
    # Open temporary database in write mode in the destination directory
    tmpdbf = NamedTemporaryFile(mode='wb', dir=pargs.file.resolve().parent,
                                delete=False)
    with cdblib.Writer(tmpdbf) as wbd:

        # Open old database in read mode
        with cdblib.Reader.from_file_path(pargs.file) as rdb:

            # Produce an iterator that gives us a complete dump
            dump = rdb.iteritems()

            # Convert the key in byte form
            bkey = bytes(pargs.key, encoding='utf-8')

            # Transfer data into the new DB, filtering-out values associated
            # with the target key
            for k, v in filter(lambda kv: kv[0] != bkey, dump):
                wbd.put(k, v)

    # Close the temporary file and rotate it in place of the old DB
    tmpdbf.close()
    Path(tmpdbf.name).replace(pargs.file)
