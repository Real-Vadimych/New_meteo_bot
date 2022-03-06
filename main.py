import foreing
import russian


def get_weather(req_type: str, airport: str) -> str:
    result_text = foreing.get_weather(req_type, airport)
    if result_text == "not in database":
        result_text = russian.get_weather(req_type, airport)
    return result_text


if __name__ == "__main__":
    print(get_weather("TAF", "KORD"))
