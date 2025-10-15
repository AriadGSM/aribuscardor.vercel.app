import { Environment } from './Environment';

// En cualquier archivo donde necesites la configuración
const env = Environment.getInstance();

// Acceder a las propiedades
const apiUrl = env.apiUrl;
const isProduction = env.production;