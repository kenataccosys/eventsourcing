from eventsourcing.infrastructure.stored_event_repos.with_cassandra import CassandraStoredEventRepository
from eventsourcing.infrastructure.cassandra import CassandraSettings, get_cassandra_connection_params, \
    setup_cassandra_connection, create_cassandra_keyspace_and_tables, drop_cassandra_keyspace
from eventsourcing.tests.unit_test_cases import AbstractTestCase


class CassandraTestCase(AbstractTestCase):

    def setUp(self):
        super(CassandraTestCase, self).setUp()
        create_cassandra_keyspace_and_tables()

    def tearDown(self):
        drop_cassandra_keyspace()
        # shutdown_cassandra_connection()
        super(CassandraTestCase, self).tearDown()


class CassandraRepoTestCase(CassandraTestCase):

    def setUp(self):
        setup_cassandra_connection(*get_cassandra_connection_params(CassandraSettings()))
        super(CassandraRepoTestCase, self).setUp()

    @property
    def stored_event_repo(self):
        try:
            return self._stored_event_repo
        except AttributeError:
            stored_event_repo = CassandraStoredEventRepository(
                always_write_entity_version=True,
                always_check_expected_version=True,
            )
            self._stored_event_repo = stored_event_repo
            return stored_event_repo
