import pytest

from api.app import create_app

@pytest.fixture(scope="function")
def app():
    from api.app import mongo_client

    def _load_collections_and_indexes():
        from api.application_layer.adapter.persistency.collections import (
            collections_definitions,
        )

        for definition in collections_definitions:
            collection = mongo_client.db.create_collection(name=definition.name)
            collection.create_index(definition.index, unique=definition.unique_index)

    app = create_app("Testing")
    app.config["TESTING"] = True
    client = app.test_client()

    _load_collections_and_indexes()

    with app.app_context():
        yield client
