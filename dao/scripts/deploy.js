// Deploys Reserve (which creates Kirk) and Treasury. Reads dao/params.json.
// Local/dry run:   npx hardhat run scripts/deploy.js
// Base Sepolia:    npx hardhat run scripts/deploy.js --network baseSepolia
// Base MAINNET:    needs CONFIRM_MAINNET (see ../LAUNCH_RUNBOOK.md); signs on the hardware wallet.
const fs = require("fs"), path = require("path");
const { ethers, network } = require("hardhat");
(async () => {
  const params = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "params.json")));
  const real = network.name === "base";
  if (real) {
    if (process.env.CONFIRM_MAINNET !== "I_HAVE_READ_KIRK_LAUNCH_PLAN") throw new Error("Mainnet blocked: set CONFIRM_MAINNET=I_HAVE_READ_KIRK_LAUNCH_PLAN");
    if (!params.finalizedByFounders) throw new Error("Mainnet blocked: params.json is not finalized by the founders");
    if (!process.env.GOVERNANCE_ADDRESS || !process.env.GUARDIAN_ADDRESS) throw new Error("Mainnet blocked: set GOVERNANCE_ADDRESS and GUARDIAN_ADDRESS (your hardware-wallet/multisig addresses)");
  }
  const signers = await ethers.getSigners();
  const deployer = signers[0];
  const gov = process.env.GOVERNANCE_ADDRESS || deployer.address;
  const guardian = process.env.GUARDIAN_ADDRESS || (signers[1] ? signers[1].address : deployer.address);
  const e18 = (n) => ethers.parseUnits(String(n), 18);
  console.log(`network=${network.name} deployer=${deployer.address}\ngovernance=${gov}\nguardian=${guardian}`);
  const R = await (await ethers.getContractFactory("Reserve")).deploy(gov, guardian, e18(params.foundingGrantKirk), e18(params.rewardPerUnitKirk), params.epochSeconds, e18(params.epochCapKirk));
  await R.waitForDeployment();
  const kirkAddr = await R.kirk();
  const T = await (await ethers.getContractFactory("Treasury")).deploy(kirkAddr, gov);
  await T.waitForDeployment();
  const out = { network: network.name, reserve: await R.getAddress(), kirk: kirkAddr, treasury: await T.getAddress(), governance: gov, guardian, params, when: new Date().toISOString() };
  fs.mkdirSync(path.join(__dirname, "..", "deployments"), { recursive: true });
  fs.writeFileSync(path.join(__dirname, "..", "deployments", `${network.name}.json`), JSON.stringify(out, null, 2));
  console.log(out);
})();
