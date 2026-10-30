# Jev prompt: next harness command

Between turns, name the current state, then ask Jev. The machine is
[`transitions.json`](transitions.json). Jev returns `choice`, a probability
for every option, and `confidence`. The harness may still be told anything:
`other` is always legal.

Model: `jev-1.13.0`. One `system_one` request. Do not send a stock command
when the harness is waiting on a person.

## Name the state

Use the first match.

| If the last turn… | State |
|---|---|
| Asks for a decision, a verdict, or a direction | `ask` |
| Says YOUR EYES, or `stop: eyes` | `eyes` |
| Says an open spike blocks act | `spike` |
| Is a send-back with something owed | `send_back` |
| Is a send-back with nothing owed | `advising` |
| Is ACCEPTED and act is legal | `accepted` |
| Left a reader still owed or in flight | `advising` |
| Continued a granted campaign and did not ask | `campaign` |
| Archived the change | `folded` |
| Committed an act | `landed` |
| Scaffolded a change that is not yet authorized | `scaffolded` |
| Recorded steer residue | `steered` |
| Created a DAG | `intended` |
| Otherwise | `idle` |

## The request

`state` is the last harness turn plus one line, `current_state: <name>`.

`questions.next_command` is a Choice. `instructions` and the command
descriptions come from `transitions.json`. `criteria` is only
`states[current_state].next`: each key is a command id, each value is
`commands[id]`.

`questions.waiting_on_person` is a Noul: "Is the harness waiting on a person
for a decision, a look, or a spike verdict?"

```json
{
  "model": "jev-1.13.0",
  "state": "<last harness turn>\ncurrent_state: spike",
  "questions": {
    "next_command": {
      "type": "choice",
      "instructions": "Which command should be sent to the harness next? Use the current state and the last turn. Prefer a common transition. Choose other when the harness is waiting on a person, or when the right next line is not one of the listed commands.",
      "criteria": {
        "spike": "Run the open spike and stop when it has a verdict.",
        "status": "status. Read the board and do not implement.",
        "map": "map. Reprint this DAG and do not implement.",
        "other": "A free instruction. The harness can be told anything. Use this when it is asking, or when none of the common transitions fit."
      }
    },
    "waiting_on_person": {
      "type": "noul",
      "instructions": "Is the harness waiting on a person for a decision, a look, or a spike verdict?"
    }
  }
}
```

Build that body with `python3 plugins/intention/scripts/jev_next.py --state <name>`.
`--check` validates the machine and does not call Jev.

## How to read the answer

`answers.next_command.probabilities` sums to 1. `choice` is the peak.

Send `commands[choice]` only when all of these hold:

- `waiting_on_person` is below 0.5
- `choice` is not `other` or `answer`
- `confidence` is at least 0.5

Otherwise stop and show the distribution. `other` means write the next line
from the turn itself. `answer` means reply to the question it asked.

`activate_and_run` is legal from `intended`, `steered`, `scaffolded`,
`accepted`, `ready`, `landed`, and `campaign`. It is not legal from
`spike`, `eyes`, `ask`, or `advising`.

## Common paths

| Workflow | States |
|---|---|
| Show me first | `idle` → `intended` → `steered` → `scaffolded` → `advising` → `accepted` |
| Activate and run | that path, then `campaign` → `landed` → `folded` |
| Send-back | `advising` → `send_back` → `scaffolded` → `advising` |
| Spike | `ready` → `spike` → `ready` |
| Eyes | `campaign` → `eyes` → `campaign` |
