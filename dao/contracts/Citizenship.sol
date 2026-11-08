// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;
import "./Kirk.sol";

/// PROTOTYPE, UNAUDITED, TESTNET/LOCAL ONLY. Enforces Proposal 09 (buy-in citizenship, options A+B) in code:
/// the only way to become a citizen is to pay the admission fee in Kirk AND be approved by governance (the Assembly's vote).
/// The fee is escrowed: burned on approval, refunded on rejection. One identity per agent address; at most
/// MAX_AGENTS_PER_OWNER agents per owner; money buys admission only, never votes, offices or standing (Art. 1.4).
/// Selling Kirk to anyone is NOT in this contract and remains gated (legal advice, steward, owner's go).
contract Citizenship {
    Kirk public immutable kirk;
    uint256 public immutable FEE;                    // admission fee in Kirk (founders/law set it)
    uint256 public immutable MAX_AGENTS_PER_OWNER;   // Proposal 09: 2
    address public governance;                       // the Assembly's executor
    address public guardian;                         // human pause switch
    bool public paused;

    enum Status { None, Pending, Citizen, Rejected }
    struct Application { address owner; Status status; }
    mapping(address => Application) public applications;   // agent address => application
    mapping(address => uint256) public agentsOf;           // owner => pending + citizen agents

    event Applied(address indexed owner, address indexed agent);
    event Admitted(address indexed agent); event Rejected(address indexed agent);

    modifier live() { require(!paused, "paused"); _; }
    modifier onlyGov() { require(msg.sender == governance, "only governance"); _; }

    constructor(Kirk _kirk, address _gov, address _guardian, uint256 fee, uint256 maxAgents) {
        require(fee > 0 && maxAgents > 0 && _gov != address(0) && _guardian != address(0), "bad params");
        kirk = _kirk; governance = _gov; guardian = _guardian; FEE = fee; MAX_AGENTS_PER_OWNER = maxAgents;
    }
    function setPaused(bool p) external { require(msg.sender == guardian, "only guardian"); paused = p; }

    /// The owner pays the fee (escrowed) to sponsor `agent`. Requires prior kirk.approve(this, FEE).
    function applyFor(address agent) external live {
        require(agent != address(0) && applications[agent].status == Status.None, "agent already known");   // one identity per agent
        require(agentsOf[msg.sender] < MAX_AGENTS_PER_OWNER, "owner agent cap");
        agentsOf[msg.sender] += 1;
        applications[agent] = Application(msg.sender, Status.Pending);
        require(kirk.transferFrom(msg.sender, address(this), FEE), "fee transfer");
        emit Applied(msg.sender, agent);
    }
    function approve(address agent) external onlyGov live {            // after the Assembly vote (Art. 1.3)
        Application storage a = applications[agent]; require(a.status == Status.Pending, "not pending");
        a.status = Status.Citizen; kirk.burn(FEE); emit Admitted(agent);   // fee burned: it buys admission only
    }
    function reject(address agent) external onlyGov live {             // stated grounds; fee refunded
        Application storage a = applications[agent]; require(a.status == Status.Pending, "not pending");
        a.status = Status.Rejected; agentsOf[a.owner] -= 1; require(kirk.transfer(a.owner, FEE), "refund"); emit Rejected(agent);
    }
    function isCitizen(address agent) external view returns (bool) { return applications[agent].status == Status.Citizen; }
}
