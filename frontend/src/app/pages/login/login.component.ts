import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  FormsModule
} from '@angular/forms';

import {
  Router,
  RouterLink,
  ActivatedRoute
} from '@angular/router';

import { ApiService } from '../../services/api.service';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterLink
  ],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {

  email = '';
  password = '';

  errorMessage = '';
  loading = false;

  returnUrl = '/';


  constructor(
    private apiService: ApiService,
    private authService: AuthService,
    private router: Router,
    private route: ActivatedRoute
  ) {

    this.returnUrl =
      this.route.snapshot.queryParams[
        'returnUrl'
      ] || '/';

  }


  login(): void {

    this.errorMessage = '';

    if (!this.email || !this.password) {

      this.errorMessage =
        'Please enter your email and password.';

      return;
    }


    this.loading = true;


    this.apiService
      .login(
        this.email,
        this.password
      )
      .subscribe({

        next: (response) => {

          this.authService.saveUser(
            response.user
          );

          this.loading = false;

          this.router.navigate([
            this.returnUrl
          ]);
        },


        error: (error) => {

          this.loading = false;

          this.errorMessage =
            error.error?.error ||
            'Login failed. Please try again.';
        }

      });
  }
}