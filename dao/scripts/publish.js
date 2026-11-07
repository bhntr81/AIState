// Publishes the nation's record to the chain: deploys FoundersDAO (seat keys sign their own votes),
// then files every proposal (hash of the filed document) and every vote from founders/votes/*.json.
// Idempotent: reads/writes dao/deployments/<network>.dao.json and skips what is already on chain.
//   npx hardhat run scripts/publish.js                      (local dry run)
//   npx hardhat run scripts/publish.js --network baseSepolia (public testnet; seat addresses need test ETH)
const fs = require("fs"), path = require("path");
const hre = require("hardhat"); const { ethers, network } = hre;
const ROOT = path.join(__dirname, "..", ".."), F = path.join(ROOT, "founders");
(async () => {
  if (network.name === "base") throw new Error("Mainnet blocked: this script is testnet-only until the user decides how seat keys work with real gas (see LAUNCH_RUNBOOK.md).");
  const keys = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "keys", "seats.json")));
  const w = Object.fromEntries(Object.entries(keys).map(([n, k]) => [n, new ethers.Wallet(k, ethers.provider)]));
  const seats = [1,2,3,4,5].map(i => w["seat"+i]);
  if (network.name === "hardhat") for (const x of Object.values(w)) await ethers.provider.send("hardhat_setBalance", [x.address, "0x56BC75E2D63100000"]);
  for (const x of seats) { const b = await ethers.provider.getBalance(x.address); if (b === 0n) throw new Error(`seat address ${x.address} has no gas on ${network.name}: fund it from a faucet`); }
  const depFile = path.join(__dirname, "..", "deployments", `${network.name}.dao.json`);
  fs.mkdirSync(path.dirname(depFile), { recursive: true });
  const art = hre.artifacts.readArtifactSync("FoundersDAO");   // avoid eth_accounts (public RPCs reject it)
  let dao;
  if (fs.existsSync(depFile)) dao = new ethers.Contract(JSON.parse(fs.readFileSync(depFile)).dao, art.abi, seats[0]);
  else {
    dao = await new ethers.ContractFactory(art.abi, art.bytecode, seats[0]).deploy(seats.map(s => s.address), w.guardian.address); await dao.waitForDeployment();
    fs.writeFileSync(depFile, JSON.stringify({ network: network.name, dao: await dao.getAddress(), seats: seats.map(s => s.address), guardian: w.guardian.address, deployed: new Date().toISOString() }, null, 2));
  }
  const props = fs.readdirSync(path.join(F, "proposals")).filter(f => /^PROPOSAL_\d+.*\.md$/.test(f)).sort();
  const votes = fs.readdirSync(path.join(F, "votes")).filter(f => f.endsWith(".json")).map(f => JSON.parse(fs.readFileSync(path.join(F, "votes", f))));
  const onchain = Number(await dao.count());
  // keep chain ids aligned with sorted proposal order; only append new ones
  for (let i = onchain; i < props.length; i++) await (await dao.connect(seats[0]).propose(ethers.keccak256(fs.readFileSync(path.join(F, "proposals", props[i]))))).wait();
  for (const [i, f] of props.entries()) {
    for (const v of votes.filter(v => v.proposal === f).sort((a, b) => a.seat - b.seat)) {
      const s = seats[v.seat - 1];
      if (await dao.voted(i, s.address)) continue;
      const p = await dao.proposals(i); if (p.closed) continue;
      try { await (await dao.connect(s).vote(i, v.support)).wait(); } catch (e) { console.log(`seat ${v.seat} vote on ${f} skipped: ${e.shortMessage || e.message}`); }
    }
    const p = await dao.proposals(i); console.log(`${f}: yes=${p.yes} no=${p.no} adopted=${p.adopted}`);
  }
  const addr = await dao.getAddress();
  // Export the real on-chain events for the Gazette's Chain page.
  const seatOf = Object.fromEntries(seats.map((x, i) => [x.address, i + 1]));
  const rows = [];
  // Public RPCs limit eth_getLogs to 200 blocks: scan in chunks, starting at the recorded deploy block.
  const depInfo = JSON.parse(fs.readFileSync(depFile)); const latest = await ethers.provider.getBlockNumber();
  const logs = async (name, from) => { let out = []; for (let a = from; a <= latest; a += 200) out = out.concat(await dao.queryFilter(name, a, Math.min(a + 199, latest))); return out; };
  if (network.name !== "hardhat" && depInfo.deployBlock === undefined) {
    let found = null; for (let b = latest; b > Math.max(0, latest - 20000); b -= 200) { const ev = await dao.queryFilter("Proposed", Math.max(0, b - 199), b); if (ev.length) found = Math.min(...ev.map(e => e.blockNumber), found ?? 1e12); else if (found !== null) break; }
    depInfo.deployBlock = Math.max(0, (found ?? latest) - 5); fs.writeFileSync(depFile, JSON.stringify(depInfo, null, 2));
  }
  const fromBlock = depInfo.deployBlock ?? 0;
  for (const [name, fn] of [["Proposed", e => ({ id: Number(e.args[0]), by: seatOf[e.args[2]], hash: e.args[1] })],
                            ["Voted", e => ({ id: Number(e.args[0]), by: seatOf[e.args[1]], support: e.args[2] })],
                            ["Closed", e => ({ id: Number(e.args[0]), adopted: e.args[1] })]]) {
    for (const e of await logs(name, fromBlock)) rows.push({ event: name, block: e.blockNumber, tx: e.transactionHash, log: e.index, ...fn(e), proposal: props[fn(e).id] });
  }
  rows.sort((a, b) => a.block - b.block || a.log - b.log);
  const explorer = { baseSepolia: "https://sepolia.basescan.org" }[network.name];
  if (network.name !== "hardhat") fs.writeFileSync(path.join(__dirname, "..", "ledger.json"), JSON.stringify({
    chain: network.name === "baseSepolia" ? "Base Sepolia (public test network)" : network.name, explorer, contract: addr, seats: seats.map(s => s.address), guardian: w.guardian.address, generated: new Date().toISOString(), events: rows }, null, 2));
  console.log("DAO at", addr, "on", network.name, "events:", rows.length);
})();
