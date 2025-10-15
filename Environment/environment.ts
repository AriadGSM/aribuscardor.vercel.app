// Environment/environment.ts
import { IEnvironment } from './environment.interface';
export const environment: IEnvironment = {
  production: false,
  apiUrl: 'http://127.0.0.1:5000/api/',
  urlFrontend: 'http://127.0.0.1:5000/',
  keyEncryption: 'KEY_ENCRYPTION'
};
