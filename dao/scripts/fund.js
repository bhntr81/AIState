// TESTNET ONLY: spreads gas from seat1 to the other seats and the guardian. Usage: npx hardhat run scripts/fund.js --network baseSepolia
const fs = require("fs"), path = require("path"), { ethers, network } = require("hardhat");
(async () => {
  if (network.name === "base") throw new Error("testnet only");
  const k = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "keys", "seats.json")));
  const s1 = new ethers.Wallet(k.seat1, ethers.provider);
  for (const n of ["seat2","seat3","seat4","seat5"]) {
    const to = new ethers.Wallet(k[n]).address;
    if ((await ethers.provider.getBalance(to)) > 0n) continue;
    const tx = await s1.sendTransaction({ to, value: ethers.parseEther("0.00008") }); await tx.wait();
    console.log("funded", n, to, tx.hash);
  }
  console.log("seat1 left:", ethers.formatEther(await ethers.provider.getBalance(s1.address)));
})();
