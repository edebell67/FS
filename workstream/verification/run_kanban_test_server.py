import sys

sys.path.insert(0, r"C:\Users\edebe\eds\workstream")

import kanban_dashboard as kd


def main() -> None:
    server = kd.ThreadedHTTPServer(("127.0.0.1", 8091), kd.KanbanHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
