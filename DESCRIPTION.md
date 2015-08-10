#### initial version

In the initial version the script is very simple.
It takes advantage of the fact that `MySQLdb.connect` method returns a connection object, which can act as context manager.
Benefits of this are that all error handling and transaction processing is done for us.

It also utilizes the standard's library `argparse` for handling command line arguments.
Since the script requires some parameters to set up connections, and they should not be hard coded, I chose to provide them as command line arguments.

Because one the requirements is to keep memory usage at a more or less constant level in spite of the size of the copied table I used the `cursor.fetchone`
to fetch one row at a time instead of `cursor.fetchall`, which would get the whole table at once and store it in memory.

In this version however all the queries are hard coded so the script isn't really very flexible, but does the job.
