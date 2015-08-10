#### initial version

In the initial version the script is very simple.
It takes advantage of the fact that `MySQLdb.connect` method returns a connection object, which can act as context manager.
Benefits of this are that all error handling and transaction processing is done for us.

It also utilizes the standard's library `argparse` for handling command line arguments.
Since the script requires some parameters to set up connections, and they should not be hard coded, I chose to provide them as command line arguments.

Because one the requirements is to keep memory usage at a more or less constant level in spite of the size of the copied table I used the `cursor.fetchone`
to fetch one row at a time instead of `cursor.fetchall`, which would get the whole table at once and store it in memory.

In this version however all the queries are hard coded so the script isn't really very flexible, but does the job.

#### improved version

In this version I changed the way the script fetches data.
Insetad of fetching row by row it now fetches rows in batches. Batch size defaults to 1000 rows in one batch.
By timing the script on the test database table it showed some improvement.
Before the script completed in `~33s` after this improvement it comleted in `~9.5s`.
The script got also more flexible since it is possible to copy any table by providing it's name as the first positional argument to the script.
There are still some problems however. Main one is that `MySQLdb` does not provide interpolation of table names in query strings, thus forcing to use regular python string formatting which is not protected against SQL injection.
