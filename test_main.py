import pandas as pd
from connect import connect, connect_single_query


def test_connect():
    # Prepare test data
    temp_table_file = './query/test_temp.sql'
    query_file = './query/test_query.sql'

    # Call the function under test
    result = connect(temp_table_file, query_file)

    # Perform assertions on the result
    assert isinstance(result, list)
    assert len(result) > 0
    for df in result:
        assert isinstance(df, pd.DataFrame)


def test_connect_single_query():
    # Prepare test data
    query = 'SELECT * FROM #test_table'

    # Call the function under test
    result = connect_single_query(query)

    # Perform assertions on the result
    assert isinstance(result, list)
    assert len(result) > 0
    for df in result:
        assert isinstance(df, pd.DataFrame)
