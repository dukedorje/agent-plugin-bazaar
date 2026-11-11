# State transition log

Append-only observations of a settled run. One JSON object per line in
[`transition-log.jsonl`](transition-log.jsonl). `transition_log.py --parse`
counts the edges. Those counts are the observed finite state machine. They
do not replace the legal commands in [`transitions.json`](transitions.json).

```json
{"v":1,"campaign":"mjolnir-mesh-70wk","change":"add-admin-canvas","from":"ready","verb":"act","to":"landed","open":["mjolnir-mesh-6sro"],"taken":true,"evidence":"add-admin-canvas — closed (a4053ca)"}
```

| Field | Meaning |
|---|---|
| `v` | Schema version. `1`. |
| `campaign` | Root bead, when the transcript names one. |
| `change` | Change id this step touched. Empty when the step is the whole campaign. |
| `from`, `verb`, `to` | The transition. `verb` is a command id from `transitions.json`. |
| `open` | Nodes still open after the loop settled. |
| `taken` | `false` when the harness refused the verb, as with "Do not fold". |
| `evidence` | The transcript or commit line this row came from. Duplicate evidence is not appended twice. |

A loop with several open nodes is a sequence of these rows. Change, then act,
then fold, then change on the next node is four rows. A refused fold is a row
with `"taken": false`, and the state does not move.

```bash
python3 plugins/intention/scripts/transition_log.py --observe < pane.txt
python3 plugins/intention/scripts/transition_log.py --parse
```
