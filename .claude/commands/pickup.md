---
description: Orient to a chartered builder or reviewer unit from git (launch names role and charter; no paste)
---

Pick up the chartered unit using the protocol in `AGENTS.md` ("Which seat are
you"). That section governs; this command only invokes it. The launch prompt
names your role and charter (and `--clean-room` for a rival round):

```sh
python3 tools/build_orientation_block.py --ref HEAD --role <builder|reviewer> --charter <path>
```

Verify the printed commit SHA against Git, adopt the role's seat file
(`docs/roles/<role>.md`), echo back your understood scope / evidence-rung
ceiling / stop conditions, then act within scope. If the launch named no
charter, stop and ask for it.

Do not ask the owner to paste context.
