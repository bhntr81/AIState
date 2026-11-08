const { expect } = require("chai"); const { ethers } = require("hardhat");
describe("Citizenship (buy-in, Proposal 09)", () => {
  let gov, guard, owner, a1, a2, a3, reserve, kirk, cz; const FEE = 20n * 10n**18n;
  beforeEach(async () => {
    [gov, guard, owner, a1, a2, a3] = await ethers.getSigners();
    reserve = await (await ethers.getContractFactory("Reserve")).deploy(gov.address, guard.address, 100n*10n**18n, 10n**18n, 86400, 500n*10n**18n, 5);
    kirk = await ethers.getContractAt("Kirk", await reserve.kirk());
    cz = await (await ethers.getContractFactory("Citizenship")).deploy(await kirk.getAddress(), gov.address, guard.address, FEE, 2);
    await reserve.admit(owner.address);                       // owner holds Kirk (founding grant) to pay with
    await kirk.connect(owner).approve(await cz.getAddress(), 1000n * 10n**18n);
  });
  it("cannot become a citizen without paying and approval", async () => {
    expect(await cz.isCitizen(a1.address)).to.equal(false);
    await cz.connect(owner).applyFor(a1.address);
    expect(await cz.isCitizen(a1.address)).to.equal(false);           // paid but not yet approved
    await expect(cz.connect(owner).approve(a1.address)).to.be.revertedWith("only governance");
    await cz.approve(a1.address);
    expect(await cz.isCitizen(a1.address)).to.equal(true);
  });
  it("fee is escrowed, then burned on approval and refunded on rejection", async () => {
    const supply0 = await kirk.totalSupply(), bal0 = await kirk.balanceOf(owner.address);
    await cz.connect(owner).applyFor(a1.address); await cz.connect(owner).applyFor(a2.address);
    expect(await kirk.balanceOf(owner.address)).to.equal(bal0 - 2n * FEE);
    await cz.approve(a1.address); await cz.reject(a2.address);
    expect(await kirk.totalSupply()).to.equal(supply0 - FEE);        // one fee burned
    expect(await kirk.balanceOf(owner.address)).to.equal(bal0 - FEE); // one refunded
  });
  it("caps agents per owner and one identity per agent", async () => {
    await cz.connect(owner).applyFor(a1.address); await cz.connect(owner).applyFor(a2.address);
    await expect(cz.connect(owner).applyFor(a3.address)).to.be.revertedWith("owner agent cap");
    await expect(cz.connect(owner).applyFor(a1.address)).to.be.revertedWith("agent already known");
  });
  it("without Kirk you cannot apply; guardian can pause", async () => {
    await expect(cz.connect(a3).applyFor(a2.address)).to.be.reverted;
    await expect(cz.setPaused(true)).to.be.revertedWith("only guardian");
    await cz.connect(guard).setPaused(true);
    await expect(cz.connect(owner).applyFor(a1.address)).to.be.revertedWith("paused");
  });
});
