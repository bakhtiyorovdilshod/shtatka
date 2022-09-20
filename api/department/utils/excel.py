from io import BytesIO
from fastapi.responses import StreamingResponse


def xls_response(output: BytesIO, filename="shtatka.xlsx"):
    headers = {
        'Content-Disposition': 'attachment; filename=%s' % filename
    }
    return StreamingResponse(output, headers=headers)
