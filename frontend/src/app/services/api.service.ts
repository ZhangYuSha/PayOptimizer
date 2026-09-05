import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import {
  Provider,
  FindCheapestResponse,
  LoginResponse,
  RegisterResponse,
  TimingOptimizationResponse,
  AIOptimizeResponse
} from '../models/api.models';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private readonly apiUrl =
    'http://127.0.0.1:5000/api';

  constructor(
    private http: HttpClient
  ) {}

  getProviders(): Observable<Provider[]> {

    return this.http.get<Provider[]>(
      `${this.apiUrl}/providers`
    );

  }

  getExchangeRates(
    from: string,
    to: string
  ): Observable<any> {

    return this.http.get<any>(
      `${this.apiUrl}/exchange-rates`,
      {
        params: {
          from,
          to
        }
      }
    );

  }

  getFees(): Observable<any> {

    return this.http.get<any>(
      `${this.apiUrl}/fees`
    );

  }

  findCheapest(
    from: string,
    to: string,
    amount: number
  ): Observable<FindCheapestResponse> {

    return this.http.get<FindCheapestResponse>(
      `${this.apiUrl}/find-cheapest`,
      {
        params: {
          from,
          to,
          amount: amount.toString()
        }
      }
    );

  }

  optimizeTiming(
    from: string,
    to: string,
    amount: number,
    deadline: string
  ): Observable<TimingOptimizationResponse> {

    return this.http.post<TimingOptimizationResponse>(
      `${this.apiUrl}/optimize-timing`,
      {
        from,
        to,
        amount,
        deadline
      }
    );

  }

  aiOptimize(
    message: string
  ): Observable<AIOptimizeResponse> {

    return this.http.post<AIOptimizeResponse>(
      `${this.apiUrl}/ai/optimize`,
      {
        message
      }
    );

  }

  register(
    name: string,
    email: string,
    password: string
  ): Observable<RegisterResponse> {

    return this.http.post<RegisterResponse>(
      `${this.apiUrl}/register`,
      {
        name,
        email,
        password
      }
    );

  }

  login(
    email: string,
    password: string
  ): Observable<LoginResponse> {

    return this.http.post<LoginResponse>(
      `${this.apiUrl}/login`,
      {
        email,
        password
      }
    );

  }

}