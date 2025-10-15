// Environment/environment.prod.ts
import { IEnvironment } from './environment.interface';

export const environment: IEnvironment = {
  production: true,
  apiUrl: 'https://produccion.com/api/',
  urlFrontend: 'https://produccion.com/',
  keyEncryption: 'KEY_ENCRYPTION'
};
