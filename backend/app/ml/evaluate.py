from app.ml.predict import get_metrics

def evaluate() -> dict:
    return get_metrics()

if __name__ == "__main__":
    import json
    print(json.dumps(evaluate(), indent=2))
