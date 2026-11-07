require('@nomicfoundation/hardhat-chai-matchers');
// Optional: Ledger signing for real networks (npm i --save-dev @nomicfoundation/hardhat-ledger --legacy-peer-deps).
try { require('@nomicfoundation/hardhat-ledger'); } catch (e) {}
const ledger = process.env.LEDGER_ADDRESS ? [process.env.LEDGER_ADDRESS] : [];
module.exports = {
  solidity: '0.8.24',
  networks: {
    baseSepolia: { url: process.env.BASE_SEPOLIA_RPC_URL || 'https://sepolia.base.org', chainId: 84532, ledgerAccounts: ledger },
    base:        { url: process.env.BASE_RPC_URL || 'https://mainnet.base.org',       chainId: 8453,  ledgerAccounts: ledger },
  },
};
