from graph_api.database import test_connection


if test_connection():
    print("CognoDB connection successful!")
else:
    print("CognoDB connection failed!")