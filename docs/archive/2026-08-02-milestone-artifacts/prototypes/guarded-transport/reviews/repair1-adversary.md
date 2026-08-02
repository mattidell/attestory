# H1 Repair 1 adversary delta review

Role: Adversary reviewer (High tier)
Charter: `charter-repair1-adversary-review.md`
Reviewed sealed repair exhibit only:
`00d1550194b3b63b99312cfa63d2985f06d9c135`.

## Verdict

**Decision-blocking: Repair 1 does not yet establish H1-P1/P2.** The complete
fresh probe's clean guarded `git push` fails to complete. It was run from a
fresh detached checkout with:

```sh
python3 prototypes/guarded-transport/repair1/scan_before_release_probe.py
```

After 25 seconds it remained blocked in case 1's `git push` and was
terminated. A child-process check showed Git waiting in the remote-helper
exchange. The helper retains buffered `print` replies to Git's capability
protocol, so no successful actual transport, actual pushed update, or strict
clean-path event order was observed. Consequently raw and `--no-verify` were
not reached by the complete probe either.

The delta ordering checks that do not need the helper pass, but cannot repair
that core evidence failure.

## Attack measurements

| Attack | Result | Evidence and classification |
| --- | --- | --- |
| Clean guarded actual `git push` | **fail** | The complete fresh probe timed out at clean case 1 before it produced a receipt. This defeats the claimed proof that the guard's pre-scan update and Git's actual fixed-ref update agree. **Decision-blocking H1-P1.** |
| Raw `git push` / `--no-verify` | **not run** | These cases are after the clean-path deadlock. Static descriptor-absent checks are not a replacement for the charter's actual-Git measurement. **Decision-blocking H1-P2 as dependent on H1-P1.** |
| Constructed marker and release ordering | **pass** | An isolated execution of the sealed fixture's marker path returned direct-scan/guarded results `1/1`, with `0/0` descriptor creations/receipts. The constructed marker therefore refused before `os.pipe` or transport. |
| Guard-byte tamper | **pass** | An isolated execution returned exit `1`, with `0/0` descriptor creations/receipts. |
| Missing installation | **pass** | An isolated execution returned exit `1`, with `0/0` descriptor creations/receipts. |
| Environment, helper, askpass, system/global/local config, includes, and direct helper | **not fully run** | The sealed sibling inventory ran before the deadlock and reported pass for its own sanitized environment/config and direct helper launch. The complete raw cases and post-push persistence oracle were not reached, so the complete inventory is not independently established. |
| Descriptor observability | **limit found** | During the stalled clean case, a same-UID ordinary `lsof` inspection could observe the descended Git remote-helper process holding anonymous pipe FD 3. This did not demonstrate token recovery or descriptor duplication, so it is not an invented bypass; however it means the sibling's `/dev/fd` name check does not establish that descriptor metadata is unobservable. The H1/H3 inventory must describe this scoped process-inspection exclusion accurately. |
| Persistent artifacts | **not run** | The post-push oracle is after the blocked clean transport. No persistence conclusion is available from this delta run. |
| H2 server control | **pass at paper boundary** | The sentence names GitHub push protection, secret scanning, and branch protection as owner-attested residual controls and makes no local proof claim. |
| H3 E18.1/E18.2 | **pass at paper-contract boundary, conditional** | The named routes and desired event assertions are implementable by a later maintained battery. They cannot attest the selected topology until the clean actual-Git case completes; the descriptor-observability limitation should remain explicit. |

## Conclusion by proposition

1. **H1-P1:** blocked. The scan-before-pipe paths refuse correctly for the
   tested marker/tamper/missing cases, but the only clean actual-Git transport
   measurement hangs.
2. **H1-P2:** blocked. The required raw and bypass forms were not executed in
   the repaired complete probe.
3. **H2-P1:** acceptable only as the stated owner-attestation boundary; no
   local conclusion about remote controls is drawn.
4. **H3-P1:** the paper contract is usable as a Track 2 candidate, subject to
   correcting the observable-descriptor scope and first completing H1's clean
   transport evidence.

All work used fresh temporary repositories and synthetic fixture data only. No
owner remote, credential source, rejected rival, or owner-excluded feature
work was read, contacted, or changed.
