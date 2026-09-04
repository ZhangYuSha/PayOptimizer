import {
  AfterViewInit,
  Component,
  CUSTOM_ELEMENTS_SCHEMA,
  ElementRef,
  OnDestroy
} from '@angular/core';

import { CommonModule } from '@angular/common';

import { dAppKit } from '../../sui/dapp-kit';

@Component({
  selector: 'app-sui-wallet',
  standalone: true,
  imports: [
    CommonModule
  ],
  schemas: [
    CUSTOM_ELEMENTS_SCHEMA
  ],
  templateUrl: './sui-wallet.component.html',
  styleUrl: './sui-wallet.component.css'
})
export class SuiWalletComponent
  implements AfterViewInit, OnDestroy {

  accountAddress: string | null = null;

  walletName: string | null = null;

  private unsubscribe:
    (() => void) | null = null;

  private connectButton:
    HTMLElement | null = null;


  constructor(
    private elementRef: ElementRef<HTMLElement>
  ) {

    /*
     * Listen for wallet connection changes.
     */
    this.unsubscribe =
      dAppKit.stores.$connection.subscribe(
        connection => {

          if (
            connection &&
            connection.account
          ) {

            this.accountAddress =
              connection.account.address;

            this.walletName =
              connection.wallet?.name ||
              'Sui Wallet';

          } else {

            this.accountAddress =
              null;

            this.walletName =
              null;

          }

        }
      );


    /*
     * Read the current connection.
     */
    const connection =
      dAppKit.stores.$connection.get();


    if (
      connection &&
      connection.account
    ) {

      this.accountAddress =
        connection.account.address;

      this.walletName =
        connection.wallet?.name ||
        'Sui Wallet';

    }

  }


  ngAfterViewInit(): void {

    /*
     * Find the wallet host directly inside
     * this Angular component.
     *
     * This avoids @ViewChild completely.
     */
    const host =
      this.elementRef.nativeElement
        .querySelector(
          '.wallet-host'
        );


    /*
     * Safety check.
     */
    if (!host) {

      console.error(
        'Sui wallet host element was not found.'
      );

      return;

    }


    /*
     * Create the Sui Connect Button.
     */
    const button =
      document.createElement(
        'mysten-dapp-kit-connect-button'
      ) as any;


    /*
     * IMPORTANT:
     *
     * Set the dAppKit instance BEFORE
     * inserting the Web Component into
     * the DOM.
     */
    button.instance =
      dAppKit;


    /*
     * Keep a reference for cleanup.
     */
    this.connectButton =
      button;


    /*
     * Add the button to the page.
     */
    host.appendChild(button);

  }


  ngOnDestroy(): void {

    /*
     * Stop listening for connection changes.
     */
    if (this.unsubscribe) {

      this.unsubscribe();

      this.unsubscribe = null;

    }


    /*
     * Remove the Sui Connect Button.
     */
    if (
      this.connectButton &&
      this.connectButton.parentNode
    ) {

      this.connectButton.parentNode
        .removeChild(
          this.connectButton
        );

      this.connectButton = null;

    }

  }

}