import {
  ChangeDetectorRef,
  Component,
  OnInit
} from '@angular/core';

import {
  CommonModule
} from '@angular/common';

import {
  FormsModule
} from '@angular/forms';

import {
  Router
} from '@angular/router';

import {
  finalize
} from 'rxjs';

import {
  ApiService
} from '../../services/api.service';

import {
  AuthService
} from '../../services/auth.service';

import {
  FindCheapestResponse
} from '../../models/api.models';


@Component({
  selector: 'app-compare',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule
  ],
  templateUrl: './compare.component.html',
  styleUrl: './compare.component.css'
})
export class CompareComponent
  implements OnInit {

  fromCurrency =
    'MYR';

  toCurrency =
    'USD';

  amount:
    number | null = null;

  result:
    FindCheapestResponse | null = null;

  errorMessage =
    '';

  loading =
    false;


  constructor(
    private apiService: ApiService,
    private authService: AuthService,
    private router: Router,
    private changeDetectorRef: ChangeDetectorRef
  ) {}


  ngOnInit(): void {

    /*
     * Compare page requires login.
     */
    if (
      !this.authService.isLoggedIn()
    ) {

      this.router.navigate(
        ['/login'],
        {
          queryParams: {
            returnUrl: '/compare'
          }
        }
      );

      return;

    }

  }


  compare(): void {

    /*
     * Clear previous state.
     */
    this.errorMessage =
      '';

    this.result =
      null;


    /*
     * Validate amount.
     */
    if (
      this.amount === null ||
      this.amount <= 0
    ) {

      this.errorMessage =
        'Please enter a valid amount.';

      this.changeDetectorRef.detectChanges();

      return;

    }


    /*
     * Prevent duplicate requests.
     */
    if (this.loading) {

      return;

    }


    /*
     * Start loading.
     */
    this.loading =
      true;

    this.changeDetectorRef.detectChanges();


    console.log(
      'Sending request:',
      {
        from:
          this.fromCurrency,

        to:
          this.toCurrency,

        amount:
          this.amount
      }
    );


    this.apiService
      .findCheapest(
        this.fromCurrency,
        this.toCurrency,
        this.amount
      )

      .pipe(

        /*
         * Always stop loading when the
         * request finishes.
         */
        finalize(() => {

          this.loading =
            false;


          console.log(
            'Compare loading finished:',
            this.loading
          );


          /*
           * Force Angular to update
           * the displayed button.
           */
          this.changeDetectorRef
            .detectChanges();

        })

      )

      .subscribe({

        next: (
          response: FindCheapestResponse
        ) => {

          console.log(
            'BACKEND RESPONSE:',
            response
          );


          /*
           * Store backend result.
           */
          this.result =
            response;


          console.log(
            'RESULT ASSIGNED:',
            this.result
          );


          /*
           * Update the UI immediately.
           */
          this.changeDetectorRef
            .detectChanges();

        },


        error: (
          error
        ) => {

          console.error(
            'BACKEND ERROR:',
            error
          );


          this.errorMessage =
            error?.error?.error ||
            'Unable to compare providers.';


          this.changeDetectorRef
            .detectChanges();

        }

      });

  }

}