import {
  ChangeDetectorRef,
  Component
} from '@angular/core';

import {
  CommonModule
} from '@angular/common';

import {
  FormsModule
} from '@angular/forms';

import {
  finalize
} from 'rxjs';

import {
  ApiService
} from '../../services/api.service';

import {
  SuiService
} from '../../services/sui.service';

import {
  AIOptimizeResponse
} from '../../models/api.models';

import {
  SuiWalletComponent
} from '../../components/sui-wallet/sui-wallet.component';

import {
  dAppKit
} from '../../sui/dapp-kit';


@Component({
  selector: 'app-ai',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    SuiWalletComponent
  ],
  templateUrl: './ai.component.html',
  styleUrl: './ai.component.css'
})
export class AIComponent {

  readonly dAppKit = dAppKit;

  message =
    'Send RM1000 to USD by 2026-09-15 17:00. Find the cheapest option.';

  result:
    AIOptimizeResponse | null = null;

  errorMessage =
    '';

  loading =
    false;

  paying =
    false;

  transactionDigest:
    string | null = null;


  constructor(
    private apiService: ApiService,
    private suiService: SuiService,
    private changeDetectorRef: ChangeDetectorRef
  ) {}


  optimize(): void {

    this.errorMessage =
      '';

    this.result =
      null;

    this.transactionDigest =
      null;


    if (!this.message.trim()) {

      this.errorMessage =
        'Please describe your payment request.';

      return;

    }


    this.loading =
      true;

    this.changeDetectorRef.detectChanges();


    console.log(
      'Sending AI request...'
    );


    this.apiService
      .aiOptimize(this.message)

      .pipe(

        finalize(() => {

          this.loading =
            false;

          console.log(
            'AI loading finished:',
            this.loading
          );


          /*
           * Force Angular to update the UI.
           */
          this.changeDetectorRef.detectChanges();

        })

      )

      .subscribe({

        next: response => {

          console.log(
            'AI RESPONSE:',
            response
          );


          this.result =
            response;


          console.log(
            'AI result stored.'
          );


          /*
           * Force Angular to render the
           * recommendation immediately.
           */
          this.changeDetectorRef.detectChanges();

        },


        error: error => {

          console.error(
            'AI ERROR:',
            error
          );


          this.errorMessage =
            error?.error?.error ||
            'Unable to optimize payment.';


          this.changeDetectorRef.detectChanges();

        }

      });

  }


  async executeSuiPayment(): Promise<void> {

    this.errorMessage =
      '';

    this.transactionDigest =
      null;


    if (!this.result) {

      return;

    }


    const connection =
      dAppKit.stores.$connection.get();


    if (
      !connection ||
      !connection.account
    ) {

      this.errorMessage =
        'Please connect your Sui wallet first.';

      this.changeDetectorRef.detectChanges();

      return;

    }


    /*
     * DEMO ONLY:
     *
     * Sends 0.001 SUI on Sui Testnet.
     *
     * This is NOT an actual
     * MYR -> USD settlement.
     */
    const recipient =
      connection.account.address;

    const testAmountSui =
      0.001;


    try {

      this.paying =
        true;

      this.changeDetectorRef.detectChanges();


      const digest =
        await this.suiService.sendSui(
          recipient,
          testAmountSui
        );


      this.transactionDigest =
        digest;

    } catch (error: any) {

      console.error(
        'SUI PAYMENT ERROR:',
        error
      );


      this.errorMessage =
        error?.message ||
        'Sui payment failed.';

    } finally {

      this.paying =
        false;

      this.changeDetectorRef.detectChanges();

    }

  }

}