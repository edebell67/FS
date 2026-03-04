import argparse
import json

p = argparse.ArgumentParser()
p.add_argument('--agent', required=True)
p.add_argument('--backlog_path', required=True)
args = p.parse_args()

tasks = {
    "tasks": [
        {
            "title": "Decompose backlog into implementation tasks",
            "summary": f"Generated for {args.agent} from {args.backlog_path}",
            "steps": [
                "Read backlog objective",
                "Split into actionable units",
                "Attach validation tests"
            ],
            "tests": [
                "Each generated task has a plan checklist",
                "Each generated task includes at least one validation test"
            ],
            "priority": 2
        },
        {
            "title": "Create traceability links",
            "summary": "Ensure generated tasks link back to source backlog id/path.",
            "steps": [
                "Add source references",
                "Confirm backlinks in generated markdown"
            ],
            "tests": [
                "Generated markdown contains Source backlog path",
                "Generated markdown contains Parent backlog id"
            ],
            "priority": 2
        }
    ]
}

print(json.dumps(tasks))
