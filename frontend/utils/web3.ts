import { ethers } from "ethers";

declare global {
  interface Window {
    ethereum?: any;
  }
}

export const connectWallet = async (): Promise<string | null> => {
  // Check if MetaMask is installed
  if (typeof window.ethereum === "undefined") {
    const errorMsg = 
      "MetaMask is not detected!\n\n" +
      "Please:\n" +
      "1. Install MetaMask extension\n" +
      "2. Enable the extension in your browser\n" +
      "3. Unlock MetaMask\n" +
      "4. Refresh this page (Ctrl+Shift+R)\n\n" +
      "If MetaMask is installed, check:\n" +
      "- Extension is enabled: chrome://extensions\n" +
      "- Extension is unlocked\n" +
      "- Browser permissions allow access to localhost";
    alert(errorMsg);
    console.error("MetaMask not detected. window.ethereum is undefined.");
    return null;
  }

  try {
    const accounts = await window.ethereum.request({
      method: "eth_requestAccounts",
    });
    return accounts[0];
  } catch (error: any) {
    console.error("Error connecting wallet:", error);
    if (error.code === 4001) {
      alert("Please connect your MetaMask account. Click 'Connect' when prompted.");
    } else {
      alert(`Error connecting wallet: ${error.message || "Unknown error"}`);
    }
    return null;
  }
};

export const getProvider = (): ethers.BrowserProvider | null => {
  if (typeof window.ethereum !== "undefined") {
    return new ethers.BrowserProvider(window.ethereum);
  }
  return null;
};

export const getSigner = async (): Promise<ethers.JsonRpcSigner | null> => {
  const provider = getProvider();
  if (provider) {
    return await provider.getSigner();
  }
  return null;
};

export const switchNetwork = async (chainId: string) => {
  if (typeof window.ethereum !== "undefined") {
    try {
      await window.ethereum.request({
        method: "wallet_switchEthereumChain",
        params: [{ chainId }],
      });
    } catch (error: any) {
      if (error.code === 4902) {
        // Chain doesn't exist, add it
        await window.ethereum.request({
          method: "wallet_addEthereumChain",
          params: [
            {
              chainId: chainId,
              chainName: "Localhost",
              rpcUrls: ["http://localhost:8545"],
              nativeCurrency: {
                name: "ETH",
                symbol: "ETH",
                decimals: 18,
              },
            },
          ],
        });
      }
    }
  }
};

export const formatAddress = (address: string): string => {
  return `${address.slice(0, 6)}...${address.slice(-4)}`;
};

export const formatDate = (timestamp: string | number): string => {
  return new Date(Number(timestamp) * 1000).toLocaleString();
};



