from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = 'sqlite:///./hospital.db'
    jwt_secret: str = 'change-me-in-production'
    access_token_expire_minutes: int = 480
    frontend_url: str = 'http://localhost:5173'
    freshness_threshold_minutes: int = 15
    stale_threshold_minutes: int = 30
    prediction_confidence_threshold: float = 0.7
    simulation_speed: float = 1.0
    target_improvement_percentage: float = 20.0
    
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

settings = Settings()
