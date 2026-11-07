// Publishes the nation's record to the chain: deploys FoundersDAO (seat keys sign their own votes),
// then files every proposal (hash of the filed document) and every vote from founders/votes/*.json.
// Idempotent: reads/writes dao/deployments/<network>.dao.json and skips what is already on chain.
//   npx hardhat run scripts/publish.js                      (local dry run)
//   npx hardhat run scripts/publish.js --network baseSepolia (public testnet; seat addresses need test ETH)
const fs = require("fs"), path = require("path");
const { ethers, network } = require("hardhat");
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
  const C = await ethers.getContractFactory("FoundersDAO");
  let dao;
  if (fs.existsSync(depFile)) dao = C.attach(JSON.parse(fs.readFileSync(depFile)).dao).connect(seats[0]);
  else {
    dao = await C.connect(seats[0]).deploy(seats.map(s => s.address), w.guardian.address); await dao.waitForDeployment();
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
  console.log("DAO at", await dao.getAddress(), "on", network.name);
})();
