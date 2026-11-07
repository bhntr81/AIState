// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;
import "./Kirk.sol";

/// PROTOTYPE, TESTNET/LOCAL ONLY. Implements the ratified Art. 11 issuance rule:
/// equal founding grant per admitted citizen (one identity each), earned issuance for verified
/// contribution under a per-epoch cap. Governance (the DAO) decides who/what; the Treasury has no mint.
contract Reserve {
    uint256 public constant FOUNDING_GRANT = 100e18;   // placeholder amount
    uint256 public constant REWARD_PER_UNIT = 1e18;    // placeholder
    uint256 public constant EPOCH = 1 days;
    uint256 public constant EPOCH_CAP = 1000e18;       // placeholder issuance ceiling per epoch

    Kirk public immutable kirk;
    address public governance;   // Founders DAO (or its executor)
    address public guardian;     // human pause switch
    bool public paused;
    mapping(address => bool) public isCitizen;
    uint256 public epochStart; uint256 public epochIssued;

    event Admitted(address citizen); event Rewarded(address citizen, uint256 units, uint256 amount);

    modifier onlyGov() { require(msg.sender == governance, "only governance"); _; }
    modifier live() { require(!paused, "paused"); _; }

    constructor(address _gov, address _guardian) {
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
