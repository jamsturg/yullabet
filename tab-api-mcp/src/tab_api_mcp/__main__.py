"""Main entry point for the TAB API MCP package."""

import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "betting":
            # Run the betting server
            from .betting import main
            main()
        elif sys.argv[1] == "server":
            # Run the basic server
            from .server import main
            main()
        else:
            # Run the combined server by default
            from .combined import main
            main()
    else:
        # Run the combined server by default
        from .combined import main
        main()