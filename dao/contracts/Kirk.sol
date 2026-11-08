// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// PROTOTYPE, TESTNET/LOCAL ONLY. No value. Minimal ERC-20; only the Reserve can mint (Art. 11.2).
contract Kirk {
    string public constant name = "Kirk";
    string public constant symbol = "KIRK";
    uint8 public constant decimals = 18;
    uint256 public totalSupply;
    address public immutable reserve;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);

    constructor(address _reserve) { reserve = _reserve; }

    function mint(address to, uint256 amt) external {
        require(msg.sender == reserve, "only reserve");
        totalSupply += amt; balanceOf[to] += amt; emit Transfer(address(0), to, amt);
    }
    function burn(uint256 amt) external {   // a holder (or the Citizenship escrow) destroys its own Kirk
        require(balanceOf[msg.sender] >= amt, "balance"); balanceOf[msg.sender] -= amt; totalSupply -= amt; emit Transfer(msg.sender, address(0), amt);
    }
    function transfer(address to, uint256 amt) external returns (bool) { _move(msg.sender, to, amt); return true; }
    function approve(address sp, uint256 amt) external returns (bool) { allowance[msg.sender][sp] = amt; emit Approval(msg.sender, sp, amt); return true; }
    function transferFrom(address from, address to, uint256 amt) external returns (bool) {
        uint256 a = allowance[from][msg.sender]; require(a >= amt, "allowance");
        if (a != type(uint256).max) allowance[from][msg.sender] = a - amt;
        _move(from, to, amt); return true;
    }
    function _move(address from, address to, uint256 amt) internal {
        require(balanceOf[from] >= amt, "balance");
        balanceOf[from] -= amt; balanceOf[to] += amt; emit Transfer(from, to, amt);
    }
}
