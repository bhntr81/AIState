// Generates 6 THROWAWAY keys (5 founder seats + 1 guardian) for TESTNETS ONLY. Writes dao/keys/seats.json (gitignored).
// Never use these for real money. Prints addresses only.
const fs = require("fs"), path = require("path"), { ethers } = require("hardhat");
const f = path.join(__dirname, "..", "keys", "seats.json");
if (fs.existsSync(f)) { console.log("keys exist; addresses:"); const k = JSON.parse(fs.readFileSync(f)); for (const [n, v] of Object.entries(k)) console.log(n, new ethers.Wallet(v).address); process.exit(0); }
const out = {}; for (const n of ["seat1","seat2","seat3","seat4","seat5","guardian"]) out[n] = ethers.Wallet.createRandom().privateKey;
fs.mkdirSync(path.dirname(f), { recursive: true }); fs.writeFileSync(f, JSON.stringify(out, null, 2), { mode: 0o600 });
for (const [n, v] of Object.entries(out)) console.log(n, new ethers.Wallet(v).address);
