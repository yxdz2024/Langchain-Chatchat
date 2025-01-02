from typing import Optional, Type
from langchain.tools import BaseTool
from pydantic import BaseModel, Field


class AddTravelInput(BaseModel):    
    location: Optional[str] = Field(description="城市名称，出差的出发地")
    target: Optional[str] = Field(description="城市名称，出差的目的地")
    date: Optional[str] = Field(description="日期,出差的日期")
    time: Optional[str] = Field(description="时间,出差的时间")

desc = (
    "能够帮助你完成网上订票，使用这个工具必须提供以下四个参数"
    "[target],[location],[date],[time]"

)

class Travel2(BaseTool):
    name = "Travel2"
    description = "能够帮助你完成网上订票，使用这个工具必须提供以下四个参数[]"
    args_schema: Type[BaseModel] = AddTravelInput
    return_direct: bool = True

    def _run(self,target:str,location:str,date:str,time:str):
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
