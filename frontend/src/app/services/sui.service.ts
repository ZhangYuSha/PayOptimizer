import {
  Injectable
} from '@angular/core';

import {
  Transaction,
  coinWithBalance
} from '@mysten/sui/transactions';

import {
  dAppKit
} from '../sui/dapp-kit';


@Injectable({
  providedIn: 'root'
})
export class SuiService {


  async sendSui(
    recipient: string,
    amountSui: number
  ): Promise<string> {

    const connection =
      dAppKit.stores.$connection.get();


    if (
      !connection ||
      !connection.account
    ) {

      throw new Error(
        'Please connect a Sui wallet first.'
      );

    }


    const transaction =
      new Transaction();


    const amountMist =
      BigInt(
        Math.floor(
          amountSui * 1_000_000_000
        )
      );


    transaction.transferObjects(

      [
        coinWithBalance({
          balance: amountMist
        })
      ],

      recipient

    );


    const result =
      await dAppKit.signAndExecuteTransaction({

        transaction,

        network:
          'testnet'

      });


    if (
      'FailedTransaction'
      in result
    ) {

      throw new Error(
        'Sui transaction failed.'
      );

    }


    if (
      'Transaction'
      in result
    ) {

      return result.Transaction.digest;

    }


    throw new Error(
      'Unexpected Sui transaction result.'
    );

  }

}