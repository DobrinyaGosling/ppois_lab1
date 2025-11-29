from fastapi import HTTPException, status

class FoodDeliveryDomainError(HTTPException):
    def __init__(
        self,
        *,
        code: str = "domain_error",
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ) -> None:
        super().__init__(status_code=status_code, detail=code)
        self.code = code
