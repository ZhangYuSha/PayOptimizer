import { createDAppKit } from '@mysten/dapp-kit-core';
import { SuiGrpcClient } from '@mysten/sui/grpc';

/**
 * Sui network configuration.
 *
 * We are using Sui Testnet for the hackathon demo.
 */
const GRPC_URLS = {
  testnet: 'https://fullnode.testnet.sui.io:443'
} as const;


/**
 * Create the global Sui dApp Kit instance.
 *
 * This instance is shared by:
 * - Wallet connection
 * - Account state
 * - Transaction signing
 * - Transaction execution
 */
export const dAppKit = createDAppKit({

  /**
   * Networks supported by the application.
   */
  networks: [
    'testnet'
  ],

  /**
   * Network selected when the application starts.
   */
  defaultNetwork:
    'testnet',

  /**
   * Create a Sui client for the selected network.
   */
  createClient(network) {

    const baseUrl =
      GRPC_URLS[
        network as keyof typeof GRPC_URLS
      ];

    return new SuiGrpcClient({
      network,
      baseUrl
    });

  }

});