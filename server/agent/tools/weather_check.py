"""
更简单的单参数输入工具实现，用于查询现在天气的情况
"""
from pydantic import BaseModel, Field
import requests
from configs.kb_config import SENIVERSE_API_KEY


def weather(location: str, api_key: str):
    # url = f"https://api.seniverse.com/v3/weather/now.json?key={api_key}&location={location}&language=zh-Hans&unit=c"
    # response = requests.get(url)
    # if response.status_code == 200:
    #     data = response.json()
    #     weather = {
    #         "temperature": data["results"][0]["now"]["temperature"],
    #         "description": data["results"][0]["now"]["text"],
    #     }
    #     return weather
    # else:
    #     raise Exception(
    #         f"Failed to retrieve weather: {response.status_code}")
    print("location",location)
    
    return "4.4℃ 降水 0mm 相对湿度 96% 风力 微风 气压 1022hpa 03/25 (今天) 中雨转晴 12℃/4℃ 微风 03/26 (明天) 多云转小雨 19℃/11℃ 微风 03/27 (后天) 中雨转晴 14℃/13℃"



def weathercheck(location: str):
    return weather(location, SENIVERSE_API_KEY)


class WeatherInput(BaseModel):
    location: str = Field(description="City name,include city and county")
