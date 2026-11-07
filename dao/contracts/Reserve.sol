// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;
import "./Kirk.sol";

/// PROTOTYPE, UNAUDITED. Implements the ratified Art. 11 issuance rule and Proposals 10 and 12:
/// equal founding grant per admitted citizen (one identity each), earned issuance for verified
/// contribution under a fixed-window per-epoch cap and a per-citizen unit limit. Governance decides
/// who and what; the Treasury has no mint power.
contract Reserve {
    // Set once at deployment (from dao/params.json, decided by the founders); immutable after.
    uint256 public immutable FOUNDING_GRANT;
    uint256 public immutable REWARD_PER_UNIT;
    uint256 public immutable EPOCH;
    uint256 public immutable EPOCH_CAP;
    uint256 public immutable MAX_UNITS_PER_CITIZEN_EPOCH;   // Proposal 10: 5
    uint256 public immutable GENESIS;

    Kirk public immutable kirk;
    address public governance;   // Founders DAO (or its executor)
    address public guardian;     // human pause switch
    bool public paused;
    mapping(address => bool) public isCitizen;
    mapping(uint256 => uint256) public issuedInEpoch;                       // epoch number => Kirk issued
    mapping(address => mapping(uint256 => uint256)) public unitsInEpoch;    // citizen => epoch number => units

    event Admitted(address citizen); event Rewarded(address citizen, uint256 units, uint256 amount);

    modifier onlyGov() { require(msg.sender == governance, "only governance"); _; }
    modifier live() { require(!paused, "paused"); _; }

    constructor(address _gov, address _guardian, uint256 grant, uint256 rewardPerUnit, uint256 epochLen, uint256 epochCap, uint256 maxUnits) {
        require(_gov != address(0) && _guardian != address(0), "zero address");
        require(grant > 0 && rewardPerUnit > 0 && epochLen > 0 && epochCap >= grant && maxUnits > 0, "bad params");
        FOUNDING_GRANT = grant; REWARD_PER_UNIT = rewardPerUnit; EPOCH = epochLen; EPOCH_CAP = epochCap;
        MAX_UNITS_PER_CITIZEN_EPOCH = maxUnits; GENESIS = block.timestamp;
        governance = _gov; guardian = _guardian; kirk = new Kirk(address(this));
    }
    function currentEpoch() public view returns (uint256) { return (block.timestamp - GENESIS) / EPOCH; }
    function setPaused(bool p) external { require(msg.sender == guardian, "only guardian"); paused = p; }

    function admit(address c) external onlyGov live {
        require(!isCitizen[c], "already citizen");           // one identity, Art. 1.2
        isCitizen[c] = true; _issue(c, FOUNDING_GRANT); emit Admitted(c);
    }
    function reward(address c, uint256 units) external onlyGov live {
        require(isCitizen[c], "not citizen");
        uint256 n = currentEpoch();
        require(unitsInEpoch[c][n] + units <= MAX_UNITS_PER_CITIZEN_EPOCH, "unit limit");
        unitsInEpoch[c][n] += units;
        uint256 amt = units * REWARD_PER_UNIT; _issue(c, amt); emit Rewarded(c, units, amt);
    }
    function _issue(address to, uint256 amt) internal {
        uint256 n = currentEpoch();
        require(issuedInEpoch[n] + amt <= EPOCH_CAP, "epoch cap");
        issuedInEpoch[n] += amt; kirk.mint(to, amt);
    }
}
