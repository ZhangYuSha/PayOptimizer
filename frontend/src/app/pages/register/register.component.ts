import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';

import { ApiService } from '../../services/api.service';
import { RegisterResponse } from '../../models/api.models';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent {
  name = '';
  email = '';
  password = '';

  errorMessage = '';
  successMessage = '';
  loading = false;

  constructor(
    private apiService: ApiService,
    private router: Router
  ) {}

  register(): void {
    this.errorMessage = '';
    this.successMessage = '';

    if (!this.name || !this.email || !this.password) {
      this.errorMessage = 'Please fill in all fields.';
      return;
    }

    this.loading = true;

    this.apiService.register(
      this.name,
      this.email,
      this.password
    ).subscribe({
      next: (response: RegisterResponse) => {
        this.loading = false;
        this.successMessage = response.message;

        setTimeout(() => {
          this.router.navigate(['/login']);
        }, 1000);
      },

      error: (error: any) => {
        this.loading = false;
        this.errorMessage =
          error.error?.error ||
          'Registration failed.';
      }
    });
  }
}