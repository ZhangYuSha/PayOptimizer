import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { App } from './app/app';
import '@mysten/dapp-kit-core/web';

bootstrapApplication(App, appConfig).catch((err) => console.error(err));
