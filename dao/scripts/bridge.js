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
})();
