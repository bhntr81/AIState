// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;
import "./Kirk.sol";

/// PROTOTYPE. Holds Kirk collected as tax; governance spends it. Has NO mint power (Art. 4.2, 11.2).
contract Treasury {
    Kirk public immutable kirk; address public governance;
    constructor(Kirk k, address gov) { kirk = k; governance = gov; }
    function spend(address to, uint256 amt) external { require(msg.sender == governance, "only governance"); kirk.transfer(to, amt); }
}
