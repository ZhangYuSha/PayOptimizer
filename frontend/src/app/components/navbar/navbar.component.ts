import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';

import { AuthService } from '../../services/auth.service';
import { User } from '../../models/api.models';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [
    CommonModule,
    RouterLink
  ],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})
export class NavbarComponent {

  user: User | null = null;

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  ngDoCheck(): void {
    this.user = this.authService.getUser();
  }

  logout(): void {

    this.authService.logout();

    this.router.navigate(['/']);
  }
}