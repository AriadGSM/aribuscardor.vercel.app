export class Environment {
    private static instance: Environment;
    private _production: boolean;
    private _apiUrl: string;
    private _urlFrontend: string;
    private _keyEncryption: string;

    private constructor() {
        this._production = false;
        this._apiUrl = 'https://localhost:7089/api/';
        this._urlFrontend = 'https://localhost:7089/';
        this._keyEncryption = 'KEY_ENCRYPTION';
        
        // Cargar configuración de forma asíncrona
        this.loadConfig();
    }

    private async loadConfig() {
        try {
            const response = await fetch('../appsettings.json');
            const config = await response.json();
            this._production = config.Environment === 'Production';
            
            if (this._production) {
                this._apiUrl = 'https://tu_servidor_produccion/api/';
                this._urlFrontend = 'https://tu_servidor_produccion/';
            }
        } catch (error) {
            console.error('Error loading config:', error);
        }
    }

    public static getInstance(): Environment {
        if (!Environment.instance) {
            Environment.instance = new Environment();
        }
        return Environment.instance;
    }

    get production(): boolean {
        return this._production;
    }

    get apiUrl(): string {
        return this._apiUrl;
    }

    get urlFrontend(): string {
        return this._urlFrontend;
    }

    get keyEncryption(): string {
        return this._keyEncryption;
    }
}