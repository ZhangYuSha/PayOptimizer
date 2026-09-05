import { Injectable } from '@angular/core';

import { User } from '../models/api.models';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private readonly userKey =
    'pay_optimizer_user';


  getUser(): User | null {

    const user =
      localStorage.getItem(
        this.userKey
      );

    if (!user) {
      return null;
    }

    try {

      return JSON.parse(user) as User;

    } catch {

      localStorage.removeItem(
        this.userKey
      );

      return null;
    }
  }


  isLoggedIn(): boolean {

    return this.getUser() !== null;
  }


  saveUser(user: User): void {

    localStorage.setItem(
      this.userKey,
      JSON.stringify(user)
    );
  }


  logout(): void {

    localStorage.removeItem(
      this.userKey
    );
  }
}
