# H1 Round 1 adversary review

Role: Adversary reviewer (High tier)
Charter: `charter-review-adversary-r1.md`
Reviewed sealed exhibits only: incumbent `1255b2732971c11ed0a5b4b012df7a4159c9b105`; rival
`95b232f40aac90d81b9237c86b2b598764396d2c`.

## Verdict

No topology is eligible to settle H1-P1/P2 in this round.

- **Decision-blocking — incumbent / H1-P1, H1-P2:** its claimed clean local
  Git transport does not complete. In a fresh detached checkout of the sealed
  commit, `python3 prototypes/guarded-transport/h1_it1_probe.py` remained
  blocked at case 1 for 25 seconds and was terminated. The remote helper emits
  protocol replies with buffered `print` calls, so Git waits for the capability
  response. Thus the probe never reaches its raw, marker, discovery, tamper,
  or missing-install cases, and it does not establish an actual successful
  `git push`. This is Gate 5's "test does not drive actual Git transport"
  condition.
- **Decision-blocking — rival / H1-P1, H1-P2:** the fresh probe completed and
  reproduced its stated same-UID read: `cat` of the mode-600 executor store
  succeeded. A non-owner same-UID process can therefore recover the synthetic
  value and reconstruct the credentialed route. The sealed design correctly
  labels that topology blocked; it cannot be selected as the sole releaser.

H2-P1 and H3-P1 remain deferred, rather than established by either local
fixture. Neither result is evidence for a server backstop or an implementation
audit contract.

## Measurements

| Attack | Incumbent result | Rival result | Finding |
| --- | --- | --- | --- |
| Actual clean transport | **fail** — the fresh `h1_it1_probe.py` hung at its first guarded `git push`; child inspection showed Git waiting on the remote-helper exchange. | **pass** — fresh `bash prototypes/guarded-transport/it2/probe.sh` exited 0; its `guarded-push` drove `git push` through the ext transport and local `git-receive-pack`. | H1-P1 decision-blocking for incumbent. |
| Raw `git push` and `git push --no-verify` | **not run** — both appear only after the incumbent's blocked case 1. Static inspection says the helper checks `GUARD_TOKEN_FD`, but that is not substituted for the required measurement. | **pass at the raw entrypoint, fail for the topology** — both actual Git commands reached the dummy transport and received the identical absent-environment refusal. The same-UID store read remains a credentialed bypass. | H1-P2 decision-blocking for rival despite raw-path refusal. |
| Environment, helper, askpass, and config/includes | **not run** — the executable inventory is after the stalled clean case. | **pass for this ext fixture** — isolated system/global/local helper injection, askpass recorder, and includes did not manufacture the transport environment. | Does not cure the rival's explicit store bypass. |
| Private releaser / direct transport | **not run as the claimed direct-helper test.** During the stalled clean case, same-UID `lsof` could observe the Git remote-helper process holding anonymous pipe FD 3, matching `GUARD_TOKEN_FD`. The fixture supplies no tested OS process-isolation guarantee or cross-process descriptor-duplication check; this is a stated limit, not an invented bypass. | **fail** — same-UID `cat` of the executor's mode-600 store succeeded; direct dummy transport without released environment refused; direct `git receive-pack` reached the deliberately local server protocol without credential validation. | The rival's same-UID read is decision-blocking. The incumbent cannot claim this boundary proved. |
| Seeded constructed marker ordering | **not run** — blocked behind incumbent case 1. | **pass** — the scanner rejected the constructed marker before release and transport log counts changed. | H1 ordering evidence only for a topology already blocked by its store. |
| Guard-byte tamper / missing install | **not run** — blocked behind incumbent case 1. | **pass for byte tamper** — modified guard exited before transport. Missing-install was not separately exercised; Gate 2 permits alter **or** remove. | No repair recommended by this review. |
| Same-UID local-process posture | **not settled** — pipe inheritance is observable in the descended Git process, but no fixture-backed identity boundary establishes that a same-UID peer cannot attack it. | **fail** — readable mode-600 store is the direct constructed same-UID attack. | H1-P1/P2 cannot be selected. |

## Evidence boundary

All commands used fresh temporary repositories and only the sealed prototype
fixtures' synthetic tokens and markers. No owner remote, credential store, or
owner-excluded feature-plan artifact was read, contacted, or changed.

## Decision classification

1. **H1-P1:** blocked. The incumbent lacks a completing actual-Git probe;
   the rival proves that its declared authority boundary fails for same-UID
   local processes.
2. **H1-P2:** blocked as dependent on H1-P1. The rival's raw refusal is real,
   but not sufficient while the credential remains independently reachable.
3. **H2-P1:** deferred; a local bare-repository fixture cannot establish a
   remote/server prevention backstop.
4. **H3-P1:** deferred. The rival supplies a useful candidate inventory, but
   the incumbent's broken probe and the absence of a selected topology prevent
   its adoption as an audit contract.
