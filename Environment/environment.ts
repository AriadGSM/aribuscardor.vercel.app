// Environment/environment.ts
import { IEnvironment } from './environment.interface';
export const environment: IEnvironment = {
  production: false,
  apiUrl: 'http://localhost:5000/api/',
  urlFrontend: 'http://localhost:4200/',
  keyEncryption: 'KEY_ENCRYPTION'
};
