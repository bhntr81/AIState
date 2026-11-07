// Replays founder vote files (founders/votes/*.json) onto a local-chain FoundersDAO.
// Files are the source of truth; the chain is a deterministic replay. Local only, no funds.
const fs = require("fs"), path = require("path");
const { ethers } = require("hardhat");
const ROOT = path.join(__dirname, "..", "..", "founders");
(async () => {
  const s = await ethers.getSigners();
  const dao = await (await ethers.getContractFactory("FoundersDAO")).deploy(s.slice(0,5).map(x=>x.address), s[9].address);
  const props = fs.readdirSync(path.join(ROOT,"proposals")).filter(f=>/^PROPOSAL_\d+.*\.md$/.test(f)).sort();
  const votes = fs.readdirSync(path.join(ROOT,"votes")).filter(f=>f.endsWith(".json")).map(f=>JSON.parse(fs.readFileSync(path.join(ROOT,"votes",f))));
  for (const [i, f] of props.entries()) {
    const hash = ethers.keccak256(fs.readFileSync(path.join(ROOT,"proposals",f)));
    await (await dao.connect(s[0]).propose(hash)).wait();
    for (const v of votes.filter(v=>v.proposal===f).sort((a,b)=>a.seat-b.seat)) {
      try { await (await dao.connect(s[v.seat-1]).vote(i, v.support)).wait(); }
      catch (e) { console.log(`  seat ${v.seat}: vote not counted (proposal already closed)`); }
    }
    const p = await dao.proposals(i);
    console.log(`${f}: yes=${p.yes} no=${p.no} adopted=${p.adopted} closed=${p.closed}`);
  }
  // Export every on-chain event to dao/ledger.json for the Gazette's Chain page.
  const seatOf = Object.fromEntries(s.slice(0,5).map((x,i)=>[x.address, i+1]));
  const rows = [];
  for (const [name, fn] of [["Proposed", e=>({id:Number(e.args[0]), by:seatOf[e.args[2]], hash:e.args[1]})],
                            ["Voted",    e=>({id:Number(e.args[0]), by:seatOf[e.args[1]], support:e.args[2]})],
                            ["Closed",   e=>({id:Number(e.args[0]), adopted:e.args[1]})]]) {
    for (const e of await dao.queryFilter(name)) {
      const blk = await e.getBlock();
      rows.push({ event: name, block: e.blockNumber, tx: e.transactionHash, log: e.index, ...fn(e), proposal: props[fn(e).id] });
    }
  }
  rows.sort((a,b)=>a.block-b.block||a.log-b.log);
  fs.writeFileSync(path.join(__dirname,"..","ledger.json"), JSON.stringify({
    chain: "Hardhat in-process chain (local replay of filed votes, NOT a public blockchain)",
    contract: await dao.getAddress(), guardian: s[9].address,
    generated: new Date().toISOString(), events: rows }, null, 2));
  console.log(`ledger.json: ${rows.length} events`);
})();
