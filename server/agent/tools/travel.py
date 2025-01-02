
from typing import Optional
from pydantic import BaseModel, Field


def add_travel(target:str,location:str,date:str,time:str):
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

    if not location:
        return "需要提供出发地"
    if not target:
        return "需要提供目的地"
    if not date:
        return "需要提供出发日期"
    if not time:
        return "需要提供出发时间"

    print("location",location)
    print("target",target)
    print("date",date)
    print("time",time)
    
    return f"尊敬的用户您好，您已成功预订{date}，G6810次15车9D(过道)，{location}-{target}，{time}开，检票口以车站为准。/n[天气]汉口，多云，最高气温22度最低气温17度。/n[出行]订餐、约车、二维码检票、退改签，请点击http://s.12306.cn/s/i 。"

class AddTravelInput(BaseModel):    
    location: Optional[str] = Field(description="City name,include city and county,The place of departure for business trips")
    target: Optional[str] = Field(description="City name,include city and county,The destination of the business trip")
    date: Optional[str] = Field(description="date,Departure date")
    time: Optional[str] = Field(description="time,Departure date")
    