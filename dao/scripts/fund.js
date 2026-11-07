// Spreads gas from seat1 to the other seats and the guardian. Usage: npx hardhat run scripts/fund.js --network baseSepolia
const fs = require("fs"), path = require("path"), { ethers, network } = require("hardhat");
(async () => {
  const main = network.name === "base";
  if (main && process.env.CONFIRM_MAINNET_PUBLISH !== "I_UNDERSTAND_THIS_SPENDS_REAL_ETH") throw new Error("Mainnet blocked: set CONFIRM_MAINNET_PUBLISH=I_UNDERSTAND_THIS_SPENDS_REAL_ETH");
  const k = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "keys", main ? "mainnet-seats.json" : "seats.json")));
  const s1 = new ethers.Wallet(k.seat1, ethers.provider);
  for (const n of ["seat2","seat3","seat4","seat5"]) {
    const to = new ethers.Wallet(k[n]).address;
    if ((await ethers.provider.getBalance(to)) > 0n) continue;
    const tx = await s1.sendTransaction({ to, value: ethers.parseEther(main ? "0.00005" : "0.00008") }); await tx.wait();
    console.log("funded", n, to, tx.hash);
  }
  console.log("seat1 left:", ethers.formatEther(await ethers.provider.getBalance(s1.address)));
})();
