from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException, RequestValidationError, ResponseValidationError
from fastapi import status
from collections import defaultdict
from services import GetInfoFromDynamoDBService, GetDataFromS3Service, PredictionService
from configs import *
from loguru import logger

prediction_route = APIRouter(
    prefix='/prediction',
    tags=['API'],
    default_response_class=JSONResponse,
)

@prediction_route.post('', status_code=status.HTTP_200_OK)
def prediction(
    id: str = Form(default='09a19fb6-8c57-41a7-92fc-5b0837616de0'), 
    text: str = Form(default='How should I wash my lingerie?')
) -> JSONResponse:
    content = defaultdict(any)
    status_code = status.HTTP_200_OK
    err_description = None

    try:
        with GetInfoFromDynamoDBService(AWS_CONFIGS, DYNAMODB_TABLE_NAME) as service:
            method_status, message, data = service.get(id)
            if not method_status:
                raise ResponseValidationError(errors=[message])
        logger.success(f'GetInfoFromDynamoDBService.get is {method_status}.')
        
        dir = f'{TMP_PATH}/{id}'
        with GetDataFromS3Service(AWS_CONFIGS, S3_BUCKET_NAME) as service:
            method_status, message, data = service.get(dir, *data)
            if not method_status:
                raise ResponseValidationError(errors=[message])
        logger.success(f'GetDataFromS3Service.get is {method_status}.')
        
        service = PredictionService()
        method_status, message = service.predict(*data, text=text)
        if not method_status:
            raise ResponseValidationError(errors=[message])
        
        content['status'], content['prediction'] = True, message
        return JSONResponse(
            content=content,
            status_code=status_code
        )

    except (RequestValidationError, ResponseValidationError, ) as e:
        err_description = str(e)
        status_code = status.HTTP_400_BAD_REQUEST

    except (Exception, HTTPException, ) as e:
        err_description = str(e)
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    content['err_description'] = err_description
    content['status'] = False

    return JSONResponse(
        content=content, 
        status_code=status_code
    )