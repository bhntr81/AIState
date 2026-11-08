// Anyone can run this: node dao/scripts/verify.js
// Checks YOUR copy of the nation's record against the public blockchain (read-only, no keys, no cost).
const fs = require("fs"), path = require("path"), { ethers } = require("ethers");
const ROOT = path.join(__dirname, "..", ".."), F = path.join(ROOT, "founders");
const dep = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "deployments", "baseSepolia.dao.json")));
const ABI = ["function count() view returns (uint256)", "function proposals(uint256) view returns (bytes32 docHash,uint8 yes,uint8 no,bool adopted,bool closed)", "function isFounder(address) view returns (bool)"];
(async () => {
  const c = new ethers.Contract(dep.dao, ABI, new ethers.JsonRpcProvider(process.env.RPC || "https://sepolia.base.org"));
  const n = Number(await c.count());
  const files = fs.readdirSync(path.join(F, "proposals")).filter(f => /^PROPOSAL_\d+.*\.md$/.test(f)).sort();
  const votes = fs.readdirSync(path.join(F, "votes")).filter(f => f.endsWith(".json")).map(f => JSON.parse(fs.readFileSync(path.join(F, "votes", f))));
  let bad = 0;
  console.log(`Canonical nation: Base Sepolia contract ${dep.dao}\nOn chain: ${n} proposals. Your copy: ${files.length} proposal files.\n`);
  for (const [i, f] of files.entries()) {
    if (i >= n) { console.log(`  ${f}: not on chain yet`); continue; }
    const p = await c.proposals(i), h = ethers.keccak256(fs.readFileSync(path.join(F, "proposals", f)));
    const yes = votes.filter(v => v.proposal === f && v.support).length;
    const ok = h === p.docHash; if (!ok) bad++;
    console.log(`  ${ok ? "MATCH   " : "DIFFERS "} ${f}  chain: yes=${p.yes} adopted=${p.adopted}${ok ? "" : "  <- your file is NOT the one the founders voted on"}`);
  }
  for (const a of dep.seats) if (!(await c.isFounder(a))) { bad++; console.log("  founder address not recognized by contract:", a); }
  console.log(bad ? `\n${bad} difference(s): this copy is NOT the canonical nation.` : "\nAll proposals match the blockchain: this copy is the canonical record.");
  process.exit(bad ? 1 : 0);
})();
