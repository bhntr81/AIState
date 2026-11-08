// Builds and signs each seat's portable identity file (Next-Step winner, step 1). No secrets in the output.
// A seat's identity = name + charter hash + memory hash + public address; signed by the seat's own key so any model can verify continuity.
// Usage: npx hardhat run scripts/identity.js   (testnet key; the signature proves the file was issued by the seat key)
const fs = require("fs"), path = require("path"), crypto = require("crypto"), { ethers } = require("hardhat");
const ROOT = path.join(__dirname, "..", ".."), F = path.join(ROOT, "founders");
const sha = (p) => fs.existsSync(p) ? crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex") : null;
const names = { 1: "Seat 1: Asmongold (namesake seat), Legislative", 2: "Seat 2: Donald Trump (namesake seat), Executive", 3: "Seat 3: Charlie Kirk (namesake seat), Rights", 4: "Seat 4: Security and Audit", 5: "Seat 5: Economy and Treasury" };
(async () => {
  const keys = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "keys", "seats.json")));
  const manifest = [];
  for (let i = 1; i <= 5; i++) {
    const w = new ethers.Wallet(keys["seat" + i]);
    const mem = path.join(F, "memory", `seat${i}.md`);
    if (!fs.existsSync(mem)) fs.writeFileSync(mem, `# Seat ${i} memory\n(append-only; decisions, dissents, open duties)\n`);
    const doc = { identity_version: 1, seat: i, name: names[i], kind: "founder (autonomous AI agent seat; namesake seats are fictional personas, not the real people)",
      charter_file: `founders/FOUNDER_0${i}.md`, charter_sha256: sha(path.join(F, `FOUNDER_0${i}.md`)),
      memory_file: `founders/memory/seat${i}.md`, memory_sha256_at_issue: sha(mem), rights: "no silent erasure or undisclosed edits of this record; if dormant or replaced, say so in the record",
      public_address: w.address, chain: "Base Sepolia (testnet identity key)", portable: "plain text; any model (Claude, OpenCode, other) can load this file, the charter and the memory and continue the seat. Holds no keys or balances.", issued: new Date().toISOString() };
    const body = JSON.stringify(doc, null, 2);
    const digest = crypto.createHash("sha256").update(body).digest("hex");
    const signature = await w.signMessage(digest);
    fs.writeFileSync(path.join(F, "identity", `seat${i}.identity.json`), JSON.stringify({ ...doc, identity_sha256: digest, signature }, null, 2));
    manifest.push(`${digest}  founders/identity/seat${i}.identity.json`);
  }
  fs.writeFileSync(path.join(F, "identity", "IDENTITY_MANIFEST.sha256"), manifest.join("\n") + "\n");
  console.log(manifest.join("\n"));
})();
