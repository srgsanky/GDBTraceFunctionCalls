import gdb


def run_gdb_command(command: str):
    gdb.execute(command)


def log(text: str):
    gdb.write(f"{text}\n", gdb.STDLOG)


def setup():
    setup_commands = [
        "set pagination off",
        "set print pretty",

        # https://sourceware.org/gdb/current/onlinedocs/gdb.html/Logging-Output.html#Logging-Output
        # by default logging goes to gdb.txt
        "set logging enabled on",
        "set logging overwrite on",
        "show logging",
        "set logging redirect off",
        f"set confirm off",
    ]
    for c in setup_commands:
        run_gdb_command(c)


discovered_paths = set()


# Record stack trace when break point is hit
def stop_handler(event):
    if isinstance(event, gdb.BreakpointEvent):
        # https://sourceware.org/gdb/download/onlinedocs/gdb/Frames-In-Python.html#Frames-In-Python
        # https://sourceware.org/gdb/download/onlinedocs/gdb/Selection.html#Selection
        call_hierarchy = []
        while True:
            try:
                call_hierarchy.append(gdb.selected_frame().name())
                run_gdb_command("up-silently")  # Won't print the frame
            except BaseException as e:
                break

        call_hierarchy.reverse()

        new_paths_found = False
        i = 0
        while i < len(call_hierarchy) - 1:
            # The path is represented with Mermaid flowchart syntax.
            path = f"{call_hierarchy[i]} ---> {call_hierarchy[i+1]}"

            if path not in discovered_paths:
                # Logging with a prefix, so it is easy to filter out this information
                # from the log using the following command.
                # grep CALL_TRACE gdb.txt | cut -d: -f 2
                log(f"CALL_TRACE:{path}")
                new_paths_found = True
                discovered_paths.add(path)
            i = i + 1

        if not new_paths_found:
            event.breakpoint.delete()
        run_gdb_command("continue")


def configure_breakpoints():
    # The following didn't seem to add any breakpoints. May be it works only with regex for methods?
    # for b in gdb.rbreak('dict.c:.'):
    #     b.silent = True

    run_gdb_command('rbreak dict.c:.')
    run_gdb_command('rbreak db.c:.')
    for b in gdb.breakpoints():
        # Making the breakpoints silent will prevent it from printing the location
        # when the breakpoint is hit. This reduces the noise in the log.
        b.silent = True


def main():
    setup()
    configure_breakpoints()

    # Setup handler to run when breakpoint is hit
    gdb.events.stop.connect(stop_handler)


main()
