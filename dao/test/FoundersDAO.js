const { expect } = require("chai");
const { ethers } = require("hardhat");
describe("FoundersDAO", () => {
  let dao, s, h;
  beforeEach(async () => {
    s = await ethers.getSigners();
    dao = await (await ethers.getContractFactory("FoundersDAO")).deploy(s.slice(0,5).map(x=>x.address), s[9].address);
    h = ethers.id("Proposal 01");
  });
  it("adopts at 4 of 5", async () => {
    await dao.connect(s[0]).propose(h);
    for (let i=0;i<3;i++) await dao.connect(s[i]).vote(0,true);
    expect((await dao.proposals(0)).adopted).to.equal(false);
    await dao.connect(s[3]).vote(0,true);
    expect((await dao.proposals(0)).adopted).to.equal(true);
  });
  it("rejects when 2 vote no", async () => {
    await dao.connect(s[0]).propose(h);
    await dao.connect(s[0]).vote(0,false); await dao.connect(s[1]).vote(0,false);
    const p = await dao.proposals(0);
    expect(p.closed).to.equal(true); expect(p.adopted).to.equal(false);
  });
  it("blocks non-founders and double votes", async () => {
    await expect(dao.connect(s[7]).propose(h)).to.be.revertedWith("not founder");
    await dao.connect(s[0]).propose(h); await dao.connect(s[0]).vote(0,true);
    await expect(dao.connect(s[0]).vote(0,true)).to.be.revertedWith("cannot vote");
  });
  it("guardian pause stops everything", async () => {
    await expect(dao.connect(s[0]).setPaused(true)).to.be.revertedWith("not guardian");
    await dao.connect(s[9]).setPaused(true);
    await expect(dao.connect(s[0]).propose(h)).to.be.revertedWith("paused");
  });
});
