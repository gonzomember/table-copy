from unittest import TestCase

import mock

import table_copy


class TableCopyTests(TestCase):
    """Perfoms tests for the table_copy script.
    """

    @mock.patch('table_copy.table_copy.copy_table')
    @mock.patch('table_copy.table_copy.make_parser')
    def test_main(self, make_parser, copy_table):
        """Check if when calling the `main` function everything gets called.
        """
        # first we set up what gets returned by `make_parse` function, it
        # should be an object that has a `parse_args` method which in turn
        # should return an object that has two properties `source` and `target`
        parsed_args = mock.Mock(table='table', source='source db',
                                target='target db', batch=4)
        make_parser.return_value.parse_args.return_value = parsed_args
        # then we invoke the function being tested and perform some checks
        table_copy.main()
        make_parser.assert_called_once_with()
        make_parser.return_value.parse_args.assert_called_once_with()
        copy_table.assert_called_once_with('table', 'source db',
                                           'target db', 4)

    def test_arg_parser_config(self):
        """Check if the parser works as expected.
        """
        parser = table_copy.make_parser()
        # it should raise an error when no arguments were provided
        self.assertRaises(SystemExit, parser.parse_args, [])
        # and parse them to two ilsts if they were provided
        source_args = ['--source', 'hosta', 'usera', 'passwda', 'dba']
        target_args = ['--target', 'hostb', 'userb', 'passwdb', 'dbb']
        parsed = parser.parse_args(['table'] + source_args + target_args)
        self.assertEqual(parsed.table, 'table')
        self.assertEqual(parsed.source, source_args[1:])
        self.assertEqual(parsed.target, target_args[1:])
        self.assertEqual(parsed.batch, 1000)

    @mock.patch('table_copy.table_copy.connect')
    def test_copy_table_db_connections_setup(self, connect):
        """Check whether two seperate db connections were made, and both used
        as context managers to handle transaction commit or rollback on errors.
        """
        # first we have to set up db connection objects that are returned by
        # `MySQLdb.connect` method.
        # those objects should provide all magic methods to support the
        # context manager protocol.
        source, target = mock.MagicMock(), mock.MagicMock()
        # we have to patch the fetchmany method on the cursor in order not to
        # get an infinite loop in the `while` loop
        source.__enter__.return_value.fetchmany.return_value = []
        connect.side_effect = [source, target]
        # we invoke the function being tested
        table_copy.copy_table('table', ['hosta', 'usera'],
                              ['hostb', 'userb'], 4)
        # check if the `connect` method was called twice with proper arguments
        self.assertEqual(connect.call_count, 2)
        self.assertEqual(connect.call_args_list,
                         [mock.call('hosta', 'usera'),
                          mock.call('hostb', 'userb')])
        # we also check if objects returned by those two `connect` calls were
        # used as context managers
        source.__enter__.assert_called_once_with()
        self.assertEqual(source.__exit__.call_count, 1)
        target.__enter__.assert_called_once_with()
        self.assertEqual(source.__exit__.call_count, 1)

    @mock.patch('table_copy.table_copy.connect')
    def test_copy_titles_query_execution(self, connect):
        """Check whether queries are executed properly.
        """
        select_query = 'select * from titles'
        insert_query = 'insert into titles values (%s, %s, %s, %s)'
        # again we have to set up mocked connections and cursors
        # `source_cursor` will pretend that it returned two rows
        source_cursor = mock.Mock(description=('column1', 'column2',
                                               'column3', 'column4'))
        source_cursor.fetchmany.side_effect = [['row1', 'row2'], []]
        target_cursor = mock.Mock()
        # our connection objects should return cursors when used as context
        # managers
        source, target = mock.MagicMock(), mock.MagicMock()
        source.__enter__.return_value = source_cursor
        target.__enter__.return_value = target_cursor
        # the connect functions should return both our connection objects
        # on subsequent calls
        connect.side_effect = [source, target]
        # invoke the function being tested and do some checks
        table_copy.copy_table('titles', [], [], 4)
        source_cursor.execute.assert_called_once_with(select_query)
        self.assertEqual(source_cursor.fetchmany.call_args_list,
                         [mock.call(4), mock.call(4)])
        self.assertEqual(target_cursor.executemany.call_count, 1)
        self.assertEqual(target_cursor.executemany.call_args_list,
                         [mock.call(insert_query, ['row1', 'row2'])])
