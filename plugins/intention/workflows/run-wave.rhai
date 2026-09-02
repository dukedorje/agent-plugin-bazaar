let meta = #{
    name: "run-wave",
    description: "One /run act wave: disjoint write nodes in parallel",
    when_to_use: "Campaign next is act and conductor.py wave has two or more nodes",
    phases: [ #{ title: "Act", detail: "one worker per disjoint write" } ],
};

if args == () { pause("verification", "Pass args.nodes — array of {id, packet}."); }
if args.nodes == () { pause("verification", "Pass args.nodes — array of {id, packet}."); }

let nodes = args.nodes;
if type_of(nodes) != "array" { pause("verification", "args.nodes must be an array."); }
if nodes.len() == 0 { pause("verification", "args.nodes must be non-empty."); }

phase("Act");
let jobs = [];
let ids = [];
for n in nodes {
    let nid = if n == () { "" } else { n.id };
    let pkt = if n == () { "" } else { n.packet };
    if nid == () || nid == "" { continue; }
    if pkt == () || pkt == "" { continue; }
    let prompt = "You are executing ONE act node. ";
    prompt += "Read plugins/intention/skills/act/SKILL.md from disk. ";
    prompt += "Packet file: ";
    prompt += pkt;
    prompt += ". Node: ";
    prompt += nid;
    prompt += ". The conductor already called take — do not take again. ";
    prompt += "Stay on HEAD. Do not isolate. Work only on constraints.paths. ";
    prompt += "Focused verify once. Write the signed result. Stop. Do not fold.";
    ids.push(nid);
    jobs.push(#{
        prompt: prompt,
        label: "act:" + nid,
        capability_mode: "execute",
        agent_type: "general-purpose",
    });
}
if jobs.len() == 0 { pause("verification", "No usable nodes in args.nodes."); }

let results = parallel(jobs);
let passed = 0;
let failed = 0;
let rows = [];
let i = 0;
for r in results {
    let ok = r != () && r.success;
    if ok { passed += 1; } else { failed += 1; }
    let nid = if i < ids.len() { ids[i] } else { "" };
    rows.push(#{ id: nid, success: ok });
    i += 1;
}
log(passed.to_string() + " passed / " + failed.to_string() + " failed");
complete(#{ nodes: rows, passed: passed, failed: failed, count: jobs.len() });
