import {
  Component,
  CUSTOM_ELEMENTS_SCHEMA,
  signal
} from '@angular/core';

import {
  RouterOutlet
} from '@angular/router';

@Component({

  imports: [
    RouterOutlet
  ],

  schemas: [
    CUSTOM_ELEMENTS_SCHEMA
  ],

  selector:
    'app-root',

  styleUrl:
    './app.css',

  templateUrl:
    './app.html'

})
export class App {

  protected readonly title =
    signal('pay-optimizer');

}