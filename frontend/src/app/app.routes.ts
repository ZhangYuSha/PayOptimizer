import {
  Routes
} from '@angular/router';

import {
  HomeComponent
} from './pages/home/home.component';

import {
  LoginComponent
} from './pages/login/login.component';

import {
  RegisterComponent
} from './pages/register/register.component';

import {
  CompareComponent
} from './pages/compare/compare.component';

import {
  AIComponent
} from './pages/ai/ai.component';


export const routes: Routes = [

  {
    path: '',
    component: HomeComponent
  },

  {
    path: 'login',
    component: LoginComponent
  },

  {
    path: 'register',
    component: RegisterComponent
  },

  {
    path: 'compare',
    component: CompareComponent
  },

  {
    path: 'ai',
    component: AIComponent
  },

  {
    path: '**',
    redirectTo: ''
  }

];