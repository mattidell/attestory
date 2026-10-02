#!/usr/bin/env node
// Browser regressions for the Track 6b saved reader. Input comes only from the
// three generated presentation.json files; the script does not run the engine.
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { startLoopbackServer } from "../lib/server.mjs";
import { launchChrome } from "../lib/chrome.mjs";
import { CDPClient } from "../lib/cdp.mjs";

const root = process.cwd();
const options = { page: "tools/presentation_harness/examples/pages/statement-calculation.experimental.v1.html", outputDir: "temp/track6b/reader-repair" };
for (let i = 2; i < process.argv.length; i += 1) {
  if (process.argv[i] === "--page") options.page = process.argv[++i];
  else if (process.argv[i] === "--output-dir") options.outputDir = process.argv[++i];
  else throw new Error(`unknown option ${process.argv[i]}`);
}
if (resolve(root, options.page).startsWith(resolve(root) + "/") === false) throw new Error("page must be repository-relative");
if (!options.outputDir.startsWith("temp/track6b/")) throw new Error("output must remain under ignored temp/track6b");
const page = options.page;
const cases = ["ordinary", "adverse", "unresolved"];
const fixtures = cases.map((name) => `temp/track6b/${name}/presentation.json`);
const allowed = new Set([page, ...fixtures]);
const failures = [];
const observations = {};
const check = (name, pass, actual = undefined, expected = undefined) => {
  if (!pass) failures.push({ name, actual, expected });
};
function compareRecord(caseName, label, record, rendered) {
  const actual = rendered[label] || {};
  const fields = [
    ["ruleId", "Producer"], ["ruleVersion", "Producer version"], ["readerRole", "Reader role"],
    ["disposition", "Original disposition"], ["interpretation", "Interpretation"], ["findingId", "Finding"],
    ["factId", "Fact identity"], ["claimType", "Claim fact type"], ["claimTypeVersion", "Claim fact type version"],
    ["suppliedFindingId", "Supplied finding"], ["suppliedValue", "Supplied value"], ["symbol", "Subject symbol"],
    ["value", "Recorded value"], ["basisOrigin", "Basis origin"], ["id", "Parameter"], ["version", "Parameter version"],
    ["consumerRuleId", "Consumer rule"], ["consumerFindingId", "Consumer finding"], ["code", "Code"], ["wording", "Published rule wording"], ["lineNote", "Published rule-stated basis"],
  ];
  for (const [key, title] of fields) {
    const expected = Object.prototype.hasOwnProperty.call(record || {}, key) ? (record[key] == null ? "not recorded" : String(record[key])) : undefined;
    if (expected !== undefined) check(`${caseName}: ${label} ${title} matches saved row`, actual[title] === expected, { actual: actual[title], expected });
  }
  const pins = record && Array.isArray(record.pins) ? JSON.stringify(record.pins) : "not recorded";
  const missing = record && Array.isArray(record.missing) ? JSON.stringify(record.missing) : "not recorded";
  check(`${caseName}: ${label} pins match saved row`, actual.Pins === pins, { actual: actual.Pins, expected: pins });
  check(`${caseName}: ${label} missing entries match saved row`, actual["Missing entries"] === missing, { actual: actual["Missing entries"], expected: missing });
}
const server = await startLoopbackServer(root, allowed);
const chrome = await launchChrome();
const client = await CDPClient.connect(chrome.wsUrl);
try {
  for (const name of cases) {
    const target = await client.send("Target.createTarget", { url: "about:blank" });
    const { sessionId } = await client.send("Target.attachToTarget", { targetId: target.targetId, flatten: true });
    await client.send("Page.enable", {}, sessionId);
    await client.send("Emulation.setDeviceMetricsOverride", { width: 1400, height: 1200, deviceScaleFactor: 1, mobile: false }, sessionId);
    const fixture = `temp/track6b/${name}/presentation.json`;
    const saved = JSON.parse(await readFile(resolve(root, fixture), "utf8"));
    const load = client.waitFor("Page.loadEventFired", sessionId, 10000);
    await client.send("Page.navigate", { url: `${server.origin}/${page}?fixture=${fixture}` }, sessionId);
    await load;
    await client.send("Page.bringToFront", {}, sessionId);
    const currentGroup = saved.calculationView.groups.find((g) => g.statementLabel.statement === "S1");
    const currentS2 = saved.calculationView.groups.find((g) => g.statementLabel.statement === "S2");
    const result = await client.send("Runtime.evaluate", {
      expression: `JSON.stringify((() => {
        const s1 = document.querySelector('#statement-S1');
        const s2 = document.querySelector('#statement-S2');
          const text = (selector, root = s1) => root?.querySelector(selector)?.innerText || '';
        return {
          categories: [...(s1?.querySelectorAll('.reader-category h3') || [])].map(x => x.innerText),
          supplied: text('.axis-supplied'), assumptions: text('.axis-assumed'), conclusion: text('.axis-concluded'), responsibility: text('.axis-responsibility'),
          suppliedText: text('.axis-supplied'), technicalSourceTitleVisible: ${JSON.stringify(currentGroup.sourceFindings.map((source) => source.factTypeTitle))}.some(title => text('.axis-supplied').includes(title)),
          s1Amount: text('.statement-amount'), s2Amount: text('.statement-amount', s2), ruleBasis: text('.rule-basis'),
          s1Wording: [...(s1?.querySelectorAll('.wording') || [])].map(x => x.textContent), s1Note: text('.rule-basis'),
          s2Wording: [...(s2?.querySelectorAll('.wording') || [])].map(x => x.textContent), s2Note: text('.rule-basis', s2),
          s2Reading: { supplied: text('.axis-supplied', s2), assumptions: text('.axis-assumed', s2), conclusion: text('.axis-concluded', s2), responsibility: text('.axis-responsibility', s2) },
          worksheet: document.querySelector('#worksheet-result')?.textContent || '',
          detailsBefore: [...(s1?.querySelectorAll('details.reader-evidence') || [])].map(x => ({ open: x.open, summary: x.querySelector('summary')?.textContent, body: x.querySelector('.evidence-json')?.textContent || '' })),
          sourceDetails: [...(s1?.querySelectorAll('details.technical-source') || [])].map(details => Object.fromEntries([...(details.querySelectorAll('dt')||[])].map(dt=>[dt.textContent,dt.nextElementSibling?.textContent||'']))),
          sourceDetailText: [...(s1?.querySelectorAll('details.technical-source') || [])].map(x=>x.textContent),
          answer: text('.answer'),
          disclosures: [...(s1?.querySelectorAll('details.reader-evidence') || [])].length
        };
      })())`,
      returnByValue: true,
    }, sessionId);
    const observed = JSON.parse(result.result.value);
    observations[name] = observed;
    await mkdir(options.outputDir, { recursive: true });
    const collapsed = await client.send("Page.captureScreenshot", { format: "png", captureBeyondViewport: false }, sessionId);
    await writeFile(`${options.outputDir}/${name}-collapsed.png`, Buffer.from(collapsed.data, "base64"));
    check(`${name}: all four distinct categories`, JSON.stringify(observed.categories) === JSON.stringify([
      "What was supplied", "What the calculation assumed", "What the rules concluded", "What remains the filer’s responsibility",
    ]), observed.categories);
    check(`${name}: no technical source description in supplied reading`, !observed.technicalSourceTitleVisible);
    check(`${name}: worksheet is separate and equals saved line21`, observed.worksheet === String(saved.sections.find((s) => s.id === "line-sch1-21").resolved.value), observed.worksheet);
    const s1 = saved.calculationView.groups.find((g) => g.statementLabel.statement === "S1");
    const s2 = saved.calculationView.groups.find((g) => g.statementLabel.statement === "S2");
    check(`${name}: S1 supplied source values visible`, s1.sourceFindings.every((source) => observed.supplied.includes(String(source.value))), observed.supplied);
    check(`${name}: source disclosure preserves recorded identities and technical titles`, s1.sourceFindings.every((source,index) => observed.sourceDetails[index]?.Finding===source.findingId && observed.sourceDetails[index]?.["Fact identity"]===source.factId && observed.sourceDetails[index]?.["Fact type"]===source.factTypeId && observed.sourceDetails[index]?.["Technical description"]===source.factTypeTitle), observed.sourceDetails);
    check(`${name}: assumptions exclude derived results and source pins`, !/intermediate findings|demo\.rule\.|student-loan-interest\|/.test(observed.assumptions), observed.assumptions);
    check(`${name}: evidence disclosures exist`, observed.disclosures >= 1, observed.disclosures);
    if (name === "ordinary") {
      check("ordinary: result explanation says supplied amount was retained", /retains the supplied amount/i.test(observed.answer), observed.answer);
      check("ordinary: copied lineNote is a rule basis, separate from responsibilities", observed.ruleBasis === `Recorded rule basis: ${s1.lineNote}` && !observed.responsibility.includes(s1.lineNote), observed.ruleBasis);
      check("ordinary: responsibility wording is copied from saved rows", JSON.stringify(observed.s1Wording) === JSON.stringify(s1.responsibilities.map((r) => r.wording)), observed.s1Wording);
    } else if (name === "adverse") {
      check("adverse: result explanation names synthetic whole-amount treatment", /synthetic whole-amount (?:rule|treatment)/i.test(observed.answer) && /calculated amount is 0/i.test(observed.answer), observed.answer);
      check("adverse: inapplicable treatment has no responsibility wording or note", observed.s1Wording.length === 0 && observed.s1Note === "", { wording: observed.s1Wording, note: observed.s1Note });
    } else {
      check("unresolved: explanation says classification could not be resolved and amount is unavailable", /claim could not be classified/i.test(observed.answer) && /amount is unavailable/i.test(observed.answer) && !/missing (?:school|fact|claim|document)/i.test(observed.answer) && !/DEPENDENCY_INVALID/.test(observed.answer), observed.answer);
      check("unresolved: blocked treatment has no responsibility wording or note", observed.s1Wording.length === 0 && observed.s1Note === "", { wording: observed.s1Wording, note: observed.s1Note });
    }

    // Open the first technical evidence disclosure with the keyboard and keep
    // checking after it is exposed, rather than trusting hidden textContent.
    let reachedEvidence = false;
    for (let attempt = 0; attempt < 10; attempt += 1) {
      await client.send("Input.dispatchKeyEvent", { type: "rawKeyDown", key: "Tab", code: "Tab", windowsVirtualKeyCode: 9, nativeVirtualKeyCode: 9 }, sessionId);
      await client.send("Input.dispatchKeyEvent", { type: "keyUp", key: "Tab", code: "Tab", windowsVirtualKeyCode: 9 }, sessionId);
      const active = await client.send("Runtime.evaluate", { expression: `!!document.activeElement?.matches('#statement-S1 details.reader-evidence > summary')`, returnByValue: true }, sessionId);
      if (active.result.value === true) { reachedEvidence = true; break; }
    }
    check(`${name}: Tab traversal reaches evidence summary`, reachedEvidence);
    await client.send("Input.dispatchKeyEvent", { type: "keyDown", key: " ", code: "Space", windowsVirtualKeyCode: 32, nativeVirtualKeyCode: 32, text: " " }, sessionId);
    await client.send("Input.dispatchKeyEvent", { type: "char", key: " ", code: "Space", text: " " }, sessionId);
    await client.send("Input.dispatchKeyEvent", { type: "keyUp", key: " ", code: "Space", windowsVirtualKeyCode: 32 }, sessionId);
    const opened = await client.send("Runtime.evaluate", { expression: `JSON.stringify({open:!!document.querySelector('#statement-S1 details.reader-evidence')?.open,visible:!!document.querySelector('#statement-S1 details.reader-evidence .evidence-content')?.getClientRects().length,body:document.querySelector('#statement-S1 details.reader-evidence .evidence-json')?.textContent||'',blocks:[...(document.querySelectorAll('#statement-S1 details.reader-evidence .evidence-block')||[])].map(block=>({label:block.querySelector('h4')?.innerText||'',fields:[...(block.querySelectorAll('dt')||[])].map(dt=>[dt.innerText,dt.nextElementSibling?.innerText||''])}))})`, returnByValue: true }, sessionId);
    const evidence = JSON.parse(opened.result.value);
    check(`${name}: keyboard opens evidence disclosure`, evidence.open);
    check(`${name}: opened evidence is visible`, evidence.visible);
    const blocks = Object.fromEntries(evidence.blocks.map((block) => [block.label, Object.fromEntries(block.fields)]));
    if (name === "unresolved") {
      await client.send("Runtime.evaluate", { expression: `document.querySelector('#statement-S1 details.reader-evidence')?.scrollIntoView({block:'center'})`, returnByValue: true }, sessionId);
      const blockedCapture = await client.send("Page.captureScreenshot", { format: "png", captureBeyondViewport: false }, sessionId);
      await writeFile(`${options.outputDir}/unresolved-open-evidence.png`, Buffer.from(blockedCapture.data, "base64"));
    }
    const amountEvidence = { ruleId:s1.ruleId, ruleVersion:s1.ruleVersion, disposition:s1.disposition, findingId:s1.findingId, symbol:s1.symbol, value:s1.value, pins:s1.pins, code:s1.code, missing:s1.missing };
    compareRecord(name, "Statement amount", amountEvidence, blocks);
    for (const [title, axis] of [["Borrowing route",s1.statementOutcome.route],["Statement-wide scope",s1.statementOutcome.statementScope],["Statement conclusion",s1.statementOutcome.conclusion]]) {
      compareRecord(name, title, axis, blocks);
    }
    for (const [index, classifier] of (s1.statementOutcome.statementScope.claims || []).entries()) compareRecord(name, `Claim classifier ${index + 1}`, classifier, blocks);
    for (const [index, node] of (s1.nodes || []).entries()) compareRecord(name, `Intermediate finding ${index + 1}`, node, blocks);
    for (const [index, item] of (s1.responsibilities || []).entries()) compareRecord(name, `Published responsibility ${index + 1}`, item, blocks);
    for (const [index, item] of (s1.statementOutcome.responsibilityFailures || []).entries()) compareRecord(name, `Responsibility diagnostic ${index + 1}`, item, blocks);
    for (const [index, item] of (s1.assumptions || []).entries()) compareRecord(name, `Selected parameter ${index + 1}`, item, blocks);
    if (typeof s1.lineNote === "string") compareRecord(name, "Published rule-stated basis", {ruleId:s1.statementOutcome.conclusion.ruleId,ruleVersion:s1.statementOutcome.conclusion.ruleVersion,disposition:s1.statementOutcome.conclusion.disposition,lineNote:s1.lineNote}, blocks);
    const expectedClassifierCode = (s1.statementOutcome.statementScope.claims || []).find((claim) => claim.disposition === "blocked")?.code;
    check(`${name}: evidence includes axis identities, pins, and blocked details from saved model`, evidence.body.length > 0 && (name !== "unresolved" || (blocks["Claim classifier 1"]?.Code === expectedClassifierCode && blocks["Claim classifier 1"]?.["Missing entries"] === JSON.stringify((s1.statementOutcome.statementScope.claims || [])[0]?.missing || []))), evidence.body.slice(0, 250));
    const modelGroup = saved.calculationView.groups.find((g) => g.statementLabel.statement === "S1");
    const expectedEvidence = JSON.stringify({ amount: modelGroup, outcome: modelGroup.statementOutcome });
    let parsedEvidence;
    try { parsedEvidence = JSON.parse(evidence.body); } catch { parsedEvidence = null; }
    check(`${name}: disclosure preserves exact saved amount/axis/classifier evidence`, JSON.stringify(parsedEvidence) === expectedEvidence, evidence.body.slice(0, 160));
    // Tab from the first disclosure into its exact-JSON fidelity aid, then open
    // S2's own evidence disclosure without assigning focus by script.
    await client.send("Input.dispatchKeyEvent", { type: "rawKeyDown", key: "Tab", code: "Tab", windowsVirtualKeyCode: 9, nativeVirtualKeyCode: 9 }, sessionId);
    await client.send("Input.dispatchKeyEvent", { type: "keyUp", key: "Tab", code: "Tab", windowsVirtualKeyCode: 9 }, sessionId);
    const rawActive = await client.send("Runtime.evaluate", { expression: `!!document.activeElement?.matches('#statement-S1 details.raw-model-evidence > summary')`, returnByValue: true }, sessionId);
    check(`${name}: Tab reaches exact-model disclosure`, rawActive.result.value === true);
    await client.send("Input.dispatchKeyEvent", { type: "keyDown", key: " ", code: "Space", windowsVirtualKeyCode: 32, nativeVirtualKeyCode: 32, text: " " }, sessionId);
    await client.send("Input.dispatchKeyEvent", { type: "char", key: " ", code: "Space", text: " " }, sessionId);
    await client.send("Input.dispatchKeyEvent", { type: "keyUp", key: " ", code: "Space", windowsVirtualKeyCode: 32 }, sessionId);
    const rawVisible = await client.send("Runtime.evaluate", { expression: `!!document.querySelector('#statement-S1 details.raw-model-evidence')?.open && !!document.querySelector('#statement-S1 .evidence-json')?.getClientRects().length`, returnByValue: true }, sessionId);
    check(`${name}: exact saved model becomes visible after keyboard activation`, rawVisible.result.value === true);
    const s2Group = currentS2;
    const s2Tab = await client.send("Runtime.evaluate", { expression: `JSON.stringify({sourceValues:[...(document.querySelectorAll('#statement-S2 .source-value')||[])].map(x=>x.innerText), sourceDetails:[...(document.querySelectorAll('#statement-S2 details.technical-source')||[])].map(details=>Object.fromEntries([...(details.querySelectorAll('dt')||[])].map(dt=>[dt.textContent,dt.nextElementSibling?.textContent||'']))), plain:document.querySelector('#statement-S2')?.innerText||'', technicalTitleVisible:${JSON.stringify(s2Group.sourceFindings.map((source) => source.factTypeTitle))}.some(title=>document.querySelector('#statement-S2 .axis-supplied')?.innerText.includes(title)), evidenceCount:document.querySelectorAll('#statement-S2 details.reader-evidence .evidence-block').length})`, returnByValue: true }, sessionId);
    const s2Visible = JSON.parse(s2Tab.result.value);
    check(`${name}: S2 source values match its saved findings`, s2Group.sourceFindings.every((source) => s2Visible.sourceValues.includes(String(source.value))), s2Visible.sourceValues);
    check(`${name}: S2 source disclosure preserves identities/titles`, s2Group.sourceFindings.every((source,index) => s2Visible.sourceDetails[index]?.Finding===source.findingId && s2Visible.sourceDetails[index]?.["Fact identity"]===source.factId && s2Visible.sourceDetails[index]?.["Fact type"]===source.factTypeId && s2Visible.sourceDetails[index]?.["Technical description"]===source.factTypeTitle), s2Visible.sourceDetails);
    check(`${name}: S2 supplied reading hides technical type descriptions`, !s2Visible.technicalTitleVisible);
    check(`${name}: S2 reading has no S1 claim leakage`, !/vehicle|demo-untreated|S1 statement-wide/.test(s2Visible.plain));
    let reachedS2 = false;
    for (let attempt = 0; attempt < 10; attempt += 1) {
      await client.send("Input.dispatchKeyEvent", { type: "rawKeyDown", key: "Tab", code: "Tab", windowsVirtualKeyCode: 9, nativeVirtualKeyCode: 9 }, sessionId);
      await client.send("Input.dispatchKeyEvent", { type: "keyUp", key: "Tab", code: "Tab", windowsVirtualKeyCode: 9 }, sessionId);
      const active = await client.send("Runtime.evaluate", { expression: `!!document.activeElement?.matches('#statement-S2 details.reader-evidence > summary')`, returnByValue: true }, sessionId);
      if (active.result.value === true) { reachedS2 = true; break; }
    }
    check(`${name}: Tab traversal reaches S2 evidence summary`, reachedS2);
    await client.send("Input.dispatchKeyEvent", { type: "keyDown", key: " ", code: "Space", windowsVirtualKeyCode: 32, nativeVirtualKeyCode: 32, text: " " }, sessionId);
    await client.send("Input.dispatchKeyEvent", { type: "char", key: " ", code: "Space", text: " " }, sessionId);
    await client.send("Input.dispatchKeyEvent", { type: "keyUp", key: " ", code: "Space", windowsVirtualKeyCode: 32 }, sessionId);
    const s2EvidenceResult = await client.send("Runtime.evaluate", { expression: `JSON.stringify({open:!!document.querySelector('#statement-S2 details.reader-evidence')?.open,blocks:[...(document.querySelectorAll('#statement-S2 details.reader-evidence .evidence-block')||[])].map(block=>({label:block.querySelector('h4')?.innerText||'',fields:[...(block.querySelectorAll('dt')||[])].map(dt=>[dt.innerText,dt.nextElementSibling?.innerText||''])}))})`, returnByValue: true }, sessionId);
    const s2Evidence = JSON.parse(s2EvidenceResult.result.value);
    check(`${name}: S2 evidence opens with keyboard`, s2Evidence.open);
    const s2Blocks = Object.fromEntries(s2Evidence.blocks.map((block) => [block.label, Object.fromEntries(block.fields)]));
    compareRecord(name, "S2 amount", {ruleId:s2Group.ruleId,ruleVersion:s2Group.ruleVersion,disposition:s2Group.disposition,findingId:s2Group.findingId,symbol:s2Group.symbol,value:s2Group.value,pins:s2Group.pins,code:s2Group.code,missing:s2Group.missing}, {"S2 amount":s2Blocks["Statement amount"]});
    const s2CompareBlocks = { ...s2Blocks, ...Object.fromEntries(Object.entries(s2Blocks).map(([label, fields]) => [`S2 ${label}`, fields])) };
    for (const [title, axis] of [["Borrowing route",s2Group.statementOutcome.route],["Statement-wide scope",s2Group.statementOutcome.statementScope],["Statement conclusion",s2Group.statementOutcome.conclusion]]) compareRecord(name, `S2 ${title}`, axis, s2CompareBlocks);
    for (const [index, row] of (s2Group.nodes || []).entries()) compareRecord(name, `S2 Intermediate finding ${index+1}`, row, s2CompareBlocks);
    for (const [index, row] of (s2Group.responsibilities || []).entries()) compareRecord(name, `S2 Published responsibility ${index+1}`, row, s2CompareBlocks);
    for (const [index, row] of (s2Group.assumptions || []).entries()) compareRecord(name, `S2 Selected parameter ${index+1}`, row, s2CompareBlocks);
    if (typeof s2Group.lineNote === "string") compareRecord(name, "S2 Published rule-stated basis", {ruleId:s2Group.statementOutcome.conclusion.ruleId,ruleVersion:s2Group.statementOutcome.conclusion.ruleVersion,disposition:s2Group.statementOutcome.conclusion.disposition,lineNote:s2Group.lineNote}, s2CompareBlocks);
    observations[name].s2Evidence = JSON.stringify(s2Evidence.blocks);
    await client.send("Target.closeTarget", { targetId: target.targetId });
  }
  const baseS2 = [observations.ordinary.s2Amount, observations.ordinary.s2Wording, observations.ordinary.s2Note];
  for (const name of ["adverse", "unresolved"]) check(`${name}: S2 remains stable`, JSON.stringify([observations[name].s2Amount, observations[name].s2Wording, observations[name].s2Note]) === JSON.stringify(baseS2));
  for (const name of ["adverse", "unresolved"]) check(`${name}: S2 short readings and saved evidence remain stable`, JSON.stringify(observations[name].s2Reading) === JSON.stringify(observations.ordinary.s2Reading) && observations[name].s2Evidence === observations.ordinary.s2Evidence);
} finally {
  client._ws.close();
  await chrome.dispose();
  await server.close();
}
const report = { version: "track6b-reader-browser-check.v1", failures, observations };
await mkdir(options.outputDir, { recursive: true });
await writeFile(`${options.outputDir}/browser-check.json`, JSON.stringify(report, null, 2));
console.log(JSON.stringify({ passed: failures.length === 0, failureCount: failures.length, failures, observationPath: `${options.outputDir}/browser-check.json` }, null, 2));
if (failures.length) process.exitCode = 1;
