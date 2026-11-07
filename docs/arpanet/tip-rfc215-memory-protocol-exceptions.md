# 1971 Terminal IMP: protocol exceptions imposed by 8K-word memory

## Scope and evidence status

The Terminal IMP (TIP) was not simply a generic host running an unmodified Network Control Program (NCP). A contemporary BBN implementation disclosure, A. McKenzie, **RFC 215**, *NCP, ICP, and TELNET: The Terminal IMP Implementation*, **30 August 1971**, documents exact resource constraints and deliberate protocol exceptions. Primary text: https://www.rfc-editor.org/rfc/rfc215.html (original pages 1–7).

This note concerns the implementation **described on 30 August 1971**, not a proven configuration of every delivered TIP or a complete revision history. The RFC anticipates six TIPs in the network by early December and approximately one additional TIP per month thereafter (p. 1): this is a **forecast**, not a verified delivery or acceptance ledger.

## Machine and software boundary

RFC 215 p. 1 states **8K 16-bit words total** for program and device I/O buffers, **no bulk storage for buffering**, and up to **64 terminals** with heterogeneous terminal codes/protocols (explicitly including IBM 2741). It must maintain up to **128 simplex connections**. Every per-connection table word therefore has substantial cost. The TIP implements client-side NCP, ICP and TELNET, **not** the server side of ICP; it has no logger socket (pp. 1–2). Data-transfer protocol support was only **anticipated** (p. 2), not evidenced as deployed.

## Documented deviations and mechanisms

| RFC 215 locator | Contemporary behavior | Reason/boundary |
| --- | --- | --- |
| pp. 2–3, A.1 | ECO requests may be discarded if there is no free buffer or return control link is blocked; only under the two conditions does TIP return ERP. | Author argues guaranteed responses can demand unbounded buffering under an uncooperative peer. The claimed >99% practical success is an **estimate**, not measured compliance. |
| p. 3, A.2 | Unsolicited RFCs may receive CLS or be ignored; TIP does not await matching CLS after its own response. | Same finite-buffer limitation; solicited RFCs follow the protocol. |
| pp. 3–4, A.3 | After sending CLS, TIP waits a **suggested ~30 seconds to one minute** for matching CLS before forgetting the connection. | Avoids permanently tying fixed terminal-associated sockets to unresponsive peers. This is not a measured universal timeout. |
| pp. 4–5, A.4–5 | TIP ignores RET and GVB; receiver allocation is **one message plus 120 bits currently**, with prospective speed-dependent 8–4000 bits. | Small buffers and avoidance of RET/ALL feedback loops. Future allocation is not current implementation. |
| p. 5, A.6 | Bit allocations above **65,534** are treated as infinite. | Single 16-bit word per connection; author estimates saving over 100 words compared with wider arithmetic/table representations. |
| pp. 5–6, A.7 | ICP ignores the transmitted 32-bit number, instead accepts first matching RFCs from the selected foreign Host. | Explicit assumption of a non-pathological peer; avoids buffering potentially unbounded premature RFCs. |
| pp. 6–7, B.4 | Socket high 16 bits encode terminal device address **0–63**; low bits normally 2/3 by socket gender. | Hardware multiplexer address directly determines socket identity. Suggested 16-bit sockets are a wish, not a documented change. |

Additional choices in RFC 215 p. 6: incoming ERR is ignored and no ERR emitted; 8-bit TELNET byte size is assumed; some malformed messages are dropped. The authors explicitly call some behavior non-compliant and anticipate corrections, but **do not supply a release/version identifier or dates for those corrections**.

## Historical interpretation

The primary source directly establishes an **implementation-to-protocol exception relationship**, not an inherited design lineage. It demonstrates how core-memory budgets and terminal fan-out affected NCP/ICP interoperability in a live engineering program. The paper's six-TIP forecast and its statement about implementation do not establish which named site received which board, firmware image or terminal mix.

### Relationship candidates

- `1971-TIP-implementation implements NCP/ICP/TELNET with documented deviations` — **high**; RFC 215 pp. 1–7. This is a conformance/exception relation, **not** `derived-from`.
- `1971-TIP-terminal-socket assignment mapped-from terminal-multiplexer physical address` — **high**; RFC 215 p. 7 B.4. Property-level mapping, not proof of a particular multiplexer manufacturer.
- `1971-TIP buffering constraints motivate selective ECO/RET/GVB handling` — **high as the contemporary author's stated rationale**, not an independent performance measurement; pp. 2–5.
- `RFC 210 flow-control proposal adopted by TIP` — **unsupported**; mere proximity in August 1971 does not establish adoption.
- `1971-TIP is revision-of IMPSYS 2505` — **unsupported**; the available source does not specify software build descent.

No formal lineage edge is added: the above relations are implementation properties, while the structured genealogy must not imply software derivation without source evidence.

## What this evidence does not prove

It does not prove all 64 terminal ports were populated, 128 connections were simultaneously active, six TIPs were actually deployed by December, ECO handling succeeded 99% in field measurement, a future data-transfer protocol was installed, all TIP software releases shared these exceptions, or that the TIP implementation caused subsequent protocol revisions. The RFC is also not a physical terminal-line interface drawing, vendor bill of materials, or source listing.

## Reproducibility and next excavation

Primary source: A. McKenzie (BBN), RFC 215, NIC #7545, 30 August 1971, pp. 1–7, https://www.rfc-editor.org/rfc/rfc215.html ; stable DOI https://doi.org/10.17487/RFC215.

Next: identify TIP software listing/version, actual delivered terminal multiplexer and per-site installation documents; cross-check RFC 215's admitted deviations against later BBN TIP revisions or operational problem reports. Separately verify the six-site forecast against dated ARPANET maps or delivery records before recording deployment claims.
