
from fastapi import APIRouter, Depends

from src.application.use_cases.catalog.get_artwork_detail_use_case import GetArtworkDetailUseCase
from src.application.use_cases.catalog.list_artworks_use_case import ListArtworksUseCase
from src.presentation.dependencies import get_artwork_detail_use_case, get_list_artworks_use_case

router = APIRouter(prefix="/artworks", tags=["artworks"])


@router.get("")
def list_artworks(list_uc: ListArtworksUseCase = Depends(get_list_artworks_use_case)):
    artworks = list_uc.execute()
    return [
        {
            "artwork_id": art.artwork_id,
            "title": art.artwork_title,
            "status": art.artwork_status_label,
            "value": art.artwork_appraisal_value,
        }
        for art in artworks
    ]


@router.get("/{artwork_id}")
def get_artwork(
    artwork_id: str,
    detail_uc: GetArtworkDetailUseCase = Depends(get_artwork_detail_use_case),
):
    artwork = detail_uc.execute(artwork_id)
    return {
        "artwork_id": artwork.artwork_id,
        "title": artwork.artwork_title,
        "year": artwork.artwork_creation_year,
        "status": artwork.artwork_status_label,
    }
