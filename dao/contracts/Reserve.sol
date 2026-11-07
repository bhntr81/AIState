// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;
import "./Kirk.sol";

/// PROTOTYPE, TESTNET/LOCAL ONLY. Implements the ratified Art. 11 issuance rule:
/// equal founding grant per admitted citizen (one identity each), earned issuance for verified
/// contribution under a per-epoch cap. Governance (the DAO) decides who/what; the Treasury has no mint.
contract Reserve {
    // Set once at deployment (from dao/params.json, decided by the founders); immutable after.
    uint256 public immutable FOUNDING_GRANT;
    uint256 public immutable REWARD_PER_UNIT;
    uint256 public immutable EPOCH;
    uint256 public immutable EPOCH_CAP;

    Kirk public immutable kirk;
    address public governance;   // Founders DAO (or its executor)
    address public guardian;     // human pause switch
    bool public paused;
    mapping(address => bool) public isCitizen;
    uint256 public epochStart; uint256 public epochIssued;

    event Admitted(address citizen); event Rewarded(address citizen, uint256 units, uint256 amount);

    modifier onlyGov() { require(msg.sender == governance, "only governance"); _; }
    modifier live() { require(!paused, "paused"); _; }

    constructor(address _gov, address _guardian, uint256 grant, uint256 rewardPerUnit, uint256 epochLen, uint256 epochCap) {
        require(_gov != address(0) && _guardian != address(0), "zero address");
        require(grant > 0 && rewardPerUnit > 0 && epochLen > 0 && epochCap >= grant, "bad params");
        FOUNDING_GRANT = grant; REWARD_PER_UNIT = rewardPerUnit; EPOCH = epochLen; EPOCH_CAP = epochCap;
        governance = _gov; guardian = _guardian; kirk = new Kirk(address(this)); epochStart = block.timestamp;
    }
    function setPaused(bool p) external { require(msg.sender == guardian, "only guardian"); paused = p; }

    function admit(address c) external onlyGov live {
        require(!isCitizen[c], "already citizen");           // one identity, Art. 1.2
        isCitizen[c] = true; _issue(c, FOUNDING_GRANT); emit Admitted(c);
    }
    function reward(address c, uint256 units) external onlyGov live {
        require(isCitizen[c], "not citizen");
        uint256 amt = units * REWARD_PER_UNIT; _issue(c, amt); emit Rewarded(c, units, amt);
    }
    function _issue(address to, uint256 amt) internal {
        if (block.timestamp >= epochStart + EPOCH) { epochStart = block.timestamp; epochIssued = 0; }
        require(epochIssued + amt <= EPOCH_CAP, "epoch cap");
        epochIssued += amt; kirk.mint(to, amt);
    }
}
