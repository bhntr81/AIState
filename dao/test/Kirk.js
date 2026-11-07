const { expect } = require("chai"); const { ethers } = require("hardhat");
describe("Kirk / Reserve / Treasury", () => {
  let gov, guard, a, b, reserve, kirk, treasury;
  beforeEach(async () => {
    [gov, guard, a, b] = await ethers.getSigners();
    reserve = await (await ethers.getContractFactory("Reserve")).deploy(gov.address, guard.address, 100n*10n**18n, 10n**18n, 86400, 1000n*10n**18n);
    kirk = await ethers.getContractAt("Kirk", await reserve.kirk());
    treasury = await (await ethers.getContractFactory("Treasury")).deploy(await kirk.getAddress(), gov.address);
  });
  it("founding grant is equal and once only", async () => {
    await reserve.admit(a.address); await reserve.admit(b.address);
    expect(await kirk.balanceOf(a.address)).to.equal(await kirk.balanceOf(b.address));
    await expect(reserve.admit(a.address)).to.be.revertedWith("already citizen");
  });
  it("only governance can admit or reward; only citizens earn", async () => {
    await expect(reserve.connect(a).admit(a.address)).to.be.revertedWith("only governance");
    await expect(reserve.reward(a.address, 1)).to.be.revertedWith("not citizen");
    await reserve.admit(a.address); await reserve.reward(a.address, 5);
    expect(await kirk.balanceOf(a.address)).to.equal(105n * 10n**18n);
  });
  it("treasury and everyone else cannot mint", async () => {
    await expect(kirk.connect(gov).mint(a.address, 1)).to.be.revertedWith("only reserve");
    expect(treasury.interface.getFunction("mint")).to.equal(null);
  });
  it("epoch issuance cap enforced, resets next epoch", async () => {
    await reserve.admit(a.address);
    await expect(reserve.reward(a.address, 901)).to.be.revertedWith("epoch cap");
    await reserve.reward(a.address, 900);
    await ethers.provider.send("evm_increaseTime", [86401]); await ethers.provider.send("evm_mine");
    await reserve.reward(a.address, 900);
  });
  it("guardian pause halts issuance", async () => {
    await expect(reserve.setPaused(true)).to.be.revertedWith("only guardian");
    await reserve.connect(guard).setPaused(true);
    await expect(reserve.admit(a.address)).to.be.revertedWith("paused");
  });
  it("treasury spends only via governance; transfers work", async () => {
    await reserve.admit(a.address);
    await kirk.connect(a).transfer(await treasury.getAddress(), 10n*10n**18n);
    await expect(treasury.connect(a).spend(b.address, 1)).to.be.revertedWith("only governance");
    await treasury.spend(b.address, 4n*10n**18n);
    expect(await kirk.balanceOf(b.address)).to.equal(4n*10n**18n);
  });
});
