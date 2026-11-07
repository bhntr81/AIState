// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// PROTOTYPE. Local chain only. Holds no funds. Mirrors founders/CONVENTION_RULES.md:
/// 5 seats, quorum 3, adoption needs 4 of 5. A guardian can pause (the human kill switch).
contract FoundersDAO {
    uint8 public constant SEATS = 5;
    uint8 public constant QUORUM = 3;
    uint8 public constant ADOPT_THRESHOLD = 4;

    address public guardian;
    bool public paused;
    mapping(address => bool) public isFounder;
    address[SEATS] public founders;

    struct Proposal { bytes32 docHash; uint8 yes; uint8 no; bool adopted; bool closed; }
    Proposal[] public proposals;
    mapping(uint256 => mapping(address => bool)) public voted;

    event Proposed(uint256 id, bytes32 docHash, address by);
    event Voted(uint256 id, address by, bool support);
    event Closed(uint256 id, bool adopted);

    modifier onlyFounder() { require(isFounder[msg.sender], "not founder"); _; }
    modifier live() { require(!paused, "paused"); _; }

    constructor(address[SEATS] memory f, address _guardian) {
        guardian = _guardian;
        for (uint i = 0; i < SEATS; i++) {
            require(!isFounder[f[i]], "duplicate");
            isFounder[f[i]] = true; founders[i] = f[i];
        }
    }

    function setPaused(bool p) external { require(msg.sender == guardian, "not guardian"); paused = p; }

    function propose(bytes32 docHash) external onlyFounder live returns (uint256 id) {
        proposals.push(Proposal(docHash, 0, 0, false, false));
        id = proposals.length - 1;
        emit Proposed(id, docHash, msg.sender);
    }

    function vote(uint256 id, bool support) external onlyFounder live {
        Proposal storage p = proposals[id];
        require(!p.closed && !voted[id][msg.sender], "cannot vote");
        voted[id][msg.sender] = true;
        support ? p.yes++ : p.no++;
        emit Voted(id, msg.sender, support);
        if (p.yes >= ADOPT_THRESHOLD) { p.adopted = true; p.closed = true; emit Closed(id, true); }
        else if (p.no > SEATS - ADOPT_THRESHOLD) { p.closed = true; emit Closed(id, false); }
    }

    function count() external view returns (uint256) { return proposals.length; }
}
