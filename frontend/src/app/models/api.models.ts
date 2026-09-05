export interface User {
  id: number;
  name: string;
  email: string;
}

export interface Provider {
  id: number;
  name: string;
}

export interface PaymentOption {
  provider: string;
  rate: number;
  fee: number;
  received: number;
  processing_hours?: number;
}

export interface FindCheapestResponse {
  from_currency: string;
  to_currency: string;
  amount: number;
  options: PaymentOption[];
  best_option: PaymentOption | null;
  estimated_savings: number;
}

export interface LoginResponse {
  message: string;
  user: User;
}

export interface RegisterResponse {
  message: string;
  user?: User;
}

export interface TimingAlternative {
  provider: string;
  scheduled_time: string;
  completion_time: string;
  rate: number;
  fee: number;
  received: number;
  processing_hours: number;
}

export interface TimingOptimizationResponse {
  from_currency: string;
  to_currency: string;
  amount: number;
  deadline: string;

  recommended_provider: string;
  recommended_time: string;
  expected_completion: string;
  expected_received: number;
  exchange_rate: number;
  fee: number;
  processing_hours: number;

  safety_buffer_hours: number;
  latest_safe_time: string;

  alternatives: TimingAlternative[];
}

export interface AIRecommendation {
  provider: string;
  scheduled_time: string;
  completion_time: string;
  received: number;
  rate: number;
  fee: number;
  processing_hours: number;
}

export interface AIOptimizeResponse {
  intent: {
    amount: number;
    from: string;
    to: string;
    deadline: string;
  };

  recommendation: AIRecommendation;

  reason: string;

  alternatives: TimingAlternative[];
}