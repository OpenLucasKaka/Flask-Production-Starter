from typing import Optional

from pydantic import BaseModel, Field


class PosterCreate(BaseModel):
    """帖子新增请求"""

    title: str = Field(..., min_length=3, max_length=15, description="标题")
    content: str = Field(..., description="内容")
    status: int = Field(4, description="状态：4=草稿, 256=发布")


class PosterUpdate(BaseModel):
    """帖子更新请求"""

    title: Optional[str] = Field(None, min_length=3, max_length=15, description="标题")
    content: Optional[str] = Field(None, description="内容")
    status: Optional[int] = Field(None, description="状态：4=草稿, 256=发布")


class ListPosterQuery(BaseModel):
    """帖子列表查询参数"""

    page: int = Field(1, ge=1, description="当前页数")
    page_size: int = Field(10, ge=1, le=100, description="每页数量")
    status: Optional[int] = Field(None, description="状态筛选")
