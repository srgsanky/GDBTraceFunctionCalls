# GDB trace function calls

The script `python_gdb_script.py` will help trace the function calls in a
program.

It uses GDB python APIs. See https://sourceware.org/gdb/download/onlinedocs/gdb/Python-API.html#Python-API

## Usage

Note: You will need gdb version 12 or above with python3 support.

Start your executable in gdb and source the python file. Run the program and
view the call hierarchy printed in the log file `gdb.txt`.

For e.g. if you are working with redis, build redis using `make all`, then run

```bash
gdb -q ./src/redis-server

# Within gdb
source python_gdb_script.py
run
```

Filter the output in `gdb.txt` using

```bash
grep CALL_TRACE gdb.txt | cut -d: -f 2
```

Paste the output in Mermaid editor to view the trace of function calls -
[Mermaid live editor](https://mermaid.live/edit).

## Development notes

The python library `types-gdb` provides the necessary gdb stubs to avoid errors
in the file. The actual `gdb` python module is not available as a library, it is
only provided by the gdb runtime.

## References

The following helped build this utility

* [Python scripts for GDB by Tarun Sharma](https://medium.com/@tarun27sh/python-scripts-for-gdb-9b17ca090ac5)
