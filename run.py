from app import create_app
import threading
from app.services import run_import_data, refresh_cache

if __name__ == '__main__':
    app = create_app()

# Note: The following is implemented for concurrency using threading-caching, however due to SQLite database errors have been commented

    # Create a lock object
    # db_lock = threading.Lock()

    # Start the import data thread
    # t = threading.Thread(target=run_import_data, args=(db_lock,))
    # t.start()

    # Start the cache refresh thread
    # t2 = threading.Thread(target=refresh_cache, args=(db_lock,))
    # t2.start()
    # run_import_data(db_lock)


    # Run the Flask app
    app.run(debug=True)
