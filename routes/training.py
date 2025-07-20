from fastapi import APIRouter, UploadFile
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException, RequestValidationError, ResponseValidationError
from fastapi import status
from collections import defaultdict
from services import TrainService, SaveToS3Service, SaveToDynamoDBService
from loguru import logger
from configs import *
from os.path import exists
from os import remove

training_route = APIRouter(
    prefix='/training',
    tags=['API'],
    default_response_class=JSONResponse,
)

@training_route.post('', status_code=status.HTTP_201_CREATED)
def training(training_set: UploadFile) -> JSONResponse:
    content = defaultdict(any)
    status_code = status.HTTP_201_CREATED
    err_description = None

    try:
        train_service = TrainService(tmp_path=TMP_PATH)
        message, data = train_service.train(file_object=training_set.file, file_name=training_set.filename)
        if not data:
            raise ResponseValidationError(errors=[message])
        logger.success(message)

        with SaveToDynamoDBService(AWS_CONFIGS, DYNAMODB_TABLE_NAME) as service:
            method_status, message = service.save(*data[:4])
            if not method_status:
                raise ResponseValidationError(errors=[message])
        logger.success(message)
        
        with SaveToS3Service(AWS_CONFIGS, S3_BUCKET_NAME) as service:
            method_status, message = service.save(*data[1:])
            if not method_status:
                raise ResponseValidationError(errors=[message])
        logger.success(message)
        
        full_path_to_vectorizer, full_path_to_model = data[-2], data[-1]

        for item in [full_path_to_vectorizer, full_path_to_model]:
            if not exists(item):
                continue
            remove(item)

        content['status'], content['message'] = True, f'All steps have been completed successfully. You can now use the API to obtain forecasts from the model. Your USER_ID is {data[0]}.'
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