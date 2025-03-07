from app.domain.tools.base import Tool
from pydantic import BaseModel


class ReportSchema(BaseModel):
    report: str


def report_function(report: ReportSchema) -> str:
    if isinstance(report, ReportSchema):
        return report.report
    else:
        raise TypeError("report must be an instance of ReportSchema")


report_tool = Tool(
    name="report_tool",
    model=ReportSchema,
    function=report_function,
    validate_missing=False,
    parse_model=True
)